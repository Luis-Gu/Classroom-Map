# 🎨 Redesign da Interface - Classroom Map Generator

## ✨ Visão Geral

A interface do Classroom Map Generator foi completamente redesenhada com uma abordagem moderna, minimalista e profissional, inspirada em aplicativos como **Notion**, **Canva** e **Figma**.

## 🎯 Identidade Visual

### Paleta de Cores

- **Azul Escuro Principal**: `#0E0E4E` - Cor principal da marca
- **Cinza Neutro**: `#757577` - Textos secundários e elementos sutis
- **Fundo Claro**: `#F7F8FA` - Cor de fundo do aplicativo
- **Branco Puro**: `#FFFFFF` - Cards e superfícies elevadas

### Tipografia

- **Fonte Principal**: Segoe UI
- **Tamanhos**:
  - Títulos: 26px bold
  - Cabeçalhos: 20px bold
  - Corpo: 14px regular
  - Labels: 13px medium
  - Botões: 15px semibold

## 🎨 Componentes Redesenhados

### 1. Sidebar (Painel Esquerdo)

**Características:**
- Largura fixa de 380px
- Fundo branco puro
- Scroll suave e responsivo
- Espaçamentos consistentes (24px)

**Seções:**
1. **Cabeçalho**
   - Título grande e bold: "Gerador de Mapa"
   - Subtítulo descritivo
   
2. **Nome da Sala**
   - Input moderno com bordas sutis
   - Placeholder descritivo
   - Efeito hover na borda

3. **Layout das Filas**
   - 4 sliders modernos e finos
   - Valor em destaque azul à direita
   - Cor de progresso azul escuro
   
4. **Mobília da Sala**
   - Botões segmentados estilo "pill"
   - Seleção exclusiva (evita conflitos)
   - Hover suave em cinza claro
   
5. **Turmas**
   - Tabs modernas com bordas arredondadas
   - Inputs com fundo elevado
   - Textboxes com fonte monoespaçada
   - Placeholders inteligentes

6. **Painel de Ações** (fixo no fundo)
   - **Botão Principal**: "GERAR MAPA"
     - Grande (56px altura)
     - Formato pill (bordas muito arredondadas)
     - Azul escuro com hover mais claro
     - Cursor pointer
   - **Botões Secundários**:
     - Salvar, Carregar, PDF
     - Estilo outline
     - Grid responsivo 1:1:1

### 2. Visualizador (Painel Direito)

**Características:**
- Fundo cinza claro (`#F7F8FA`)
- Card central branco com bordas arredondadas
- Margem generosa (32px)
- Sombra sutil simulada

**Elementos:**
1. **Cabeçalho do Preview**
   - Título: "Preview da Sala"
   - Badge com contador de alunos
   
2. **Estado Vazio**
   - Ícone circular com sala simplificada
   - Texto instruções centralizado
   - Aparece quando não há mapa gerado

3. **Visualização da Sala**
   - **Cabeçalhos das Colunas**:
     - Pills com bordas coloridas
     - Nomes das turmas em destaque
     - Azul escuro (Turma 1) e Cinza (Turma 2)
   
   - **Carteiras**:
     - Sombra simulada para profundidade
     - Fundo branco para mesa
     - Fundo cinza claro para cadeira
     - Bordas suaves
     - Nome do aluno em negrito
     - Espaçamento consistente
   
   - **Mobília**:
     - Cards arredondados
     - Fundo cinza claro
     - Borda cinza
     - Texto cinza escuro
     - Posicionamento nas margens

### 3. Layout Responsivo

**Grid System:**
```
[Sidebar: 380px fixo] | [Conteúdo: expansível]
```

**Comportamento:**
- Sidebar mantém largura mínima
- Preview escala automaticamente
- Carteiras se ajustam proporcionalmente
- Centralização automática do conteúdo
- Margens adaptativas

### 4. Animações e Micro-interações

**Implementadas:**

1. **Toast Notifications**
   - Aparecem no topo centro
   - 4 tipos: success, error, warning, info
   - Ícones intuitivos
   - Desaparecem automaticamente (3s)
   
2. **Loading Overlay**
   - Fundo semi-transparente azul escuro
   - Card central branco
   - Animação de pontos (...)
   - Usado em "Gerar Mapa" e "Exportar PDF"

3. **Hover Effects**
   - Inputs: borda muda para azul escuro
   - Botões: mudança suave de cor
   - Cursor pointer em elementos clicáveis
   
4. **Feedback Visual**
   - Geração: loading + toast de sucesso
   - Salvar/Carregar: toast instantâneo
   - Exportar: loading + toast de confirmação
   - Erros: toast vermelho

