import customtkinter as ctk
from .theme import Theme

class FurnitureSelector(ctk.CTkFrame):
    """
    Seletor de mobília compacto com badge indicador
    """
    def __init__(self, master, label_text, value_key, current_value, command=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.command = command
        self.value_key = value_key
        self.buttons = {}
        self.current_val = current_value
        
        # Header com label + badge
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 4))
        
        ctk.CTkLabel(
            header,
            text=label_text,
            font=(Theme.FONT_FAMILY, 12, "bold"),
            text_color=Theme.TEXT_PRIMARY
        ).pack(side="left")
        
        # Badge indicador
        self.badge_frame = ctk.CTkFrame(
            header,
            fg_color=Theme.ACCENT_SOFT,
            corner_radius=8
        )
        self.badge_frame.pack(side="right")
        
        self.badge_label = ctk.CTkLabel(
            self.badge_frame,
            text=self._get_label(current_value),
            font=(Theme.FONT_FAMILY, 9),
            text_color=Theme.ACCENT_PRIMARY
        )
        self.badge_label.pack(padx=6, pady=1)
        
        # Container dos botões - compacto
        buttons_frame = ctk.CTkFrame(
            self,
            fg_color=Theme.NEUTRAL_SOFT,
            corner_radius=6,
            height=32
        )
        buttons_frame.pack(fill="x")
        buttons_frame.pack_propagate(False)
        
        for i in range(5):
            buttons_frame.grid_columnconfigure(i, weight=1)
        buttons_frame.grid_rowconfigure(0, weight=1)
        
        # Ícones profissionais (setas finas)
        self.options = [
            ("×", "Nenhum"),
            ("↑", "Topo"),
            ("←", "Esq"),
            ("→", "Dir"),
            ("↓", "Fundo")
        ]
        
        for idx, (icon, val) in enumerate(self.options):
            self._create_button(buttons_frame, idx, icon, val)
        
        self.set(self.current_val)

    def _get_label(self, value):
        """Retorna texto do badge"""
        labels = {
            "Nenhum": "Nenhum",
            "Topo": "Superior",
            "Esq": "Esquerda",
            "Dir": "Direita",
            "Fundo": "Inferior"
        }
        return labels.get(value, value)

    def _create_button(self, parent, idx, icon, value):
        is_selected = (value == self.current_val)
        
        btn = ctk.CTkButton(
            parent,
            text=icon,
            width=28,
            height=26,
            corner_radius=4,
            font=(Theme.FONT_FAMILY, 13, "bold"),
            border_width=1 if is_selected else 0,
            border_color=Theme.ACCENT_PRIMARY,
            fg_color=Theme.WHITE_PURE if is_selected else Theme.NEUTRAL_SOFT,
            hover_color=Theme.HOVER_LIGHT,
            text_color=Theme.ACCENT_PRIMARY if is_selected else Theme.TEXT_SECONDARY,
            command=lambda v=value: self._on_select(v)
        )
        btn.grid(row=0, column=idx, padx=1, pady=3, sticky="nsew")
        self.buttons[value] = btn

    def _on_select(self, value):
        self.set(value)
        if self.command:
            self.command(self.value_key, value)

    def set(self, value):
        self.current_val = value
        self.badge_label.configure(text=self._get_label(value))
        
        for val, btn in self.buttons.items():
            if val == value:
                btn.configure(
                    fg_color=Theme.WHITE_PURE,
                    text_color=Theme.ACCENT_PRIMARY,
                    border_width=1
                )
            else:
                btn.configure(
                    fg_color=Theme.NEUTRAL_SOFT,
                    text_color=Theme.TEXT_SECONDARY,
                    border_width=0
                )

    def get(self):
        return self.current_val
