import customtkinter as ctk
from .theme import Theme
from .animations import LoadingOverlay, ToastNotification

class AppWindow(ctk.CTk):
    """
    Janela principal do aplicativo
    Design de 2 colunas: Sidebar (Config+Turmas) e Preview
    """
    def __init__(self):
        super().__init__()

        # === CONFIGURAÇÃO DA JANELA ===
        self.title("Gerador de Mapa de Sala")
        self.geometry("1300x750")
        self.resizable(False, False)
        
        # Ícone do app (taskbar + titlebar)
        import os, sys
        if sys.platform == "win32":
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("classroommap.app")
        
        try:
            import os
            if sys.platform == "win32":
                ico_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icon", "app.ico")
                if os.path.exists(ico_path):
                    self.after(10, lambda: self.iconbitmap(ico_path))
        except Exception as e:
            print(f"Icon error: {e}")
        
        # Tema
        ctk.set_appearance_mode("Light")
        self.configure(fg_color=Theme.BACKGROUND_LIGHT)

        # === LAYOUT (2 Colunas) ===
        self.grid_columnconfigure(0, weight=0, minsize=240)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._setup_ui()
    
    def _setup_ui(self):
        """Configura a interface principal"""
        
        # === SIDEBAR ESQUERDA ===
        from .sidebar_unified import SidebarUnified
        self.sidebar = SidebarUnified(
            self,
            width=240,
            on_change=self.handle_config_change,
            on_generate=self.handle_generate,
            on_save=self.handle_save,
            on_load=self.handle_load,
            on_delete=self.handle_delete,
            on_export=self.handle_export
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # === VISUALIZADOR (CENTRO - MAIOR) ===
        self.center_frame = ctk.CTkFrame(self, fg_color=Theme.BACKGROUND_LIGHT, corner_radius=0)
        self.center_frame.grid(row=0, column=1, sticky="nsew")
        self.center_frame.grid_rowconfigure(0, weight=1)
        self.center_frame.grid_columnconfigure(0, weight=1)
        
        from .classroom_visualizer import ClassroomVisualizer
        self.visualizer = ClassroomVisualizer(self.center_frame)
        self.visualizer.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Loading Overlay
        self.loading = LoadingOverlay(self.center_frame)
        
        # Refresh dropdown on startup
        self.after(500, self._refresh_saves)
    
    # === HELPERS ===
    
    def _refresh_saves(self):
        """Atualiza a lista de saves no dropdown"""
        from utils.file_handler import FileHandler
        saves = FileHandler.list_saves()
        self.sidebar.refresh_saves_dropdown(saves)
    
    # === HANDLERS ===
    
    def handle_config_change(self, config):
        """Callback quando a configuração da sala muda"""
        self.visualizer.update_config(config)
    
    def handle_generate(self):
        """Gera o mapa de assentos"""
        try:
            config = self.sidebar.get_config()
            students_dict = self.sidebar.get_students()
            
            if not any(students_dict.values()):
                ToastNotification.show(
                    self.center_frame,
                    "Adicione pelo menos um aluno",
                    type="warning"
                )
                return
            
            self.visualizer.update_config(config)
            self.loading.show("Gerando mapa")
            
            def process():
                try:
                    data_for_manager = {'classes': students_dict}
                    
                    from logic.student_manager import StudentManager
                    from logic.seating_algorithm import SeatingAlgorithm
                    
                    sm = StudentManager()
                    sm.parse_input(data_for_manager)
                    
                    algo = SeatingAlgorithm()
                    seating_map = algo.generate_seating(config, sm)
                    
                    self.after(0, lambda: self._finish_generation(seating_map))
                except Exception as e:
                    self.after(0, lambda: self._handle_generation_error(e))
            
            self.after(300, process)
            
        except Exception as e:
            self._handle_generation_error(e)
    
    def _finish_generation(self, seating_map):
        self.loading.hide()
        self.visualizer.set_seating(seating_map)
        ToastNotification.show(self.center_frame, "Mapa gerado com sucesso!", type="success")
    
    def _handle_generation_error(self, error):
        self.loading.hide()
        print(f"Erro ao gerar mapa: {error}")
        ToastNotification.show(self.center_frame, "Erro ao gerar mapa", type="error")
    
    def handle_save(self):
        """Salva o layout internamente usando o nome da sala"""
        from utils.file_handler import FileHandler
        
        config = self.sidebar.get_config()
        room_name = config.get("room_name", "").strip()
        
        if not room_name:
            ToastNotification.show(self.center_frame, "Preencha o nome da sala primeiro", type="warning")
            return
        
        try:
            full_data = {
                "config": config,
                "students": self.sidebar.get_students(),
                "seating_map": {str(k): v for k, v in self.visualizer.seating_map.items()}
            }
            
            if FileHandler.save_internal(room_name, full_data):
                self._refresh_saves()
                # Select the just-saved item
                self.sidebar.saves_dropdown.set(room_name)
                ToastNotification.show(self.center_frame, f"'{room_name}' salvo!", type="success")
            else:
                ToastNotification.show(self.center_frame, "Erro ao salvar", type="error")
        except Exception as e:
            print(f"Erro ao salvar: {e}")
            ToastNotification.show(self.center_frame, "Erro ao salvar", type="error")
    
    def handle_load(self):
        """Carrega o layout selecionado no dropdown"""
        from utils.file_handler import FileHandler
        
        selected = self.sidebar.get_selected_save()
        if not selected:
            ToastNotification.show(self.center_frame, "Selecione um layout salvo", type="warning")
            return
        
        try:
            data = FileHandler.load_internal(selected)
            if data:
                # Restore config
                if "config" in data:
                    self.sidebar.set_config(data["config"])
                    self.visualizer.update_config(data["config"])
                
                # Restore students
                if "students" in data:
                    self.sidebar.set_students(data["students"])
                
                # Restore seating map
                if "seating_map" in data:
                    seating = {}
                    for k, v in data["seating_map"].items():
                        try:
                            parts = k.strip("()").split(',')
                            col, row = int(parts[0].strip()), int(parts[1].strip())
                            seating[(col, row)] = v
                        except:
                            pass
                    self.visualizer.set_seating(seating)
                
                ToastNotification.show(self.center_frame, f"'{selected}' carregado!", type="success")
            else:
                ToastNotification.show(self.center_frame, "Erro ao carregar layout", type="error")
        except Exception as e:
            print(f"Erro ao carregar: {e}")
            ToastNotification.show(self.center_frame, "Erro ao carregar", type="error")
    
    def handle_delete(self):
        """Exclui o layout selecionado no dropdown"""
        from utils.file_handler import FileHandler
        
        selected = self.sidebar.get_selected_save()
        if not selected:
            ToastNotification.show(self.center_frame, "Selecione um layout para excluir", type="warning")
            return
        
        if FileHandler.delete_save(selected):
            self._refresh_saves()
            ToastNotification.show(self.center_frame, f"'{selected}' excluído!", type="success")
        else:
            ToastNotification.show(self.center_frame, "Erro ao excluir", type="error")
    
    def handle_export(self):
        from tkinter import filedialog
        from utils.pdf_exporter import PDFExporter
        from datetime import datetime
        
        if not self.visualizer.seating_map:
            ToastNotification.show(self.center_frame, "Gere o mapa antes de exportar", type="warning")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Arquivo PDF", "*.pdf"), ("Todos os arquivos", "*.*")],
            title="Exportar para PDF"
        )
        
        if filename:
            try:
                self.loading.show("Exportando PDF")
                def export():
                    try:
                        config = self.visualizer.current_config
                        room_name = config.get("room_name", "").strip() or "Sala de Aula"
                        date_str = datetime.now().strftime("%d/%m/%Y")
                        
                        PDFExporter.export(
                            config,
                            self.visualizer.seating_map,
                            room_name,
                            date_str,
                            filename
                        )
                        self.after(0, lambda: self._finish_export(filename))
                    except Exception as e:
                        self.after(0, lambda: self._handle_export_error(e))
                self.after(300, export)
            except Exception as e:
                self._handle_export_error(e)
    
    def _finish_export(self, filename):
        self.loading.hide()
        ToastNotification.show(self.center_frame, "PDF exportado com sucesso!", type="success")
    
    def _handle_export_error(self, error):
        self.loading.hide()
        print(f"Erro ao exportar: {error}")
        ToastNotification.show(self.center_frame, "Erro ao exportar PDF", type="error")

    def run(self):
        self.mainloop()

