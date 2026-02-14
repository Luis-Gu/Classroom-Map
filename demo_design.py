"""
Script de demonstração do novo design
Mostra as cores e componentes principais
"""

import customtkinter as ctk
from ui.theme import Theme


def show_color_palette():
    """Mostra a paleta de cores do novo tema"""
    print("\n" + "="*60)
    print("🎨 PALETA DE CORES - CLASSROOM MAP GENERATOR")
    print("="*60)
    
    colors = {
        "🔵 Azul Escuro Principal": Theme.PRIMARY_DARK,
        "⚪ Cinza Neutro": Theme.GRAY_NEUTRAL,
        "📄 Fundo Claro": Theme.BACKGROUND_LIGHT,
        "⬜ Branco Puro": Theme.WHITE_PURE,
        "🟦 Texto Principal": Theme.TEXT_PRIMARY,
        "🔘 Texto Secundário": Theme.TEXT_SECONDARY,
        "🔹 Hover": Theme.ACCENT_HOVER,
        "✅ Sucesso": Theme.SUCCESS,
        "❌ Erro": Theme.ERROR,
        "⚠️  Aviso": Theme.WARNING,
        "ℹ️  Info": Theme.INFO,
    }
    
    for name, color in colors.items():
        print(f"\n{name:30} {color}")
    
    print("\n" + "="*60)


def show_typography():
    """Mostra a hierarquia tipográfica"""
    print("\n" + "="*60)
    print("📝 TIPOGRAFIA")
    print("="*60)
    
    fonts = {
        "Título Principal": (Theme.FONT_SIZE_TITLE, "bold"),
        "Cabeçalho": (Theme.FONT_SIZE_HEADING, "bold"),
        "Subcabeçalho": (Theme.FONT_SIZE_SUBHEADING, "bold"),
        "Corpo": (Theme.FONT_SIZE_BODY, "regular"),
        "Label": (Theme.FONT_SIZE_LABEL, "medium"),
        "Botão": (Theme.FONT_SIZE_BUTTON, "semibold"),
        "Pequeno": (Theme.FONT_SIZE_SMALL, "regular"),
    }
    
    print(f"\nFonte: {Theme.FONT_FAMILY}")
    print(f"Fonte Monoespaçada: {Theme.FONT_FAMILY_MONO}\n")
    
    for name, (size, weight) in fonts.items():
        print(f"{name:20} {size}px {weight}")
    
    print("\n" + "="*60)


def show_spacing():
    """Mostra o sistema de espaçamento"""
    print("\n" + "="*60)
    print("📏 ESPAÇAMENTO")
    print("="*60)
    
    spacing = {
        "Grande": Theme.PADDING_LARGE,
        "Padrão": Theme.PADDING,
        "Pequeno": Theme.PADDING_SMALL,
        "Mínimo": Theme.PADDING_TINY,
    }
    
    for name, value in spacing.items():
        print(f"\n{name:20} {value}px")
    
    print("\n" + "="*60)


def show_borders():
    """Mostra os raios de borda"""
    print("\n" + "="*60)
    print("⭕ BORDAS ARREDONDADAS")
    print("="*60)
    
    borders = {
        "Grande (Cards)": Theme.CORNER_RADIUS_LARGE,
        "Padrão": Theme.CORNER_RADIUS,
        "Pequeno (Inputs)": Theme.CORNER_RADIUS_SMALL,
        "Pill (Botões)": Theme.CORNER_RADIUS_PILL,
    }
    
    for name, value in borders.items():
        print(f"\n{name:25} {value}px")
    
    print("\n" + "="*60)


def show_components_info():
    """Mostra informações sobre os componentes"""
    print("\n" + "="*60)
    print("🧩 COMPONENTES PRINCIPAIS")
    print("="*60)
    
    print("""
1. SIDEBAR (Painel Esquerdo)
   - Largura: 380px (fixa)
   - Fundo: Branco Puro
   - Componentes:
     * Cabeçalho com título grande
     * Input de nome da sala
     * 4 Sliders de filas
     * 3 Segmented buttons (mobília)
     * Tabview com 2 turmas
     * Painel de ações fixo no fundo

2. VISUALIZADOR (Painel Direito)
   - Fundo: Cinza Claro
   - Card central branco
   - Componentes:
     * Cabeçalho do preview
     * Canvas para desenho
     * Estado vazio amigável
     * Carteiras com sombras
     * Mobília estilizada

3. BOTÃO PRINCIPAL
   - Texto: "GERAR MAPA"
   - Altura: 56px
   - Cor: Azul Escuro
   - Bordas: Pill (30px)
   - Hover: Azul mais claro

4. ANIMAÇÕES
   - Toast Notifications (4 tipos)
   - Loading Overlay
   - Hover Effects
   - Feedback Visual
    """)
    
    print("="*60)


