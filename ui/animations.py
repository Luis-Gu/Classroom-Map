"""
Módulo de animações e efeitos visuais
Adiciona micro-interações e feedback visual ao aplicativo
"""

import customtkinter as ctk
from .theme import Theme


class AnimationHelper:
    """
    Helper para criar animações e efeitos visuais suaves
    """
    
    @staticmethod
    def fade_in(widget, duration=300, steps=10):
        """
        Efeito de fade in em um widget
        
        Args:
            widget: Widget CustomTkinter
            duration: Duração em ms
            steps: Número de passos da animação
        """
        step_duration = duration // steps
        
        def animate(step=0):
            if step < steps:
                # Calcula opacidade (0.0 a 1.0)
                opacity = step / steps
                # Nota: CustomTkinter não suporta opacity diretamente
                # Mas podemos simular com cores
                widget.after(step_duration, lambda: animate(step + 1))
        
        animate()
    
    @staticmethod
    def shake(widget, distance=5, duration=500):
        """
        Efeito de shake (tremor) em um widget
        Útil para indicar erro ou validação
        
        Args:
            widget: Widget CustomTkinter
            distance: Distância do movimento em pixels
            duration: Duração total em ms
        """
        original_x = widget.winfo_x()
        steps = 8
        step_duration = duration // steps
        
        offsets = [distance, -distance, distance, -distance, 
                   distance//2, -distance//2, distance//4, 0]
        
        def animate(step=0):
            if step < len(offsets):
                new_x = original_x + offsets[step]
                widget.place_configure(x=new_x)
                widget.after(step_duration, lambda: animate(step + 1))
            else:
                widget.place_configure(x=original_x)
        
        animate()
    
    @staticmethod
    def pulse(widget, duration=1000, scale=1.05):
        """
        Efeito de pulso (escala) em um widget
        
        Args:
            widget: Widget CustomTkinter
            duration: Duração de um ciclo completo em ms
            scale: Fator de escala máximo
        """
        # Nota: Difícil implementar scale em CustomTkinter
        # Alternativa: mudar o tamanho temporariamente
        pass
    
    @staticmethod
    def loading_dots(label_widget, base_text="Gerando", duration=400):
        """
        Animação de loading com pontos (...)
        
        Args:
            label_widget: CTkLabel para animar
            base_text: Texto base
            duration: Duração entre mudanças em ms
        
        Returns:
            função para parar a animação
        """
        dots = ["", ".", "..", "..."]
        index = [0]  # Usar lista para mutabilidade
        is_running = [True]
        
        def animate():
            if is_running[0]:
                label_widget.configure(text=f"{base_text}{dots[index[0]]}")
                index[0] = (index[0] + 1) % len(dots)
                label_widget.after(duration, animate)
        
        def stop():
            is_running[0] = False
            label_widget.configure(text=base_text)
        
        animate()
        return stop
    
    @staticmethod
    def smooth_scroll_to(scrollable_frame, target_y, duration=300):
        """
        Scroll suave até uma posição
        
        Args:
            scrollable_frame: CTkScrollableFrame
            target_y: Posição y alvo (0.0 a 1.0)
            duration: Duração em ms
        """
        # CustomTkinter não expõe facilmente o controle de scroll
        # Implementação simplificada
        pass
    
    @staticmethod
    def color_transition(widget, param, start_color, end_color, duration=300, steps=15):
        """
        Transição suave entre duas cores
        
        Args:
            widget: Widget CustomTkinter
            param: Parâmetro a animar (ex: 'fg_color', 'text_color')
            start_color: Cor inicial (hex)
            end_color: Cor final (hex)
            duration: Duração em ms
            steps: Número de passos
        """
        step_duration = duration // steps
        
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def rgb_to_hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(*[int(c) for c in rgb])
        
        start_rgb = hex_to_rgb(start_color)
        end_rgb = hex_to_rgb(end_color)
        
        def animate(step=0):
            if step <= steps:
                # Interpolação linear
                ratio = step / steps
                current_rgb = tuple(
                    start_rgb[i] + (end_rgb[i] - start_rgb[i]) * ratio
                    for i in range(3)
                )
                current_color = rgb_to_hex(current_rgb)
                
                try:
                    widget.configure(**{param: current_color})
                except:
                    pass
                
                widget.after(step_duration, lambda: animate(step + 1))
        
        animate()
    
    @staticmethod
    def hover_lift(widget, lift_amount=2):
        """
        Efeito de elevação ao hover (simula card levantando)
        
        Args:
            widget: Widget CustomTkinter
            lift_amount: Pixels para "levantar"
        """
        original_color = widget.cget("fg_color")
        
        def on_enter(e):
            # Simula elevação com mudança de cor (mais clara)
            widget.configure(fg_color=Theme.SURFACE_ELEVATED)
        
        def on_leave(e):
            widget.configure(fg_color=original_color)
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    @staticmethod
    def button_press_animation(button):
        """
        Animação de clique em botão (feedback tátil visual)
        
        Args:
            button: CTkButton
        """
        original_fg = button.cget("fg_color")
        press_fg = Theme.ACCENT_ACTIVE
        
        def on_press(e):
            button.configure(fg_color=press_fg)
        
        def on_release(e):
            button.after(50, lambda: button.configure(fg_color=original_fg))
        
        button.bind("<Button-1>", on_press)
        button.bind("<ButtonRelease-1>", on_release)


class LoadingOverlay:
    """
    Overlay de loading com spinner
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.overlay = None
        self.spinner_label = None
        self.stop_animation = None
    
    def show(self, text="Processando"):
        """Mostra o overlay de loading"""
        if self.overlay:
            return
        
        # Overlay semi-transparente
        self.overlay = ctk.CTkFrame(
            self.parent,
            fg_color=Theme.PRIMARY_DARK,
            corner_radius=0
        )
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Container central
        center = ctk.CTkFrame(
            self.overlay,
            fg_color=Theme.WHITE_PURE,
            corner_radius=Theme.CORNER_RADIUS_LARGE,
            border_width=1,
            border_color=Theme.BORDER
        )
        center.place(relx=0.5, rely=0.5, anchor="center")
        
        # Texto com animação
        self.spinner_label = ctk.CTkLabel(
            center,
            text=text,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_BODY, "bold"),
            text_color=Theme.TEXT_PRIMARY
        )
        self.spinner_label.pack(padx=60, pady=40)
        
        # Inicia animação
        self.stop_animation = AnimationHelper.loading_dots(
            self.spinner_label, 
            text
        )
    
    def hide(self):
        """Esconde o overlay"""
        if self.stop_animation:
            self.stop_animation()
        
        if self.overlay:
            self.overlay.destroy()
            self.overlay = None
            self.spinner_label = None
            self.stop_animation = None


class ToastNotification:
    """
    Notificação toast (temporária no canto da tela)
    """
    
    @staticmethod
    def show(parent, message, type="info", duration=3000):
        """
        Mostra uma notificação toast
        
        Args:
            parent: Widget pai
            message: Mensagem a exibir
            type: Tipo ('success', 'error', 'warning', 'info')
            duration: Duração em ms
        """
        # Cores por tipo
        colors = {
            "success": Theme.SUCCESS,
            "error": Theme.ERROR,
            "warning": Theme.WARNING,
            "info": Theme.INFO
        }
        
        # Ícones por tipo
        icons = {
            "success": "✓",
            "error": "✕",
            "warning": "⚠",
            "info": "ⓘ"
        }
        
        bg_color = colors.get(type, Theme.INFO)
        icon = icons.get(type, "ⓘ")
        
        # Cria toast
        toast = ctk.CTkFrame(
            parent,
            fg_color=bg_color,
            corner_radius=Theme.CORNER_RADIUS,
            border_width=0
        )
        
        # Label
        label = ctk.CTkLabel(
            toast,
            text=f"{icon}  {message}",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_BODY, "bold"),
            text_color=Theme.TEXT_LIGHT
        )
        label.pack(padx=Theme.PADDING, pady=Theme.PADDING_SMALL)
        
        # Posiciona no topo centro
        toast.place(relx=0.5, rely=0.05, anchor="n")
        
        # Remove após duração
        def fade_out():
            toast.destroy()
        
        parent.after(duration, fade_out)
        
        return toast
