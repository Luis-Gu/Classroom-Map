# 🎨 Guia de Customização - Classroom Map Generator

Este guia mostra como personalizar facilmente a aparência do aplicativo.

## 🎨 Mudando Cores

### Localização
Todas as cores estão centralizadas em: **`ui/theme.py`**

### Cores Principais

```python
# Para mudar a cor principal do app:
PRIMARY_DARK = "#0E0E4E"  # Altere para qualquer código hex

# Para mudar o cinza neutro:
GRAY_NEUTRAL = "#757577"

# Para mudar o fundo:
BACKGROUND_LIGHT = "#F7F8FA"
```

### Cores das Turmas

```python
# Cor da Turma 1 (aparece nos headers e colunas 1 e 3)
CLASS_A_COLOR = "#0E0E4E"  # Azul escuro

# Cor da Turma 2 (aparece nos headers e colunas 2 e 4)
CLASS_B_COLOR = "#757577"  # Cinza neutro
```

### Cores de Feedback

```python
# Verde de sucesso (toast e mensagens)
SUCCESS = "#10B981"

# Vermelho de erro
ERROR = "#EF4444"

# Amarelo de aviso
WARNING = "#F59E0B"

# Azul de informação
INFO = "#3B82F6"
```

## 📝 Mudando Fontes

### Fonte Principal

```python
# Localização: ui/theme.py

# Windows
FONT_FAMILY = "Segoe UI"

# macOS
FONT_FAMILY = "San Francisco"

# Linux
FONT_FAMILY = "Ubuntu"

# Universais
FONT_FAMILY = "Arial"
FONT_FAMILY = "Helvetica"
```

### Tamanhos de Fonte

```python
# Para deixar tudo maior:
FONT_SIZE_TITLE = 30        # Era 26
FONT_SIZE_HEADING = 24      # Era 20
FONT_SIZE_BODY = 16         # Era 14
FONT_SIZE_BUTTON = 17       # Era 15

# Para deixar tudo menor:
FONT_SIZE_TITLE = 22        # Era 26
FONT_SIZE_HEADING = 18      # Era 20
FONT_SIZE_BODY = 13         # Era 14
FONT_SIZE_BUTTON = 14       # Era 15
```

## 📐 Ajustando Espaçamentos

### Espaçamento Geral

```python
# Localização: ui/theme.py

# Para mais espaço (layout mais "arejado"):
PADDING = 32                # Era 24
PADDING_LARGE = 48          # Era 32
PADDING_SMALL = 20          # Era 16

# Para menos espaço (mais compacto):
PADDING = 16                # Era 24
PADDING_LARGE = 24          # Era 32
PADDING_SMALL = 12          # Era 16
```

### Largura da Sidebar

```python
# Localização: ui/app_window.py, linha ~54

# Sidebar mais larga:
self.sidebar = Sidebar(
    self,
    width=450,  # Era 380
    ...
)

# Sidebar mais estreita:
self.sidebar = Sidebar(
    self,
    width=320,  # Era 380
    ...
)
```

## ⭕ Mudando Bordas

### Arredondamento

```python
# Localização: ui/theme.py

# Bordas mais arredondadas:
CORNER_RADIUS = 20              # Era 16
CORNER_RADIUS_LARGE = 32        # Era 24
CORNER_RADIUS_PILL = 40         # Era 30

# Bordas mais quadradas:
CORNER_RADIUS = 8               # Era 16
CORNER_RADIUS_LARGE = 12        # Era 24
CORNER_RADIUS_PILL = 20         # Era 30

# Completamente quadrado (sem bordas arredondadas):
CORNER_RADIUS = 0
CORNER_RADIUS_LARGE = 0
CORNER_RADIUS_PILL = 0
```

## 🔘 Ajustando Botões

### Botão Principal "GERAR MAPA"

```python
# Localização: ui/sidebar.py, linha ~347

# Botão maior:
self.btn_generate = ctk.CTkButton(
    ...,
    height=64,  # Era 56
    font=(Theme.FONT_FAMILY, 18, "bold"),  # Era 15
    ...
)

# Botão menor:
self.btn_generate = ctk.CTkButton(
    ...,
    height=48,  # Era 56
    font=(Theme.FONT_FAMILY, 14, "bold"),  # Era 15
    ...
)
```

### Botões Secundários

```python
# Localização: ui/sidebar.py, linha ~393

# Altura dos botões secundários:
btn = ctk.CTkButton(
    ...,
    height=42,  # Era 38
    ...
)
```

## 🖼️ Customizando Preview

### Tamanho das Carteiras

