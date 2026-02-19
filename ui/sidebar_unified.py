import customtkinter as ctk
from .theme import Theme
from .furniture_selector import FurnitureSelector

class SidebarUnified(ctk.CTkFrame):
    """
    Sidebar unificada: Configuração, Turmas e Ações
    Usa scroll para caber todo o conteúdo
    """
    def __init__(self, master, on_change=None, on_generate=None, on_save=None, on_load=None, on_delete=None, on_export=None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_change = on_change
        self.on_generate = on_generate
        self.on_save = on_save
        self.on_load = on_load
        self.on_delete = on_delete
        self.on_export = on_export
        
        self.configure(fg_color=Theme.WHITE_PURE, corner_radius=0)
        
        # Container com scroll
        self.scroll = ctk.CTkScrollableFrame(
            self, 
            fg_color="transparent",
            scrollbar_button_color=Theme.BORDER,
            scrollbar_button_hover_color=Theme.GRAY_NEUTRAL
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
        
        # === TURMAS ===
        self._build_classes_section()
        
        # === BOTÕES DE AÇÃO (fora do scroll) ===
        self._build_actions_panel()

    def _build_header(self):
        header_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        header_frame.pack(padx=12, pady=(10, 6), fill="x")

        ctk.CTkLabel(
            header_frame,
            text="Configuração",
            font=(Theme.FONT_FAMILY, 16, "bold"),
            text_color=Theme.TEXT_PRIMARY,
            anchor="w"
        ).pack(anchor="w")

    def _build_section_header(self, title):
        header = ctk.CTkFrame(self.scroll, fg_color="transparent")
        header.pack(padx=12, pady=(10, 2), fill="x")
        ctk.CTkLabel(
            header,
            text=title,
            font=(Theme.FONT_FAMILY, 9, "bold"),
            text_color=Theme.TEXT_TERTIARY
        ).pack(anchor="w")

    def _build_room_section(self):
        section_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        section_frame.pack(padx=12, pady=(4, 0), fill="x")
        
        ctk.CTkLabel(
            section_frame,
            text="NOME DA SALA",
            font=(Theme.FONT_FAMILY, 9, "bold"),
            text_color=Theme.TEXT_TERTIARY,
            anchor="w"
        ).pack(anchor="w", pady=(0, 2))
        
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
        self.entry_room.bind("<KeyRelease>", lambda e: self.on_config_change())

    def _build_rows_section(self):
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
                height=14,
                button_length=0,
                button_corner_radius=7
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

    def _build_classes_section(self):
        """Seção de turmas — custom tabs (sem CTkTabview)"""
        self._build_section_header("TURMAS")
        
        section_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        section_frame.pack(padx=12, pady=(2, 0), fill="x")
        
        # === CUSTOM TAB BUTTONS ===
        tab_bar = ctk.CTkFrame(section_frame, fg_color="transparent")
        tab_bar.pack(fill="x", pady=(0, 6))
        
        self._active_tab = 0
        self._tab_buttons = []
        
        for i, label in enumerate(["Turma 1", "Turma 2"]):
            btn = ctk.CTkButton(
                tab_bar,
                text=label,
                height=30,
                corner_radius=15,
                font=(Theme.FONT_FAMILY, 11, "bold"),
                command=lambda idx=i: self._switch_tab(idx)
            )
            btn.pack(side="left", padx=(0, 6))
            self._tab_buttons.append(btn)
        
        # === TAB CONTENT FRAMES ===
        self._tab_container = ctk.CTkFrame(section_frame, fg_color="transparent")
        self._tab_container.pack(fill="x")
        
        self._tab_frames = []
        
        frame1 = ctk.CTkFrame(self._tab_container, fg_color="transparent")
        self._tab_frames.append(frame1)
        self._build_class_content(frame1, "TURMA A", True)
        
        frame2 = ctk.CTkFrame(self._tab_container, fg_color="transparent")
        self._tab_frames.append(frame2)
        self._build_class_content(frame2, "TURMA B", False)
        
        # Show first tab
        self._switch_tab(0)

    def _switch_tab(self, index):
        """Troca a aba ativa"""
        self._active_tab = index
        
        for i, frame in enumerate(self._tab_frames):
            if i == index:
                frame.pack(fill="x", in_=self._tab_container)
            else:
                frame.pack_forget()
        
        for i, btn in enumerate(self._tab_buttons):
            if i == index:
                btn.configure(
                    fg_color=Theme.ACCENT_PRIMARY,
                    hover_color=Theme.ACCENT_HOVER,
                    text_color=Theme.TEXT_LIGHT
                )
            else:
                btn.configure(
                    fg_color=Theme.SELECTED,
                    hover_color=Theme.ACCENT_SOFT_HOVER,
                    text_color=Theme.ACCENT_PRIMARY
                )

    def _build_class_content(self, parent, default_name, is_first=True):
        """Conteúdo de cada aba de turma"""
        ctk.CTkLabel(
            parent,
            text="Nome da turma",
            font=(Theme.FONT_FAMILY, 9),
            text_color=Theme.TEXT_TERTIARY,
            anchor="w"
        ).pack(fill="x", pady=(2, 1))
        
        entry = ctk.CTkEntry(
            parent,
            placeholder_text="Ex: 1\u00aa S\u00e9rie E",
            border_width=1,
            border_color=Theme.BORDER,
            fg_color=Theme.WHITE_PURE,
            text_color=Theme.TEXT_PRIMARY,
            height=32,
            corner_radius=6,
            font=(Theme.FONT_FAMILY, 12)
        )
        entry.pack(fill="x", pady=(0, 6))
        entry.insert(0, default_name)
        
        ctk.CTkLabel(
            parent,
            text="Alunos (um por linha)",
            font=(Theme.FONT_FAMILY, 9),
            text_color=Theme.TEXT_TERTIARY,
            anchor="w"
        ).pack(fill="x", pady=(0, 1))
        
        textbox = ctk.CTkTextbox(
            parent,
            font=(Theme.FONT_FAMILY, 12),
            fg_color=Theme.WHITE_PURE,
            border_width=1,
            border_color=Theme.BORDER,
            corner_radius=6,
            text_color=Theme.TEXT_PRIMARY,
            wrap="word",
            height=130
        )
        textbox.pack(fill="x", pady=(0, 4))
        
        placeholder = "Jo\u00e3o Silva\nMaria Santos\nAna Carolina"
        textbox.insert("0.0", placeholder)
        textbox.configure(text_color=Theme.TEXT_TERTIARY)
        
        def on_focus_in(event):
            if textbox.get("0.0", "end-1c") == placeholder:
                textbox.delete("0.0", "end")
                textbox.configure(text_color=Theme.TEXT_PRIMARY)
        
        def on_focus_out(event):
            if not textbox.get("0.0", "end-1c").strip():
                textbox.insert("0.0", placeholder)
                textbox.configure(text_color=Theme.TEXT_TERTIARY)
        
        textbox.bind("<FocusIn>", on_focus_in)
        textbox.bind("<FocusOut>", on_focus_out)
        
        if is_first:
            self.entry_name_1 = entry
            self.txt_class_1 = textbox
        else:
            self.entry_name_2 = entry
            self.txt_class_2 = textbox

    def _build_actions_panel(self):
        """Painel de ações no fundo (fora do scroll)"""
        panel = ctk.CTkFrame(self, fg_color=Theme.WHITE_PURE, corner_radius=0)
        panel.pack(fill="x", side="bottom", padx=0, pady=0)
        
        separator = ctk.CTkFrame(panel, height=1, fg_color=Theme.BORDER)
        separator.pack(fill="x", pady=(0, 6))
        
        inner = ctk.CTkFrame(panel, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=12, pady=(0, 10))
        
        # === GERAR MAPA ===
        self.btn_generate = ctk.CTkButton(
            inner,
            text="✨ GERAR MAPA",
            fg_color=Theme.ACCENT_PRIMARY,
            hover_color=Theme.ACCENT_HOVER,
            height=40,
            corner_radius=20,
            font=(Theme.FONT_FAMILY, 12, "bold"),
            text_color=Theme.TEXT_LIGHT,
            command=self._on_generate
        )
        self.btn_generate.pack(fill="x", pady=(0, 8))
        
        # === LAYOUTS SALVOS ===
        saves_label = ctk.CTkLabel(
            inner,
            text="LAYOUTS SALVOS",
            font=(Theme.FONT_FAMILY, 9, "bold"),
            text_color=Theme.TEXT_TERTIARY,
            anchor="w"
        )
        saves_label.pack(anchor="w", pady=(0, 3))
        
        # Dropdown de layouts salvos
        self.saves_dropdown = ctk.CTkOptionMenu(
            inner,
            values=["(nenhum)"],
            fg_color=Theme.NEUTRAL_SOFT,
            button_color=Theme.BORDER,
            button_hover_color=Theme.GRAY_NEUTRAL,
            text_color=Theme.TEXT_PRIMARY,
            dropdown_fg_color=Theme.WHITE_PURE,
            dropdown_text_color=Theme.TEXT_PRIMARY,
            dropdown_hover_color=Theme.HOVER_LIGHT,
            height=30,
            corner_radius=6,
            font=(Theme.FONT_FAMILY, 10),
            dropdown_font=(Theme.FONT_FAMILY, 10)
        )
        self.saves_dropdown.pack(fill="x", pady=(0, 5))
        
        # Botões: Salvar | Carregar | Excluir
        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.pack(fill="x", pady=(0, 5))
        btn_row.grid_columnconfigure(0, weight=1)
        btn_row.grid_columnconfigure(1, weight=1)
        btn_row.grid_columnconfigure(2, weight=1)
        
        self._create_secondary_button(btn_row, "💾 Salvar", self._on_save).grid(
            row=0, column=0, padx=(0, 2), sticky="ew")
        self._create_secondary_button(btn_row, "📂 Carregar", self._on_load).grid(
            row=0, column=1, padx=2, sticky="ew")
        
        btn_delete = ctk.CTkButton(
            btn_row,
            text="🗑️ Excluir",
            fg_color="transparent",
            border_width=1,
            border_color="#e53935",
            text_color="#e53935",
            hover_color="#ffebee",
            height=28,
            corner_radius=6,
            font=(Theme.FONT_FAMILY, 10, "bold"),
            command=self._on_delete
        )
        btn_delete.grid(row=0, column=2, padx=(2, 0), sticky="ew")
        
        # Separador antes do PDF
        sep2 = ctk.CTkFrame(inner, height=1, fg_color=Theme.BORDER_LIGHT)
        sep2.pack(fill="x", pady=(3, 5))
        
        # Botão PDF
        btn_pdf = ctk.CTkButton(
            inner,
            text="📄 Exportar PDF",
            fg_color="transparent",
            border_width=1,
            border_color=Theme.ACCENT_PRIMARY,
            text_color=Theme.ACCENT_PRIMARY,
            hover_color=Theme.SELECTED,
            height=28,
            corner_radius=6,
            font=(Theme.FONT_FAMILY, 10, "bold"),
            command=self._on_export
        )
        btn_pdf.pack(fill="x")

    def _create_secondary_button(self, parent, text, command):
        return ctk.CTkButton(
            parent,
            text=text,
            fg_color="transparent",
            border_width=1,
            border_color=Theme.BORDER,
            text_color=Theme.TEXT_SECONDARY,
            hover_color=Theme.HOVER_LIGHT,
            height=28,
            corner_radius=6,
            font=(Theme.FONT_FAMILY, 10, "bold"),
            command=command
        )

    def refresh_saves_dropdown(self, saves_list):
        """Atualiza o dropdown com a lista de saves disponíveis"""
        if saves_list:
            self.saves_dropdown.configure(values=saves_list)
            self.saves_dropdown.set(saves_list[0])
        else:
            self.saves_dropdown.configure(values=["(nenhum)"])
            self.saves_dropdown.set("(nenhum)")
    
    def get_selected_save(self):
        """Retorna o nome do save selecionado no dropdown"""
        val = self.saves_dropdown.get()
        return val if val != "(nenhum)" else None

    # === SETTERS for loading saved config ===
    def set_config(self, config):
        """Preenche os campos da sidebar com uma config carregada"""
        # Room name
        self.entry_room.delete(0, "end")
        self.entry_room.insert(0, config.get("room_name", ""))
        
        # Rows
        rows = config.get("rows", [7, 7, 7, 7])
        for i, slider in enumerate(self.row_vars):
            if i < len(rows):
                slider.set(rows[i])
                self.row_value_labels[i].configure(text=str(rows[i]))
        
        # Furniture
        self.fs_board.set(config.get("board", "Topo"))
        self.fs_door.set(config.get("door", "Esq"))
        self.fs_windows.set(config.get("windows", "Dir"))
    
    def set_students(self, students_dict):
        """Preenche os campos de turmas com dados carregados"""
        if not students_dict:
            return
        
        class_names = list(students_dict.keys())
        class_students = list(students_dict.values())
        
        # Turma 1
        if len(class_names) >= 1:
            self.entry_name_1.delete(0, "end")
            self.entry_name_1.insert(0, class_names[0])
            self.txt_class_1.delete("0.0", "end")
            self.txt_class_1.configure(text_color=Theme.TEXT_PRIMARY)
            if class_students[0]:
                self.txt_class_1.insert("0.0", "\n".join(class_students[0]))
        
        # Turma 2
        if len(class_names) >= 2:
            self.entry_name_2.delete(0, "end")
            self.entry_name_2.insert(0, class_names[1])
            self.txt_class_2.delete("0.0", "end")
            self.txt_class_2.configure(text_color=Theme.TEXT_PRIMARY)
            if class_students[1]:
                self.txt_class_2.insert("0.0", "\n".join(class_students[1]))

    # === GETTERS ===
    def get_config(self):
        return {
            "rows": [int(s.get()) for s in self.row_vars],
            "board": self.fs_board.get(),
            "door": self.fs_door.get(),
            "windows": self.fs_windows.get(),
            "room_name": self.entry_room.get()
        }

    def get_students(self):
        name1 = self.entry_name_1.get().strip() or "TURMA A"
        name2 = self.entry_name_2.get().strip() or "TURMA B"
        
        def get_clean_text(textbox):
            text = textbox.get("0.0", "end").strip()
            if text.startswith("Digite um nome por linha"):
                return []
            return [n.strip() for n in text.split('\n') if n.strip()]
        
        return {
            name1: get_clean_text(self.txt_class_1),
            name2: get_clean_text(self.txt_class_2)
        }

    def on_config_change(self):
        if self.on_change:
            self.on_change(self.get_config())

    # === CALLBACKS ===
    def _on_generate(self):
        if self.on_generate: self.on_generate()
    def _on_save(self):
        if self.on_save: self.on_save()
    def _on_load(self):
        if self.on_load: self.on_load()
    def _on_delete(self):
        if self.on_delete: self.on_delete()
    def _on_export(self):
        if self.on_export: self.on_export()
