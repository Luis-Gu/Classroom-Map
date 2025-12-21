import flet as ft
import random
import json
from typing import Optional, List, Dict, Any

# --- Configurações e Constantes ---
class AppColors:
    PRIMARY = ft.Colors.INDIGO_600
    PRIMARY_LIGHT = ft.Colors.INDIGO_100
    SECONDARY = ft.Colors.TEAL_600
    BACKGROUND = ft.Colors.BLUE_GREY_50
    SURFACE = ft.Colors.WHITE
    TEXT_PRIMARY = ft.Colors.BLUE_GREY_900
    TEXT_SECONDARY = ft.Colors.BLUE_GREY_500
    BORDER = ft.Colors.BLUE_GREY_200
    SUCCESS = ft.Colors.GREEN_500
    ERROR = ft.Colors.RED_500
    DRAGGING = ft.Colors.INDIGO_300
    GHOST = ft.Colors.INDIGO_200

class AppDimensions:
    SIDEBAR_WIDTH = 320
    CARD_WIDTH = 100
    CARD_HEIGHT = 70
    BORDER_RADIUS = 12
    PADDING = 20

# --- Componentes Personalizados ---

class Aluno(ft.Draggable):
    def __init__(self, nome: str, source_id: str):
        self.nome = nome
        self.source_id = source_id
        
        # Conteúdo visual do aluno (Card)
        content_normal = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=16),
                    ft.Text(
                        value=nome, 
                        weight=ft.FontWeight.W_600, 
                        color=ft.Colors.WHITE, 
                        size=11, 
                        text_align=ft.TextAlign.CENTER,
                        max_lines=2,
                        overflow=ft.TextOverflow.ELLIPSIS
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2
            ),
            width=AppDimensions.CARD_WIDTH - 10, # Um pouco menor que a carteira
            height=AppDimensions.CARD_HEIGHT - 10,
            bgcolor=AppColors.PRIMARY,
            border_radius=AppDimensions.BORDER_RADIUS - 2,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(blur_radius=4, color=ft.Colors.BLACK26, offset=ft.Offset(0, 2)),
        )

        # Visual enquanto arrasta (Fantasma)
        content_dragging = ft.Container(
            content=ft.Text(value=nome, color=ft.Colors.WHITE, size=12, weight=ft.FontWeight.BOLD),
            width=AppDimensions.CARD_WIDTH - 10,
            height=AppDimensions.CARD_HEIGHT - 10,
            bgcolor=AppColors.DRAGGING,
            border_radius=AppDimensions.BORDER_RADIUS - 2,
            alignment=ft.alignment.center,
            opacity=0.7,
            border=ft.border.all(2, ft.Colors.WHITE)
        )

        super().__init__(
            group="alunos",
            content=content_normal,
            content_when_dragging=content_dragging,
            data=json.dumps({"nome": nome, "source_id": source_id})
        )