## 📁 Arquitetura de Arquivos

```
ui/
├── theme.py              # Tema completo com todas as cores e constantes
├── app_window.py         # Janela principal + handlers
├── sidebar.py            # Painel esquerdo com todos os controles
├── classroom_visualizer.py  # Preview da sala
├── animations.py         # Sistema de animações e feedback
├── layout_editor.py      # (não modificado)
└── __init__.py
```

## 🚀 Como Usar

### Executar o Aplicativo

```powershell
# Ativar ambiente virtual
.\venv\Scripts\activate

# Executar
python main.py
```

### Fluxo de Uso

1. **Configurar Nome da Sala**
   - Digite no campo "Nome da Sala"

2. **Ajustar Layout**
   - Use os sliders para definir quantas carteiras por fila (1-15)
   - Configure posição de Quadro, Porta e Janelas

3. **Adicionar Alunos**
   - Clique nas tabs "Turma 1" e "Turma 2"
   - Digite um nome por linha

4. **Gerar Mapa**
   - Clique no botão azul grande "GERAR MAPA"
   - Aguarde o loading
   - Visualize o resultado no preview

5. **Exportar**
   - Salvar configuração (JSON) para reutilizar depois
   - Exportar PDF para impressão

## 🎯 Melhorias Implementadas

### ✅ Layout Responsivo
- Grid configurado corretamente
- Sidebar com largura fixa
- Preview escalável e centralizado
- Componentes se ajustam ao redimensionamento

### ✅ Tipografia Moderna
- Fonte Segoe UI em todos os elementos
- Hierarquia clara de tamanhos
- Pesos variados (regular, medium, bold)
- Contraste otimizado

### ✅ Componentes Modernos
- Sliders finos com valor destacado
- Botões pill com bordas arredondadas
- Segmented buttons com hover
- Inputs com feedback visual
- Cards com sombras simuladas

### ✅ Animações Elegantes
- Toast notifications suaves
- Loading overlay profissional
- Hover effects consistentes
- Feedback visual em todas as ações

### ✅ Visual Premium
- Espaçamentos generosos e consistentes
- Sombras sutis simuladas
- Bordas arredondadas
- Cores balanceadas
- Design limpo e organizado

### ✅ Preview Melhorado
- Card branco centralizado
- Cabeçalho com informações
- Estado vazio amigável
- Carteiras com profundidade
- Mobília estilizada
- Escala automática

### ✅ Botão Principal Destacado
- 56px de altura
- Bordas muito arredondadas (pill)
- Azul escuro marcante
- Hover mais claro
- Feedback visual ao clicar

## 🎨 Guia de Estilo

### Cores Semânticas

```python
# Estados
SUCCESS = "#10B981"   # Verde
ERROR = "#EF4444"     # Vermelho
WARNING = "#F59E0B"   # Amarelo
INFO = "#3B82F6"      # Azul

# Interação
HOVER_LIGHT = "#F0F2F5"
SELECTED = "#E6E7FF"
```

### Espaçamentos

```python
PADDING = 24          # Padrão
PADDING_LARGE = 32    # Grande
PADDING_SMALL = 16    # Pequeno
PADDING_TINY = 8      # Mínimo
```

### Bordas

```python
CORNER_RADIUS = 16           # Padrão
CORNER_RADIUS_LARGE = 24     # Cards principais
CORNER_RADIUS_SMALL = 8      # Inputs
CORNER_RADIUS_PILL = 30      # Botões pill
```

## 📊 Antes vs Depois

### Antes
- Visual básico e funcional
- Cores vibrantes (vermelho, azul forte)
- Espaçamentos inconsistentes
- Sem feedback visual claro
- Layout menos polido

### Depois
- Visual profissional e elegante
- Cores sutis e harmoniosas
- Espaçamentos generosos e consistentes
- Feedback visual em toda interação
- Layout responsivo e moderno
- Animações suaves
- Hierarquia visual clara
- Experiência de uso fluida

## 🎓 Tecnologias

- **Python 3.x**
- **CustomTkinter** - Framework UI moderno
- **Canvas Tkinter** - Desenho do preview
- **Princípios de Design**:
  - Material Design
  - Apple Human Interface Guidelines
  - Fluent Design System

## 🔮 Futuras Melhorias (Opcionais)

- [ ] Dark mode completo
- [ ] Animações de transição entre estados
- [ ] Drag & drop de alunos
- [ ] Undo/Redo
- [ ] Atalhos de teclado
- [ ] Zoom no preview
- [ ] Exportar para PNG/SVG
- [ ] Temas customizáveis

---

**Desenvolvido com ❤️ para tornar o trabalho da professora mais fácil e agradável!**
