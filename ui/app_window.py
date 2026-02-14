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
        self.title("Gerador de Mapa de Sala - Classroom Map")
        self.geometry("1300x750")
        self.resizable(False, False)
        
        # Tema
        ctk.set_appearance_mode("Light")
        self.configure(fg_color=Theme.BACKGROUND_LIGHT)

        # === LAYOUT (2 Colunas) ===
        # Col 0: Sidebar - Compacta
        # Col 1: Visualizer (Preview) - Maior
        self.grid_columnconfigure(0, weight=0, minsize=240)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._setup_ui()
    
    def _setup_ui(self):
        """Configura a interface principal"""
        
        # === SIDEBAR ESQUERDA (TUDO) ===
        from .sidebar_unified import SidebarUnified
        self.sidebar = SidebarUnified(
            self,
            width=240,
            on_change=self.handle_config_change,
            on_generate=self.handle_generate,
            on_save=self.handle_save,
            on_load=self.handle_load,
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
        from tkinter import filedialog
        from utils.file_handler import FileHandler
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Arquivo JSON", "*.json"), ("Todos os arquivos", "*.*")],
            title="Salvar Configuração"
        )
        
        if filename:
            try:
                full_data = {
                    "config": self.sidebar.get_config(),
                    "students": self.sidebar.get_students(),
                    "seating_map": {str(k): v for k, v in self.visualizer.seating_map.items()}
                }
                
                if FileHandler.save_layout(full_data, filename):
                    ToastNotification.show(self.center_frame, "Configuração salva!", type="success")
            except Exception as e:
                ToastNotification.show(self.center_frame, "Erro ao salvar arquivo", type="error")
    
    def handle_load(self):
        from tkinter import filedialog
        from utils.file_handler import FileHandler
        
        filename = filedialog.askopenfilename(
            filetypes=[("Arquivo JSON", "*.json"), ("Todos os arquivos", "*.*")],
            title="Carregar Configuração"
        )
        
        if filename:
            try:
                data = FileHandler.load_layout(filename)
                if data:
                    if "config" in data:
                        self.visualizer.update_config(data["config"])
                    
                    if "seating_map" in data:
                        seating = {}
                        for k, v in data["seating_map"].items():
                            try:
                                parts = k.strip("()").split(',')
                                col, row = int(parts[0]), int(parts[1])
                                seating[(col, row)] = v
                            except:
                                pass
                        self.visualizer.set_seating(seating)
                    
                    ToastNotification.show(self.center_frame, "Configuração carregada!", type="success")
            except Exception as e:
                ToastNotification.show(self.center_frame, "Erro ao carregar arquivo", type="error")
    
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