```python
# Localização: ui/classroom_visualizer.py, linha ~168

# Carteiras maiores:
item_w = 80   # Era 70
item_h = 66   # Era 58
gap_x = 28    # Era 24
gap_y = 22    # Era 18

# Carteiras menores:
item_w = 60   # Era 70
item_h = 50   # Era 58
gap_x = 20    # Era 24
gap_y = 14    # Era 18
```

### Margens do Preview

```python
# Localização: ui/classroom_visualizer.py, linha ~162

# Margens maiores:
margin_top = 100      # Era 80
margin_bottom = 100   # Era 80
margin_left = 100     # Era 80
margin_right = 100    # Era 80

# Margens menores:
margin_top = 60       # Era 80
margin_bottom = 60    # Era 80
margin_left = 60      # Era 80
margin_right = 60     # Era 80
```

## 🎭 Ativando/Desativando Animações

### Desativar Toast Notifications

```python
# Localização: ui/app_window.py

# Comentar as linhas de ToastNotification:

def handle_generate(self):
    ...
    # ToastNotification.show(...)  # Comentar
    ...

def _finish_generation(self, seating_map):
    ...
    # ToastNotification.show(...)  # Comentar
    ...
```

### Desativar Loading Overlay

```python
# Localização: ui/app_window.py

# No método handle_generate:
def handle_generate(self):
    ...
    # self.loading.show("Gerando mapa")  # Comentar
    ...
    # self.loading.hide()  # Comentar
    ...
```

### Ajustar Duração das Animações

```python
# Localização: ui/app_window.py

# Toast mais rápido:
ToastNotification.show(
    ...,
    duration=1500  # Era 3000 (ms)
)

# Toast mais lento:
ToastNotification.show(
    ...,
    duration=5000  # Era 3000 (ms)
)
```

## 🪟 Ajustando Tamanho da Janela

### Tamanho Inicial

```python
# Localização: ui/app_window.py, linha ~17

# Janela maior:
self.geometry("1600x1000")  # Era "1400x900"

# Janela menor:
self.geometry("1200x800")   # Era "1400x900"
```

### Tamanho Mínimo

```python
# Localização: ui/app_window.py, linha ~18

# Permite janela menor:
self.minsize(900, 650)  # Era (1100, 750)

# Força janela maior:
self.minsize(1300, 850)  # Era (1100, 750)
```

## 🎨 Criando um Tema Escuro

Para criar um tema escuro, modifique as cores em `ui/theme.py`:

```python
# Cores para Dark Mode
PRIMARY_DARK = "#6B7FFF"       # Azul mais claro
BACKGROUND_LIGHT = "#1E1E1E"   # Fundo escuro
WHITE_PURE = "#2D2D2D"         # Cards escuros
TEXT_PRIMARY = "#E4E4E4"       # Texto claro
TEXT_SECONDARY = "#A0A0A0"     # Texto secundário claro
BORDER = "#404040"             # Bordas escuras

# Configure o modo:
# Em app_window.py, linha ~16:
ctk.set_appearance_mode("Dark")
```

## 📱 Ajustando para Tela Pequena

Para laptops com tela menor:

```python
# 1. Reduzir sidebar (ui/app_window.py):
width=300  # Era 380

# 2. Reduzir espaçamentos (ui/theme.py):
PADDING = 16           # Era 24
PADDING_LARGE = 20     # Era 32

# 3. Reduzir fontes (ui/theme.py):
FONT_SIZE_TITLE = 22   # Era 26
FONT_SIZE_BODY = 13    # Era 14

# 4. Janela menor (ui/app_window.py):
self.geometry("1100x750")  # Era "1400x900"
```

## 🔄 Reverter para Design Anterior

Se quiser voltar ao design original, use o git:

```powershell
# Ver o commit anterior ao redesign
git log --oneline

# Reverter apenas os arquivos de UI
git checkout HEAD~1 -- ui/

# Ou restaurar tudo
git reset --hard HEAD~1
```

## 💡 Dicas

1. **Sempre edite `ui/theme.py` primeiro** - É onde todas as constantes estão
2. **Teste mudanças incrementalmente** - Uma mudança por vez
3. **Mantenha consistência** - Use o mesmo espaçamento em todo o app
4. **Documentação**: Adicione comentários quando customizar
5. **Backup**: Faça commit antes de grandes mudanças

## 🆘 Problemas Comuns

### Texto cortado
- Aumente `width` dos componentes
- Reduza `FONT_SIZE_*`

### Layout quebrado
- Verifique `grid_rowconfigure` e `grid_columnconfigure`
- Confirme `sticky="nsew"` em componentes expansíveis

### Cores não mudam
- Reinicie o aplicativo após editar `theme.py`
- Verifique se editou a constante certa

### Botões muito grandes/pequenos
- Ajuste `height` no componente
- Modifique `FONT_SIZE_BUTTON`

---

**Divirta-se customizando! 🎨**