def create_demo_window():
    """Cria uma janela de demonstração das cores"""
    root = ctk.CTk()
    root.title("🎨 Demonstração do Novo Design")
    root.geometry("800x600")
    root.configure(fg_color=Theme.BACKGROUND_LIGHT)
    
    # Frame principal
    main = ctk.CTkFrame(root, fg_color="transparent")
    main.pack(fill="both", expand=True, padx=40, pady=40)
    
    # Título
    title = ctk.CTkLabel(
        main,
        text="Classroom Map Generator",
        font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_TITLE, "bold"),
        text_color=Theme.TEXT_PRIMARY
    )
    title.pack(pady=(0, 10))
    
    # Subtítulo
    subtitle = ctk.CTkLabel(
        main,
        text="Novo Design Moderno e Profissional",
        font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_BODY),
        text_color=Theme.TEXT_SECONDARY
    )
    subtitle.pack(pady=(0, 30))
    
    # Card com paleta de cores
    card = ctk.CTkFrame(
        main,
        fg_color=Theme.WHITE_PURE,
        corner_radius=Theme.CORNER_RADIUS_LARGE,
        border_width=1,
        border_color=Theme.BORDER
    )
    card.pack(fill="both", expand=True, pady=10)
    
    # Grid de cores
    colors_frame = ctk.CTkFrame(card, fg_color="transparent")
    colors_frame.pack(fill="both", expand=True, padx=30, pady=30)
    
    colors = [
        ("Azul Escuro", Theme.PRIMARY_DARK),
        ("Cinza Neutro", Theme.GRAY_NEUTRAL),
        ("Fundo Claro", Theme.BACKGROUND_LIGHT),
        ("Branco Puro", Theme.WHITE_PURE),
        ("Sucesso", Theme.SUCCESS),
        ("Erro", Theme.ERROR),
        ("Aviso", Theme.WARNING),
        ("Info", Theme.INFO),
    ]
    
    for i, (name, color) in enumerate(colors):
        row = i // 4
        col = i % 4
        
        color_container = ctk.CTkFrame(colors_frame, fg_color="transparent")
        color_container.grid(row=row, column=col, padx=10, pady=10)
        
        # Quadrado de cor
        color_box = ctk.CTkFrame(
            color_container,
            width=100,
            height=100,
            fg_color=color,
            corner_radius=Theme.CORNER_RADIUS
        )
        color_box.pack()
        color_box.pack_propagate(False)
        
        # Nome e código
        ctk.CTkLabel(
            color_container,
            text=name,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL, "bold"),
            text_color=Theme.TEXT_PRIMARY
        ).pack(pady=(5, 0))
        
        ctk.CTkLabel(
            color_container,
            text=color,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_TINY),
            text_color=Theme.TEXT_TERTIARY
        ).pack()
    
    # Botão de exemplo
    btn = ctk.CTkButton(
        main,
        text="GERAR MAPA",
        font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_BUTTON, "bold"),
        fg_color=Theme.ACCENT_PRIMARY,
        hover_color=Theme.ACCENT_HOVER,
        height=56,
        corner_radius=Theme.CORNER_RADIUS_PILL,
        cursor="hand2"
    )
    btn.pack(pady=20)
    
    root.mainloop()


if __name__ == "__main__":
    print("\n" + "🎨 "*20)
    print("NOVO DESIGN - CLASSROOM MAP GENERATOR")
    print("🎨 "*20)
    
    show_color_palette()
    show_typography()
    show_spacing()
    show_borders()
    show_components_info()
    
    print("\n" + "="*60)
    print("💡 Dica: Execute o main.py para ver o aplicativo!")
    print("="*60 + "\n")
    
    # Pergunta se quer ver a demo visual
    try:
        response = input("\nDeseja abrir a janela de demonstração? (s/n): ")
        if response.lower() in ['s', 'sim', 'y', 'yes']:
            create_demo_window()
    except:
        pass
