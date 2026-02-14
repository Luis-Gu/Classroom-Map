import customtkinter as ctk
from .theme import Theme

class SidebarRight(ctk.CTkFrame):
    """
    Sidebar Direita: Turmas e Ações
    Compacta e sem scroll
    """
    def __init__(self, master, on_generate=None, on_save=None, on_load=None, on_export=None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_generate = on_generate
        self.on_save = on_save
        self.on_load = on_load
        self.on_export = on_export
        
        self.configure(fg_color=Theme.WHITE_PURE, corner_radius=0)
        
        # Container principal (sem scroll)
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=0, pady=0)

        self._build_classes_section()
        self._build_actions_panel()

    def _build_classes_section(self):
        """Seção de turmas com tabs - compacta"""
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(padx=12, pady=(10, 4), fill="x")
        
        ctk.CTkLabel(
            header_frame,
            text="TURMAS",
            font=(Theme.FONT_FAMILY, 9, "bold"),
            text_color=Theme.TEXT_TERTIARY
        ).pack(anchor="w")
        
        section_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        section_frame.pack(padx=12, pady=(0, 0), fill="both", expand=True)
        
        self.tab_classes = ctk.CTkTabview(
            section_frame,
            anchor="nw",
            segmented_button_selected_color=Theme.WHITE_PURE,
            segmented_button_selected_hover_color=Theme.HOVER_LIGHT,
            segmented_button_unselected_color=Theme.NEUTRAL_SOFT,
            segmented_button_unselected_hover_color=Theme.HOVER_SUBTLE,
            text_color=Theme.TEXT_PRIMARY,
            corner_radius=8,
            border_width=0,
            fg_color=Theme.NEUTRAL_SOFT
        )
        self.tab_classes.pack(fill="both", expand=True)
        
        self.tab_classes.add("Turma 1")
        self.tab_classes.add("Turma 2")
        
        self._build_class_tab(self.tab_classes.tab("Turma 1"), "TURMA A", True)
        self._build_class_tab(self.tab_classes.tab("Turma 2"), "TURMA B", False)

    def _build_class_tab(self, parent, default_name, is_first=True):
        entry = ctk.CTkEntry(
            parent,
            placeholder_text="Nome da Turma",
            border_width=0,
            fg_color=Theme.WHITE_PURE,
            text_color=Theme.TEXT_PRIMARY,
            height=32,
            corner_radius=6,
            font=(Theme.FONT_FAMILY, 11)
        )
        entry.pack(fill="x", padx=8, pady=(8, 4))
        entry.insert(0, default_name)
        
        textbox = ctk.CTkTextbox(
            parent,
            font=(Theme.FONT_FAMILY, 10),
            fg_color=Theme.WHITE_PURE,
            border_width=0,
            corner_radius=6,
            text_color=Theme.TEXT_PRIMARY,
            wrap="word"
        )
        textbox.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        
        placeholder = "Digite um nome por linha\nExemplo:\nJoão Silva\nMaria Santos"
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
        """Painel de ações no fundo - compacto"""
        panel = ctk.CTkFrame(self, fg_color=Theme.WHITE_PURE, corner_radius=0)
        panel.pack(fill="x", side="bottom", padx=0, pady=0)
        
        separator = ctk.CTkFrame(panel, height=1, fg_color=Theme.BORDER)
        separator.pack(fill="x", pady=(0, 10))
        
        inner = ctk.CTkFrame(panel, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=12, pady=(0, 10))
        
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
        
        files_frame = ctk.CTkFrame(inner, fg_color="transparent")
        files_frame.pack(fill="x")
        files_frame.grid_columnconfigure(0, weight=1)
        files_frame.grid_columnconfigure(1, weight=1)
        files_frame.grid_columnconfigure(2, weight=1)
        
        self._create_secondary_button(files_frame, "Salvar", self._on_save).grid(row=0, column=0, padx=(0, 4), sticky="ew")
        self._create_secondary_button(files_frame, "Carregar", self._on_load).grid(row=0, column=1, padx=2, sticky="ew")
        
        btn_pdf = ctk.CTkButton(
            files_frame,
            text="PDF",
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
        btn_pdf.grid(row=0, column=2, padx=(4, 0), sticky="ew")

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

    def _on_generate(self):
        if self.on_generate: self.on_generate()
    def _on_save(self):
        if self.on_save: self.on_save()
    def _on_load(self):
        if self.on_load: self.on_load()
    def _on_export(self):
        if self.on_export: self.on_export()