class Carteira(ft.DragTarget):
    def __init__(self, id: str, on_move_callback, aluno: Optional[Aluno] = None):
        self.my_id = id
        self.on_move_callback = on_move_callback
        self.aluno_atual = aluno

        self.container = ft.Container(
            width=AppDimensions.CARD_WIDTH,
            height=AppDimensions.CARD_HEIGHT,
            bgcolor=AppColors.SURFACE,
            border=ft.border.all(1, AppColors.BORDER),
            border_radius=AppDimensions.BORDER_RADIUS,
            alignment=ft.alignment.center,
            content=self._get_content(),
            animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT)
        )
        
        super().__init__(
            group="alunos",
            content=self.container,
            on_accept=self.drag_accept,
            on_will_accept=self.drag_will_accept,
            on_leave=self.drag_leave
        )

    def _get_content(self):
        if self.aluno_atual:
            return self.aluno_atual
        return ft.Column(
            [
                ft.Icon(ft.Icons.EVENT_SEAT, color=ft.Colors.BLUE_GREY_100, size=20),
                ft.Text("Vazia", size=10, color=ft.Colors.BLUE_GREY_200)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2
        )

    def drag_will_accept(self, e):
        self.container.border = ft.border.all(2, AppColors.SUCCESS)
        self.container.bgcolor = ft.Colors.GREEN_50
        self.container.scale = 1.05
        self.container.update()

    def drag_leave(self, e):
        self.container.border = ft.border.all(1, AppColors.BORDER)
        self.container.bgcolor = AppColors.SURFACE
        self.container.scale = 1.0
        self.container.update()

    def drag_accept(self, e):
        self.container.border = ft.border.all(1, AppColors.BORDER)
        self.container.bgcolor = AppColors.SURFACE
        self.container.scale = 1.0
        
        src = self.page.get_control(e.src_id)
        data = json.loads(e.data)
        
        nome_aluno = data['nome']
        id_origem = data['source_id']
        
        self.on_move_callback(nome_aluno, id_origem, self.my_id)

    def set_aluno(self, nome: str):
        self.aluno_atual = Aluno(nome, self.my_id)
        self.container.content = self.aluno_atual
        self.update()

    def clear(self):
        self.aluno_atual = None
        self.container.content = self._get_content()
        self.update()

# --- Aplicação Principal ---

def main(page: ft.Page):
    # Configurações da Página
    page.title = "Classroom Map - Organizador de Salas"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window_min_width = 1000
    page.window_min_height = 700
    page.bgcolor = AppColors.BACKGROUND
    
    # Fontes (Opcional: carregar Google Fonts se desejar)
    page.fonts = {
        "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap"
    }
    page.theme = ft.Theme(font_family="Roboto")

    # Estado
    carteiras_map: Dict[str, Carteira] = {}

    # --- Lógica de Negócio ---

    def mover_aluno(nome: str, id_origem: str, id_destino: str):
        if id_origem == id_destino:
            return

        # Remove da origem se existir
        if id_origem in carteiras_map:
            carteiras_map[id_origem].clear()
        
        # Lida com o destino
        carteira_destino = carteiras_map[id_destino]
        aluno_anterior = carteira_destino.aluno_atual
        
        # Coloca o novo aluno no destino
        carteira_destino.set_aluno(nome)

        # Se tinha alguém no destino, manda para a origem (troca)
        if aluno_anterior and id_origem in carteiras_map:
             carteiras_map[id_origem].set_aluno(aluno_anterior.nome)
        
        # Feedback visual (opcional)
        page.update()

    def gerar_sala(rows: int, cols: int):
        carteiras_map.clear()
        grid_sala.controls.clear()

        texto_raw = input_alunos.value
        lista_alunos = [nome.strip() for nome in texto_raw.split('\n') if nome.strip()]
        
        if not lista_alunos:
             page.show_snack_bar(ft.SnackBar(content=ft.Text("A lista de alunos está vazia!"), bgcolor=AppColors.ERROR))
             return

        random.shuffle(lista_alunos)

        total_carteiras = rows * cols
        grid_sala.runs_count = cols
        
        for i in range(total_carteiras):
            carteira_id = f"desk_{i}"
            
            aluno_inicial = None
            if i < len(lista_alunos):
                aluno_inicial = Aluno(lista_alunos[i], carteira_id)

            nova_carteira = Carteira(
                id=carteira_id, 
                on_move_callback=mover_aluno,
                aluno=aluno_inicial
            )
            
            carteiras_map[carteira_id] = nova_carteira
            grid_sala.controls.append(nova_carteira)

        page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Sala gerada com {len(lista_alunos)} alunos!"), bgcolor=AppColors.SUCCESS))
        grid_sala.update()

    # --- Elementos da UI ---

    # Sidebar Components
    input_alunos = ft.TextField(
        label="Lista de Alunos",
        multiline=True,
        expand=True, # Expande para ocupar o espaço disponível
        hint_text="Cole os nomes aqui (um por linha)...",
        text_size=13,
        bgcolor=AppColors.SURFACE,
        border_color=AppColors.BORDER,
        border_radius=8,
        content_padding=15
    )

    btn_modelo_1 = ft.ElevatedButton(
        text="Modelo de Sala 1 (5x5)", 
        icon=ft.Icons.GRID_ON, 
        style=ft.ButtonStyle(
            bgcolor={"": AppColors.PRIMARY, "hovered": AppColors.PRIMARY_LIGHT},
            color={"": AppColors.SURFACE, "hovered": AppColors.PRIMARY},
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=2
        ),
        width=280,
        on_click=lambda e: gerar_sala(5, 5)
    )

    btn_modelo_2 = ft.ElevatedButton(
        text="Modelo de Sala 2 (6x6)", 
        icon=ft.Icons.GRID_4X4, 
        style=ft.ButtonStyle(
            bgcolor={"": AppColors.SECONDARY, "hovered": AppColors.PRIMARY_LIGHT},
            color={"": AppColors.SURFACE, "hovered": AppColors.SECONDARY},
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=2
        ),
        width=280,
        on_click=lambda e: gerar_sala(6, 6)
    )

    btn_template = ft.OutlinedButton(
        "Carregar Template", 
        icon=ft.Icons.FILE_UPLOAD_OUTLINED,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=15
        ),
        width=280
    )
    
    btn_salvar = ft.OutlinedButton(
        "Salvar Configuração", 
        icon=ft.Icons.SAVE_OUTLINED,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=15
        ),
        width=280
    )

    sidebar_content = ft.Column(
        controls=[
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.SCHOOL, color=AppColors.PRIMARY, size=30),
                    ft.Text("Classroom Map", size=22, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY)
                ], alignment=ft.MainAxisAlignment.CENTER),
                padding=ft.padding.only(bottom=20)
            ),
            ft.Divider(color=AppColors.BORDER),
            ft.Text("Alunos", weight=ft.FontWeight.W_600, color=AppColors.TEXT_SECONDARY, size=14),
            ft.Container(
                content=input_alunos,
                expand=True, # Container expande
                padding=ft.padding.only(bottom=10)
            ),
            ft.Divider(color=AppColors.BORDER),
            ft.Text("Gerar Sala", weight=ft.FontWeight.W_600, color=AppColors.TEXT_SECONDARY, size=14),
            ft.Container(height=10),
            btn_modelo_1,
            ft.Container(height=10),
            btn_modelo_2,
            ft.Container(height=20),
            ft.Column([btn_template, btn_salvar], spacing=10)
        ],
        expand=True, # Coluna ocupa toda a altura
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5
    )

    sidebar = ft.Container(
        width=AppDimensions.SIDEBAR_WIDTH,
        bgcolor=AppColors.SURFACE,
        padding=AppDimensions.PADDING,
        border=ft.border.only(right=ft.border.BorderSide(1, AppColors.BORDER)),
        content=sidebar_content,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12, offset=ft.Offset(2, 0))
    )

    # Main Area Components
    grid_sala = ft.GridView(
        expand=True,
        runs_count=5,
        max_extent=130, 
        child_aspect_ratio=1.3,
        spacing=15,
        run_spacing=15,
        padding=20
    )

    header_main = ft.Container(
        padding=ft.padding.symmetric(horizontal=20, vertical=15),
        bgcolor=AppColors.SURFACE,
        border=ft.border.only(bottom=ft.border.BorderSide(1, AppColors.BORDER)),
        content=ft.Row(
            controls=[
                ft.Column([
                    ft.Text("Mapa da Sala", size=20, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_PRIMARY),
                    ft.Text("Arraste e solte os alunos para organizar a disposição da sala.", size=12, color=AppColors.TEXT_SECONDARY),
                ]),
                ft.Row([
                    ft.IconButton(icon=ft.Icons.ZOOM_IN, tooltip="Aumentar Zoom"),
                    ft.IconButton(icon=ft.Icons.ZOOM_OUT, tooltip="Diminuir Zoom"),
                    ft.IconButton(icon=ft.Icons.PRINT, tooltip="Imprimir"),
                ])
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    )

    main_area = ft.Container(
        expand=True,
        bgcolor=AppColors.BACKGROUND,
        content=ft.Column(
            controls=[
                header_main,
                ft.Container(
                    content=grid_sala,
                    expand=True,
                    padding=20
                )
            ],
            spacing=0
        )
    )

    # Layout Final
    layout = ft.Row(
        controls=[sidebar, main_area],
        expand=True,
        spacing=0
    )

    page.add(layout)

if __name__ == "__main__":
    ft.app(target=main)
