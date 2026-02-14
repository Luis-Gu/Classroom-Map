import customtkinter as ctk
from .theme import Theme
from .furniture_selector import FurnitureSelector

class SidebarLeft(ctk.CTkFrame):
    """
    Sidebar Esquerda: Configuração da Sala
    Contém: Nome, Layout das filas, Mobília
    """
    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_change = on_change
        
        # Configuração visual
        self.configure(fg_color=Theme.WHITE_PURE, corner_radius=0)
        
        # Container principal (sem scroll)
        self.scroll = ctk.CTkFrame(
            self, 
            fg_color="transparent"
        )
        self.scroll.pack(fill="both", expand=True, padx=0, pady=0)

        # === CABEÇALHO ===
        self._build_header()
        
        # === NOME DA SALA ===
        self._build_room_section()
        
        # === LAYOUT DAS FILAS ===
        self._build_rows_section()
        
        # === MOBÍLIA ===
        self._build_furniture_section()

    def _build_header(self):
        """Cabeçalho compacto"""
        header_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        header_frame.pack(padx=12, pady=(10, 6), fill="x")
        
        title = ctk.CTkLabel(
            header_frame,
            text="Configuração",
            font=(Theme.FONT_FAMILY, 16, "bold"),
            text_color=Theme.TEXT_PRIMARY,
            anchor="w"
        )
        title.pack(anchor="w")
        


    def _build_room_section(self):
        """Seção do nome da sala - compacta"""
        section_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        section_frame.pack(padx=12, pady=(4, 0), fill="x")
        
        label = ctk.CTkLabel(
            section_frame,
            text="NOME DA SALA",
            font=(Theme.FONT_FAMILY, 9, "bold"),
            text_color=Theme.TEXT_TERTIARY,
            anchor="w"
        )
        label.pack(anchor="w", pady=(0, 2))
        
        self.entry_room = ctk.CTkEntry(
            section_frame,
            placeholder_text="Ex: Sala 1A...",
            border_width=0,
            fg_color=Theme.NEUTRAL_SOFT,
            text_color=Theme.TEXT_PRIMARY,
            height=32,
            corner_radius=6,
            font=(Theme.FONT_FAMILY, 11)
        )
        self.entry_room.pack(fill="x")
        
        # Bind para atualizar config quando mudar (opcional, ou só ao gerar)
        self.entry_room.bind("<KeyRelease>", lambda e: self.on_config_change())

    def _build_rows_section(self):
        """Seção de sliders das filas - compacta"""
        self._build_section_header("LAYOUT DAS FILAS")
        
        section_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        section_frame.pack(padx=12, pady=(2, 0), fill="x")
        
        self.row_vars = []
        self.row_value_labels = []
        
        for i in range(4):
            row_container = ctk.CTkFrame(section_frame, fg_color="transparent")
            row_container.pack(fill="x", pady=2)
            
            top_frame = ctk.CTkFrame(row_container, fg_color="transparent")
            top_frame.pack(fill="x", pady=(0, 2))
            
            ctk.CTkLabel(
                top_frame,
                text=f"Fila {i+1}",
                font=(Theme.FONT_FAMILY, 11, "bold"),
                text_color=Theme.TEXT_PRIMARY,
                anchor="w"
            ).pack(side="left")
            
            val_lbl = ctk.CTkLabel(
                top_frame,
                text="7",
                font=(Theme.FONT_FAMILY, 11, "bold"),
                text_color=Theme.ACCENT_PRIMARY,
                anchor="e"
            )
            val_lbl.pack(side="right")
            self.row_value_labels.append(val_lbl)
            
            slider = ctk.CTkSlider(
                row_container,
                from_=1,
                to=15,
                number_of_steps=14,
                button_color=Theme.ACCENT_PRIMARY,
                button_hover_color=Theme.ACCENT_HOVER,
                progress_color=Theme.ACCENT_PRIMARY,
                fg_color=Theme.BORDER_LIGHT,
                height=5,
                button_length=12
            )
            slider.set(7)
            slider.pack(fill="x")
            
            slider.configure(command=lambda v, idx=i: self._update_slider_value(idx, v))
            self.row_vars.append(slider)

    def _update_slider_value(self, index, value):
        self.row_value_labels[index].configure(text=str(int(value)))
        self.on_config_change()

    def _build_furniture_section(self):
        self._build_section_header("MOBÍLIA DA SALA")
        
        section_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        section_frame.pack(padx=12, pady=(2, 0), fill="x")
        
        self.fs_board = FurnitureSelector(
            section_frame, 
            "Quadro", 
            "board", 
            "Topo", 
            command=self.check_conflicts
        )
        self.fs_board.pack(fill="x", pady=(0, 4))

        self.fs_door = FurnitureSelector(
            section_frame, 
            "Porta", 
            "door", 
            "Esq", 
            command=self.check_conflicts
        )
        self.fs_door.pack(fill="x", pady=(0, 4))

        self.fs_windows = FurnitureSelector(
            section_frame, 
            "Janelas", 
            "windows", 
            "Dir", 
            command=self.check_conflicts
        )
        self.fs_windows.pack(fill="x", pady=(0, 4))

    def check_conflicts(self, source, value):
        if value == "Nenhum":
            self.on_config_change()
            return
        
        targets = {
            "board": self.fs_board,
            "door": self.fs_door,
            "windows": self.fs_windows
        }
        
        for key, widget in targets.items():
            if key != source and widget.get() == value:
                widget.set("Nenhum")
        
        self.on_config_change()

    def _build_section_header(self, title):
        header = ctk.CTkFrame(self.scroll, fg_color="transparent")
        header.pack(padx=12, pady=(8, 2), fill="x")
        ctk.CTkLabel(
            header,
            text=title,
            font=(Theme.FONT_FAMILY, 9, "bold"),
            text_color=Theme.TEXT_TERTIARY
        ).pack(anchor="w")

    def check_conflicts(self, source, value):
        if value == "Nenhum":
            self.on_config_change()
            return
        
        targets = {
            "board": self.fs_board,
            "door": self.fs_door,
            "windows": self.fs_windows
        }
        
        for key, widget in targets.items():
            if key != source and widget.get() == value:
                widget.set("Nenhum")
        
        self.on_config_change()

    def on_config_change(self, *args):
        if self.on_change:
            self.on_change(self.get_config())

    def get_config(self):
        return {
            "rows": [int(s.get()) for s in self.row_vars],
            "board": self.fs_board.get(),
            "door": self.fs_door.get(),
            "windows": self.fs_windows.get(),
            "room_name": self.entry_room.get()
        }
