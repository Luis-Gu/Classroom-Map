

class Theme:
    """
    Tema moderno e minimalista inspirado em Notion/Canva/Linear
    Paleta de cores refinada para identidade visual profissional
    """
    
    # Cores Principais
    PRIMARY_DARK = "#1E3A5F"       # Azul escuro principal (mais vibrante)
    PRIMARY_VIBRANT = "#3B82F6"    # Azul vibrante para destaque
    GRAY_NEUTRAL = "#64748B"       # Cinza azulado neutro
    BACKGROUND_LIGHT = "#F5F7FA"   # Fundo claro (levemente mais quente)
    WHITE_PURE = "#FFFFFF"         # Branco puro
    
    # Variações para UI
    SURFACE = "#FFFFFF"            # Cards e superfícies
    SURFACE_ELEVATED = "#FFFFFF"   # Superfícies elevadas (brancas)
    BORDER = "#E2E8F0"             # Bordas muito sutis
    BORDER_LIGHT = "#F1F5F9"       # Bordas quase invisíveis
    
    # Textos
    TEXT_PRIMARY = "#1E293B"       # Texto principal (escuro mas não preto)
    TEXT_SECONDARY = "#64748B"     # Texto secundário (cinza médio)
    TEXT_TERTIARY = "#94A3B8"      # Texto terciário (mais suave)
    TEXT_LIGHT = "#FFFFFF"         # Texto claro
    
    # Acentos e Estados
    ACCENT_PRIMARY = "#3B82F6"     # Azul vibrante como destaque principal
    ACCENT_HOVER = "#2563EB"       # Hover sobre elementos azuis
    ACCENT_ACTIVE = "#1D4ED8"      # Estado ativo/pressionado
    
    # Estados de Interação
    HOVER_LIGHT = "#F8FAFC"        # Hover em superfícies claras
    HOVER_SUBTLE = "#F1F5F9"       # Hover mais pronunciado
    SELECTED = "#DBEAFE"           # Estado selecionado (azul suave)
    
    # Cores de Turmas (para carteiras e badges)
    CLASS_A_COLOR = "#3B82F6"      # Turma A - Azul vibrante
    CLASS_A_BG = "#DBEAFE"         # Badge background Turma A
    CLASS_B_COLOR = "#8B5CF6"      # Turma B - Roxo vibrante
    CLASS_B_BG = "#EDE9FE"         # Badge background Turma B
    
    # Elementos da Sala
    DESK_FILL = "#FFFFFF"          # Fundo das carteiras
    DESK_BORDER = "#CBD5E0"        # Borda das carteiras (mais suave)
    DESK_SHADOW = "#E2E8F0"        # Sombra simulada
    CHAIR_FILL = "#F7F8FA"         # Cadeira (fundo claro)
    
    # Mobília
    FURNITURE_FILL = "#F8FAFC"     # Fundo mobília (mais claro)
    FURNITURE_BORDER = "#E2E8F0"   # Borda mobília (muito sutil)
    FURNITURE_TEXT = "#64748B"     # Texto mobília
    
    # Feedback Visual
    SUCCESS = "#10B981"            # Verde sucesso
    ERROR = "#EF4444"              # Vermelho erro
    WARNING = "#F59E0B"            # Amarelo aviso
    INFO = "#3B82F6"               # Azul informação
    
    # Gradientes (simulados)
    GRADIENT_START = "#3B82F6"     # Início do gradiente
    GRADIENT_END = "#8B5CF6"       # Fim do gradiente
    
    # Dimensões e Espaçamento (Reduzido para design minimalista)
    CORNER_RADIUS = 12             # Raio padrão para bordas
    CORNER_RADIUS_LARGE = 16       # Raio grande (cards principais)
    CORNER_RADIUS_SMALL = 6        # Raio pequeno (inputs)
    CORNER_RADIUS_PILL = 20        # Raio para botões pill
    
    PADDING = 16                   # Espaçamento padrão
    PADDING_LARGE = 20             # Espaçamento grande
    PADDING_SMALL = 12             # Espaçamento pequeno
    PADDING_TINY = 6               # Espaçamento mínimo
    
    # Tipografia Moderna
    # Tipografia principal (Inter como primária, Roboto como fallback)
    FONT_FAMILY = "Segoe UI"       # Fonte principal (nativa Windows)
    FONT_FAMILY_ALT = "Roboto"     # Fonte secundária/fallback
    FONT_FAMILY_MONO = "Roboto Mono"  # Fonte monoespaçada/fallback
    
    # Tamanhos de Fonte (Reduzido para design compacto)
    FONT_SIZE_TITLE = 20           # Títulos principais
    FONT_SIZE_HEADING = 16         # Cabeçalhos
    FONT_SIZE_SUBHEADING = 14      # Subcabeçalhos
    FONT_SIZE_BODY = 13            # Texto corpo
    FONT_SIZE_LABEL = 12           # Labels
    FONT_SIZE_BUTTON = 13          # Botões
    FONT_SIZE_SMALL = 11           # Texto pequeno
    FONT_SIZE_TINY = 10            # Texto muito pequeno

    # Suporte tipográfico
    FONT_WEIGHTS = (400, 500, 600)

    # Estados suaves e desabilitados
    ACCENT_SOFT = "#DBEAFE"        # Azul bem suave (selecionado)
    ACCENT_SOFT_HOVER = "#BFDBFE"  # Azul suave hover
    NEUTRAL_SOFT = "#F1F5F9"       # Neutro bem claro
    DISABLED_BG = "#F1F5F9"        # Background desabilitado
    DISABLED_TEXT = "#94A3B8"      # Texto desabilitado (legível)
    
    # Sombras (simuladas com bordas/cores no CustomTkinter)
    SHADOW_COLOR = "#E2E8F0"       # Sombra suave
    SHADOW_STRONG = "#CBD5E1"      # Sombra mais forte
    
    # Elevação (para cards flutuantes)
    ELEVATION_1 = "#F8FAFC"        # Nível 1
    ELEVATION_2 = "#F1F5F9"        # Nível 2
