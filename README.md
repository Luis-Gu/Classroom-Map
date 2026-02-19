# 🪑 Mapa da Sala

> **Gerador de Mapa de Sala** — Organize carteiras, alunos e turmas de forma visual e exporte o layout em PDF.

Uma aplicação desktop feita em Python para professores e coordenadores que precisam criar mapas de sala de aula de forma rápida, visual e profissional. Basta cadastrar os alunos, configurar a sala e gerar!

---

## ✨ Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| 🖥️ **Preview em tempo real** | Visualize o mapa da sala enquanto configura |
| 👥 **Duas turmas** | Suporte para duas turmas lado a lado (ex: Turma A e Turma B) com cores distintas |
| 🔀 **Distribuição automática** | Algoritmo inteligente para posicionar alunos nas carteiras |
| 🪑 **Layout flexível** | Configure o número de filas e carteiras por fila usando sliders |
| 🚪 **Mobília da sala** | Posicione quadro, porta e janelas em qualquer lado da sala |
| 📄 **Exportar PDF** | Gere um PDF profissional do mapa para impressão |
| 💾 **Salvar/Carregar** | Sistema interno de saves — salve e carregue layouts sem complicação |
| 🎨 **Interface moderna** | UI limpa e responsiva com CustomTkinter |

---

## 📸 Preview

<p align="center">
  <img src="icon/app.ico" width="64" alt="Ícone do app">
</p>

---

## 🚀 Como Usar

### Pré-requisitos

- **Python 3.9+** instalado
- **pip** (gerenciador de pacotes)

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/Luis-Gu/Classroom-Map.git
cd Classroom-Map

# 2. Crie o ambiente virtual
python -m venv venv

# 3. Ative o ambiente virtual
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt
```

### Executar

```bash
python main.py
```

### Gerar executável (.exe)

```bash
pip install pyinstaller
pyinstaller main.spec
```

O executável será gerado em `dist/MapaDeSala/MapaDeSala.exe`.

---

## 🗂️ Estrutura do Projeto

```
Classroom-Map/
├── main.py                 # Ponto de entrada
├── main.spec               # Configuração do PyInstaller
├── requirements.txt        # Dependências
│
├── ui/                     # Interface gráfica
│   ├── app_window.py       # Janela principal
│   ├── sidebar_unified.py  # Painel lateral (configuração)
│   ├── classroom_visualizer.py  # Preview do mapa
│   ├── theme.py            # Cores e estilos
│   ├── animations.py       # Loading e toasts
│   └── furniture_selector.py    # Seletor de mobília
│
├── logic/                  # Lógica de negócio
│   ├── student_manager.py  # Gerenciamento de alunos
│   └── seating_algorithm.py # Algoritmo de distribuição
│
├── utils/                  # Utilitários
│   ├── file_handler.py     # Salvar/carregar layouts
│   └── pdf_exporter.py     # Exportação para PDF
│
├── icon/                   # Ícones do aplicativo
├── saves/                  # Layouts salvos (local)
└── dist/                   # Executáveis gerados
```

---

## 🛠️ Tecnologias

- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** — Interface gráfica moderna
- **[FPDF2](https://github.com/py-pdf/fpdf2)** — Geração de PDFs
- **[Pillow](https://pillow.readthedocs.io/)** — Manipulação de imagens
- **[PyInstaller](https://pyinstaller.org/)** — Empacotamento como `.exe`

---

## 📋 Como funciona

1. **Configure a sala** — Defina o nome da sala, número de filas e carteiras por fila
2. **Posicione a mobília** — Escolha onde ficam o quadro, porta e janelas
3. **Cadastre os alunos** — Insira os nomes nas abas Turma 1 e Turma 2
4. **Gere o mapa** — Clique em "Gerar Mapa" e veja o preview em tempo real
5. **Exporte** — Salve o layout ou exporte como PDF para impressão

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

<p align="center">
  Feito por Luis Gustavo
</p>
