import customtkinter as ctk
from .theme import Theme

class Sidebar(ctk.CTkFrame):
    """
    Sidebar moderna com design minimalista e responsivo
    Inspiração: Notion, Canva, Figma
    """
    def __init__(self, master, on_change=None, on_generate=None, 
                 on_save=None, on_load=None, on_export=None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_change = on_change
        self.on_generate = on_generate
        self.on_save = on_save
        self.on_load = on_load
        self.on_export = on_export
        
        # Mapeamento de Ícones
        self.ICON_MAP = {"Nenhum": "✕", "Topo": "⬆", "Esq": "⬅", "Dir": "➡", "Fundo": "⬇"}
        self.REVERSE_ICON_MAP = {v: k for k, v in self.ICON_MAP.items()}
        
        # Configuração com cores do novo tema
        self.configure(fg_color=Theme.WHITE_PURE, corner_radius=0)
        
        # Variáveis para animações hover
        self.hover_widgets = []

        
        # Variáveis para animações hover
        self.hover_widgets = []

        # Container principal com scroll
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

        # === PAINEL DE AÇÕES (FIXO NO FUNDO) ===
        self._build_actions_panel()
    
    def _build_header(self):
        """Cabeçalho moderno com título grande e subtítulo"""
        header_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        header_frame.pack(padx=Theme.PADDING, pady=(Theme.PADDING, Theme.PADDING_SMALL), fill="x")
        
        # Título principal - grande e bold
        title = ctk.CTkLabel(
            header_frame,
            text="Gerador de Mapa",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_TITLE, "bold"),
            text_color=Theme.TEXT_PRIMARY,
            anchor="w"
        )
        title.pack(anchor="w", pady=(0, 4))
        
        # Subtítulo descritivo
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Configure a disposição da sala de aula",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            text_color=Theme.TEXT_SECONDARY,
            anchor="w"
        )
        subtitle.pack(anchor="w")
    
    def _build_room_section(self):
        """Seção do nome da sala"""
        section_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        section_frame.pack(padx=Theme.PADDING, pady=(Theme.PADDING_SMALL, 0), fill="x")
        
        # Label da seção
        label = ctk.CTkLabel(
            section_frame,
            text="NOME DA SALA",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_TINY, "bold"),
            text_color=Theme.TEXT_TERTIARY,
            anchor="w"
        )
        label.pack(anchor="w", pady=(0, Theme.PADDING_TINY))
        
        # Input moderno
        self.entry_room = ctk.CTkEntry(
            section_frame,
            placeholder_text="Ex: Sala 1A, Laboratório 3...",
            border_width=1,
            border_color=Theme.BORDER,
            fg_color=Theme.WHITE_PURE,
            text_color=Theme.TEXT_PRIMARY,
            placeholder_text_color=Theme.TEXT_TERTIARY,
            height=36,
            corner_radius=Theme.CORNER_RADIUS_SMALL,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_BODY)
        )
        self.entry_room.pack(fill="x")
        
        # Hover effect
        self._add_hover_effect(self.entry_room, Theme.BORDER, Theme.PRIMARY_DARK)
    
    def _build_rows_section(self):
        """Seção de configuração das filas com sliders modernos"""
        self._build_section_header("LAYOUT DAS FILAS", "Defina quantas carteiras por fila")
        
        section_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        section_frame.pack(padx=Theme.PADDING, pady=(Theme.PADDING_TINY, 0), fill="x")
        
        self.row_vars = []
        self.row_value_labels = []
        
        for i in range(4):
            # Container para cada fila
            row_container = ctk.CTkFrame(section_frame, fg_color="transparent")
            row_container.pack(fill="x", pady=Theme.PADDING_TINY)
            
            # Label e valor no topo
            top_frame = ctk.CTkFrame(row_container, fg_color="transparent")
            top_frame.pack(fill="x", pady=(0, 6))
            
            ctk.CTkLabel(
                top_frame,
                text=f"Fila {i+1}",
                font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_LABEL, "bold"),
                text_color=Theme.TEXT_PRIMARY,
                anchor="w"
            ).pack(side="left")
            
            val_lbl = ctk.CTkLabel(
                top_frame,
                text="7",
                font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_LABEL, "bold"),
                text_color=Theme.ACCENT_PRIMARY,
                anchor="e"
            )
            val_lbl.pack(side="right")
            self.row_value_labels.append(val_lbl)
            
            # Slider moderno e fino
            slider = ctk.CTkSlider(
                row_container,
                from_=1,
                to=15,
                number_of_steps=14,
                button_color=Theme.ACCENT_PRIMARY,
                button_hover_color=Theme.ACCENT_HOVER,
                progress_color=Theme.ACCENT_PRIMARY,
                fg_color=Theme.BORDER_LIGHT,
                height=14
            )
            slider.set(7)
            slider.pack(fill="x")
            
            # Bind para atualizar o label
            slider.configure(command=lambda v, idx=i: self._update_slider_value(idx, v))
            self.row_vars.append(slider)
    
    def _update_slider_value(self, index, value):
        """Atualiza o valor exibido do slider"""
        self.row_value_labels[index].configure(text=str(int(value)))
        self.on_config_change()
    
    def _build_furniture_section(self):
        """Seção de mobília com design moderno e profissional"""
        self._build_section_header("MOBÍLIA DA SALA", "Posicione os elementos na sala")
        
        # Container principal com fundo sutil
        section_frame = ctk.CTkFrame(
            self.scroll, 
            fg_color=Theme.NEUTRAL_SOFT,
            corner_radius=Theme.CORNER_RADIUS
        )
        section_frame.pack(padx=Theme.PADDING, pady=(Theme.PADDING_TINY, 0), fill="x")
        
        # Padding interno
        inner_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        inner_frame.pack(fill="x", padx=Theme.PADDING_SMALL, pady=Theme.PADDING_SMALL)
        
        # Quadro
        self._build_furniture_selector(inner_frame, "📋 Quadro", "board", default="Topo", icon_emoji="📋")
        
        # Porta
        self._build_furniture_selector(inner_frame, "🚪 Porta", "door", default="Esq", icon_emoji="🚪")
        
        # Janelas
        self._build_furniture_selector(inner_frame, "🪟 Janelas", "windows", default="Dir", icon_emoji="🪟")
    
    def _build_furniture_selector(self, parent, label_text, key, default="Nenhum", icon_emoji=""):
        """Cria um seletor de mobília moderno com card estilizado"""
        # Card container com fundo branco e sombra sutil
        card = ctk.CTkFrame(
            parent, 
            fg_color=Theme.WHITE_PURE,
            corner_radius=Theme.CORNER_RADIUS_SMALL,
            border_width=1,
            border_color=Theme.BORDER_LIGHT
        )
        card.pack(fill="x", pady=(0, Theme.PADDING_TINY))
        
        # Inner padding
        card_inner = ctk.CTkFrame(card, fg_color="transparent")
        card_inner.pack(fill="x", padx=Theme.PADDING_SMALL, pady=Theme.PADDING_SMALL)
        
        # Header row com label
        header_row = ctk.CTkFrame(card_inner, fg_color="transparent")
        header_row.pack(fill="x", pady=(0, Theme.PADDING_TINY))
        
        ctk.CTkLabel(
            header_row,
            text=label_text,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_BODY, "bold"),
            text_color=Theme.TEXT_PRIMARY,
            anchor="w"
        ).pack(side="left")
        
        # Container dos botões de direção
        buttons_frame = ctk.CTkFrame(
            card_inner, 
            fg_color=Theme.NEUTRAL_SOFT,
            corner_radius=Theme.CORNER_RADIUS_SMALL
        )
        buttons_frame.pack(fill="x")
        
        # Grid para os botões - responsivo
        for i in range(5):
            buttons_frame.grid_columnconfigure(i, weight=1, uniform="btn")
        buttons_frame.grid_rowconfigure(0, weight=1)
        
        # Botões de direção com design moderno
        direction_options = [
            ("✕", "Nenhum", "Remover"),
            ("↑", "Topo", "Parte superior"),
            ("←", "Esq", "Lado esquerdo"),
            ("→", "Dir", "Lado direito"),
            ("↓", "Fundo", "Parte inferior")
        ]
        
        btn_refs = {}
        for idx, (icon, value, tooltip) in enumerate(direction_options):
            is_selected = (value == default)
            
            btn = ctk.CTkButton(
                buttons_frame,
                text=icon,
                width=36,
                height=36,
                corner_radius=Theme.CORNER_RADIUS_SMALL,
                font=(Theme.FONT_FAMILY, 18, "bold"),
                border_width=2 if is_selected else 0,
                border_color=Theme.ACCENT_PRIMARY if is_selected else "transparent",
                fg_color=Theme.WHITE_PURE if is_selected else "transparent",
                hover_color=Theme.HOVER_LIGHT,
                text_color=Theme.ACCENT_PRIMARY if is_selected else Theme.TEXT_SECONDARY,
                command=lambda v=value, k=key: self._on_furniture_select(k, v),
                cursor="hand2"
            )
            btn.grid(row=0, column=idx, padx=2, pady=4, sticky="ew")
            btn_refs[value] = btn
            
            # Hover effect
            self._add_furniture_btn_hover(btn, is_selected)
        
        # Armazenar referências dos botões
        if key == "board":
            self.furniture_btns_board = btn_refs
            self.furniture_current_board = default
        elif key == "door":
            self.furniture_btns_door = btn_refs
            self.furniture_current_door = default
        elif key == "windows":
            self.furniture_btns_windows = btn_refs
            self.furniture_current_windows = default
        
        # Hover effect no card
        self._add_card_hover(card)
    
    def _add_furniture_btn_hover(self, btn, is_selected):
        """Adiciona efeito hover sutil aos botões de mobília"""
        def on_enter(e):
            if not is_selected:
                btn.configure(fg_color=Theme.HOVER_SUBTLE)
        
        def on_leave(e):
            if not is_selected:
                btn.configure(fg_color="transparent")
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    def _add_card_hover(self, card):
        """Adiciona efeito hover ao card de mobília"""
        def on_enter(e):
            card.configure(border_color=Theme.BORDER)
        
        def on_leave(e):
            card.configure(border_color=Theme.BORDER_LIGHT)
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
    
    def _on_furniture_select(self, key, value):
        """Callback quando uma opção de mobília é selecionada"""
        # Obter referências corretas
        if key == "board":
            btns = self.furniture_btns_board
            old_value = self.furniture_current_board
            self.furniture_current_board = value
        elif key == "door":
            btns = self.furniture_btns_door
            old_value = self.furniture_current_door
            self.furniture_current_door = value
        elif key == "windows":
            btns = self.furniture_btns_windows
            old_value = self.furniture_current_windows
            self.furniture_current_windows = value
        
        # Atualizar visual dos botões
        for val, btn in btns.items():
            if val == value:
                btn.configure(
                    fg_color=Theme.WHITE_PURE,
                    text_color=Theme.ACCENT_PRIMARY,
                    border_width=2,
                    border_color=Theme.ACCENT_PRIMARY
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=Theme.TEXT_SECONDARY,
                    border_width=0,
                    border_color="transparent"
                )
        
        # Verificar conflitos (mesma posição para diferentes elementos)
        self._check_furniture_conflicts(key, value)
        
        self.on_config_change()
    
    def _check_furniture_conflicts(self, source, value):
        """Garante que cada posição tenha apenas um elemento"""
        if value == "Nenhum":
            return
        
        items = {
            "board": (getattr(self, 'furniture_btns_board', {}), 'furniture_current_board'),
            "door": (getattr(self, 'furniture_btns_door', {}), 'furniture_current_door'),
            "windows": (getattr(self, 'furniture_btns_windows', {}), 'furniture_current_windows')
        }
        
        for key, (btns, current_attr) in items.items():
            if key != source and getattr(self, current_attr, None) == value:
                # Resetar para Nenhum
                setattr(self, current_attr, "Nenhum")
                for val, btn in btns.items():
                    if val == "Nenhum":
                        btn.configure(
                            fg_color=Theme.WHITE_PURE,
                            text_color=Theme.ACCENT_PRIMARY,
                            border_width=2,
                            border_color=Theme.ACCENT_PRIMARY
                        )
                    else:
                        btn.configure(
                            fg_color="transparent",
                            text_color=Theme.TEXT_SECONDARY,
                            border_width=0,
                            border_color="transparent"
                        )
    
    def _build_classes_section(self):
        """Seção de turmas com tabs modernos"""
        self._build_section_header("TURMAS", "Liste os alunos de cada turma")
        
        section_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        section_frame.pack(padx=Theme.PADDING, pady=(Theme.PADDING_TINY, 0), fill="x")
        
        # Tabview moderno
        self.tab_classes = ctk.CTkTabview(
            section_frame,
            height=240,
            anchor="nw",
            segmented_button_selected_color=Theme.WHITE_PURE,
            segmented_button_selected_hover_color=Theme.HOVER_LIGHT,
            segmented_button_unselected_color=Theme.NEUTRAL_SOFT,
            segmented_button_unselected_hover_color=Theme.HOVER_SUBTLE,
            text_color=Theme.TEXT_PRIMARY,
            corner_radius=Theme.CORNER_RADIUS,
            border_width=0,
            fg_color=Theme.NEUTRAL_SOFT
        )
        self.tab_classes.pack(fill="both", expand=True)
        
        # Adicionar tabs
        self.tab_classes.add("Turma 1")
        self.tab_classes.add("Turma 2")
        
        # Turma 1
        self._build_class_tab(
            self.tab_classes.tab("Turma 1"),
            "TURMA A",
            is_first=True
        )
        
        # Turma 2
        self._build_class_tab(
            self.tab_classes.tab("Turma 2"),
            "TURMA B",
            is_first=False
        )
    
    def _build_class_tab(self, parent, default_name, is_first=True):
        """Constrói o conteúdo de uma tab de turma"""
        # Input do nome da turma
        entry = ctk.CTkEntry(
            parent,
            placeholder_text="Nome da Turma",
            border_width=1,
            border_color=Theme.BORDER,
            fg_color=Theme.SURFACE_ELEVATED,
            text_color=Theme.TEXT_PRIMARY,
            height=38,
            corner_radius=Theme.CORNER_RADIUS_SMALL,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_BODY)
        )
        entry.pack(fill="x", padx=Theme.PADDING_SMALL, pady=(Theme.PADDING_SMALL, Theme.PADDING_TINY))
        entry.insert(0, default_name)
        
        # Textbox para lista de alunos
        textbox = ctk.CTkTextbox(
            parent,
            font=(Theme.FONT_FAMILY_MONO, Theme.FONT_SIZE_SMALL),
            fg_color=Theme.SURFACE_ELEVATED,
            border_color=Theme.BORDER,
            border_width=1,
            corner_radius=Theme.CORNER_RADIUS_SMALL,
            text_color=Theme.TEXT_PRIMARY,
            wrap="word"
        )
        textbox.pack(
            fill="both",
            expand=True,
            padx=Theme.PADDING_SMALL,
            pady=(0, Theme.PADDING_SMALL)
        )
        
        # Placeholder text
        placeholder = "Digite um nome por linha\nExemplo:\nJoão Silva\nMaria Santos\nPedro Oliveira"
        textbox.insert("0.0", placeholder)
        textbox.configure(text_color=Theme.TEXT_TERTIARY)
        
        # Efeito placeholder
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
        
        # Salvar referências
        if is_first:
            self.entry_name_1 = entry
            self.txt_class_1 = textbox
        else:
            self.entry_name_2 = entry
            self.txt_class_2 = textbox
    
    def _build_actions_panel(self):
        """Painel de ações fixo no fundo com botão destaque"""
        panel = ctk.CTkFrame(
            self,
            fg_color=Theme.WHITE_PURE,
            height=180,
            corner_radius=0
        )
        panel.pack(fill="x", side="bottom", padx=0, pady=0)
        
        # Linha separadora sutil
        separator = ctk.CTkFrame(panel, height=1, fg_color=Theme.BORDER)
        separator.pack(fill="x", pady=(0, Theme.PADDING))
        
        # Container interno com padding
        inner = ctk.CTkFrame(panel, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=Theme.PADDING, pady=(0, Theme.PADDING))
        
        # BOTÃO PRINCIPAL - GERAR MAPA (Elegante e destacado)
        self.btn_generate = ctk.CTkButton(
            inner,
            text="GERAR MAPA",
            fg_color=Theme.ACCENT_PRIMARY,
            hover_color=Theme.ACCENT_HOVER,
            height=44,
            corner_radius=Theme.CORNER_RADIUS_PILL,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_BUTTON, "bold"),
            text_color=Theme.TEXT_LIGHT,
            command=self._on_generate,
            cursor="hand2"
        )
        self.btn_generate.pack(fill="x", pady=(0, Theme.PADDING_SMALL))
        
        # Animação hover para o botão principal
        self._add_button_hover_animation(self.btn_generate)
        
        # Botões secundários (arquivo)
        files_frame = ctk.CTkFrame(inner, fg_color="transparent")
        files_frame.pack(fill="x")
        
        # Grid para botões secundários
        files_frame.grid_columnconfigure(0, weight=1)
        files_frame.grid_columnconfigure(1, weight=1)
        files_frame.grid_columnconfigure(2, weight=1)
        
        # Botão Salvar
        btn_save = self._create_secondary_button(
            files_frame,
            text="Salvar",
            command=self._on_save
        )
        btn_save.grid(row=0, column=0, padx=(0, 6), sticky="ew")
        
        # Botão Carregar
        btn_load = self._create_secondary_button(
            files_frame,
            text="Carregar",
            command=self._on_load
        )
        btn_load.grid(row=0, column=1, padx=3, sticky="ew")
        
        # Botão PDF (com destaque)
        btn_pdf = ctk.CTkButton(
            files_frame,
            text="PDF",
            fg_color="transparent",
            border_width=2,
            border_color=Theme.ACCENT_PRIMARY,
            text_color=Theme.ACCENT_PRIMARY,
            hover_color=Theme.SELECTED,
            height=32,
            corner_radius=Theme.CORNER_RADIUS_SMALL,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL, "bold"),
            command=self._on_export,
            cursor="hand2"
        )
        btn_pdf.grid(row=0, column=2, padx=(6, 0), sticky="ew")
    
    def _create_secondary_button(self, parent, text, command):
        """Cria um botão secundário com estilo outline"""
        btn = ctk.CTkButton(
            parent,
            text=text,
            fg_color="transparent",
            border_width=1,
            border_color=Theme.BORDER,
            text_color=Theme.TEXT_SECONDARY,
            hover_color=Theme.HOVER_LIGHT,
            height=32,
            corner_radius=Theme.CORNER_RADIUS_SMALL,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL, "bold"),
            command=command,
            cursor="hand2"
        )
        return btn
    
    def _build_section_header(self, title, subtitle=None):
        """Cria um cabeçalho de seção consistente"""
        header_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        header_frame.pack(
            padx=Theme.PADDING,
            pady=(Theme.PADDING, Theme.PADDING_TINY),
            fill="x"
        )
        
        # Título da seção
        title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_TINY, "bold"),
            text_color=Theme.TEXT_TERTIARY,
            anchor="w"
        )
        title_label.pack(anchor="w")
        
        # Subtítulo opcional
        if subtitle:
            subtitle_label = ctk.CTkLabel(
                header_frame,
                text=subtitle,
                font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_TINY),
                text_color=Theme.TEXT_TERTIARY,
                anchor="w"
            )
            subtitle_label.pack(anchor="w", pady=(2, 0))
    
    def _add_hover_effect(self, widget, normal_color, hover_color):
        """Adiciona efeito hover a um widget"""
        def on_enter(e):
            widget.configure(border_color=hover_color)
        
        def on_leave(e):
            widget.configure(border_color=normal_color)
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def _add_button_hover_animation(self, button):
        """Adiciona animação sutil ao hover do botão"""
        original_fg = button.cget("fg_color")
        hover_fg = button.cget("hover_color")
        
        def on_enter(e):
            # Animação sutil: poderia expandir levemente
            button.configure(cursor="hand2")
        
        def on_leave(e):
            button.configure(cursor="")
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    # === MÉTODOS DE DADOS E CALLBACKS ===
    
    def get_config(self):
        """Retorna a configuração atual da sala"""
        return {
            "rows": [int(s.get()) for s in self.row_vars],
            "board": getattr(self, 'furniture_current_board', "Topo"),
            "door": getattr(self, 'furniture_current_door', "Esq"),
            "windows": getattr(self, 'furniture_current_windows', "Dir"),
            "room_name": self.entry_room.get()
        }
    
    def get_students(self):
        """Retorna os alunos organizados por turma"""
        name1 = self.entry_name_1.get().strip() or "TURMA A"
        name2 = self.entry_name_2.get().strip() or "TURMA B"
        
        # Função auxiliar para limpar placeholder
        def get_clean_text(textbox, placeholder):
            text = textbox.get("0.0", "end").strip()
            # Remove placeholder se ainda estiver lá
            if text.startswith("Digite um nome por linha"):
                return []
            return [n.strip() for n in text.split('\n') if n.strip()]
        
        placeholder = "Digite um nome por linha\nExemplo:\nJoão Silva\nMaria Santos\nPedro Oliveira"
        
        return {
            name1: get_clean_text(self.txt_class_1, placeholder),
            name2: get_clean_text(self.txt_class_2, placeholder)
        }
    
    def on_config_change(self, *args):
        """Callback quando a configuração muda"""
        if self.on_change:
            self.on_change(self.get_config())
    
    # Callbacks dos botões
    def _on_generate(self):
        if self.on_generate:
            self.on_generate()
    
    def _on_save(self):
        if self.on_save:
            self.on_save()
    
    def _on_load(self):
        if self.on_load:
            self.on_load()
    
    def _on_export(self):
        if self.on_export:
            self.on_export()

