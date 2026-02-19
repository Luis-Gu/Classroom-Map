import customtkinter as ctk
from .theme import Theme
from PIL import Image, ImageDraw, ImageFont, ImageTk
import io

class ClassroomVisualizer(ctk.CTkFrame):
    """
    Visualizador premium da sala de aula
    Design moderno com cards, sombras e animações suaves
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Configuração do container principal
        self.configure(
            fg_color=Theme.BACKGROUND_LIGHT,
            corner_radius=0
        )
        
        # Card container com visual premium (sem bordas, elevação sutil)
        self.card_container = ctk.CTkFrame(
            self,
            fg_color=Theme.WHITE_PURE,
            corner_radius=Theme.CORNER_RADIUS_LARGE,
            border_width=0  # Sem borda para visual limpo
        )
        self.card_container.pack(
            fill="both",
            expand=True,
            padx=Theme.PADDING_LARGE,
            pady=Theme.PADDING_LARGE
        )
        
        # Cabeçalho do preview
        self._build_header()
        
        # Canvas para desenho
        self.canvas = ctk.CTkCanvas(
            self.card_container,
            bg=Theme.WHITE_PURE,
            highlightthickness=0,
            cursor="arrow"
        )
        self.canvas.pack(
            fill="both",
            expand=True,
            padx=Theme.PADDING,
            pady=(0, Theme.PADDING)
        )
        
        # Estado
        self.resize_triggered = False
        self.canvas.bind("<Configure>", self.on_resize)
        
        self.current_config = {
            "rows": [7, 7, 7, 7],
            "board": "Topo",
            "door": "Esq",
            "windows": "Dir",
            "room_name": ""
        }
        self.seating_map = {}
        
        # Desenho inicial
        self.draw_empty_state()
    
    def _build_header(self):
        """Cabeçalho do preview com título e info"""
        header = ctk.CTkFrame(
            self.card_container,
            fg_color="transparent",
            height=60
        )
        header.pack(fill="x", padx=Theme.PADDING, pady=(Theme.PADDING, Theme.PADDING_SMALL))
        header.pack_propagate(False)
        
        # Título
        title = ctk.CTkLabel(
            header,
            text="Preview da Sala",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_HEADING, "bold"),
            text_color=Theme.TEXT_PRIMARY,
            anchor="w"
        )
        title.pack(side="left", fill="y")
        
        # Info badge (opcional)
        self.info_label = ctk.CTkLabel(
            header,
            text="",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            text_color=Theme.TEXT_TERTIARY,
            anchor="e"
        )
        self.info_label.pack(side="right", fill="y", padx=(Theme.PADDING_SMALL, 0)) 
        self.info_label.pack(side="right", fill="y", padx=(Theme.PADDING_SMALL, 0))
    
    def draw_empty_state(self):
        """Desenha um estado vazio com mensagem"""
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        if w < 100 or h < 100:
            self.after(100, self.draw_empty_state)
            return
        
        # Ícone ou texto centralizado
        cx, cy = w / 2, h / 2
        
        # Círculo de fundo
        r = 80
        self.canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill=Theme.BACKGROUND_LIGHT,
            outline=Theme.BORDER,
            width=2
        )
        
        # Ícone simples (quadrado representando sala)
        size = 40
        self.canvas.create_rectangle(
            cx - size, cy - size/2, cx + size, cy + size/2,
            fill=Theme.WHITE_PURE,
            outline=Theme.GRAY_NEUTRAL,
            width=2
        )
        
        # Texto
        self.canvas.create_text(
            cx, cy + r + 40,
            text="Configure a sala e clique em 'GERAR MAPA'",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_BODY),
            fill=Theme.TEXT_SECONDARY
        )
    
    def on_resize(self, event):
        """Callback de redimensionamento com debounce"""
        if not self.resize_triggered:
            self.resize_triggered = True
            self.after(100, self.draw)
    
    def update_config(self, config):
        """Atualiza configuração e redesenha"""
        self.current_config = config
        if self.seating_map:
            self.draw()
    
    def set_seating(self, seating_map):
        """Define o mapa de assentos e redesenha"""
        self.seating_map = seating_map
        self.draw()
    
    def draw(self):
        """Desenho principal da sala - matches PDF layout with dynamic sizing"""
        self.resize_triggered = False
        self.canvas.delete("all")
        
        # Limpar referências de imagens antigas
        self._text_images = []
        
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        if w < 100 or h < 100:
            return
        
        # Se não há mapa gerado, mostra estado vazio
        if not self.seating_map:
            self.draw_empty_state()
            return
        
        config = self.current_config
        rows_config = config.get("rows", [7, 7, 7, 7])
        max_rows = max(rows_config)
        num_cols = 4
        
        # === DYNAMIC MARGINS based on furniture placement ===
        furniture_margin = 70  # pixels reserved for furniture labels
        page_margin = 12       # tiny edge margin
        
        board_side = config.get("board")
        door_side = config.get("door")
        windows_side = config.get("windows")
        
        has_top = board_side == "Topo" or door_side == "Topo" or windows_side == "Topo"
        has_bottom = board_side == "Fundo" or door_side == "Fundo" or windows_side == "Fundo"
        has_left = board_side == "Esq" or door_side == "Esq" or windows_side == "Esq"
        has_right = board_side == "Dir" or door_side == "Dir" or windows_side == "Dir"
        
        # Room name header space
        room_name = config.get("room_name", "")
        header_space = 25 if room_name else 10
        
        mt = page_margin + (furniture_margin if has_top else 0) + header_space
        mb = page_margin + (furniture_margin if has_bottom else 0)
        ml = page_margin + (furniture_margin if has_left else 0)
        mr = page_margin + (furniture_margin if has_right else 0)
        
        avail_w = w - ml - mr
        avail_h = h - mt - mb
        
        if avail_w < 50 or avail_h < 50:
            return
        
        # === DYNAMIC SIZING (same proportions as PDF) ===
        corridor_ratio = 0.30
        row_gap_ratio = 0.25
        chair_h_ratio = 0.28
        chair_gap_ratio = 0.08
        
        desk_w = avail_w / (num_cols + (num_cols - 1) * corridor_ratio)
        
        total_item_h = avail_h / (max_rows + (max_rows - 1) * row_gap_ratio)
        desk_h = total_item_h / (1 + chair_gap_ratio + chair_h_ratio)
        chair_h = desk_h * chair_h_ratio
        chair_gap = desk_h * chair_gap_ratio
        
        gap_x = desk_w * corridor_ratio
        gap_y = total_item_h * row_gap_ratio
        
        # Cap max size so desks don't get absurdly large
        max_desk_w = 110
        max_desk_h = 40
        if desk_w > max_desk_w:
            desk_w = max_desk_w
            gap_x = desk_w * corridor_ratio
        if desk_h > max_desk_h:
            desk_h = max_desk_h
            chair_h = desk_h * chair_h_ratio
            chair_gap = desk_h * chair_gap_ratio
            total_item_h = desk_h + chair_gap + chair_h
            gap_y = total_item_h * row_gap_ratio
        
        # Recalculate block for centering
        block_w = (num_cols * desk_w) + ((num_cols - 1) * gap_x)
        block_h = (max_rows * total_item_h) + ((max_rows - 1) * gap_y)
        
        ox = ml + (avail_w - block_w) / 2
        oy = mt + (avail_h - block_h) / 2
        
        # === ROOM NAME (Top Right) ===
        if room_name:
            font_size = max(int(desk_w * 0.15), 11)
            self.canvas.create_text(
                w - page_margin - 5, page_margin + 8,
                text=room_name.upper(),
                fill=Theme.TEXT_PRIMARY,
                font=(Theme.FONT_FAMILY, font_size, "bold"),
                anchor="ne"
            )
        
        # === COLUMN HEADERS ===
        self._draw_column_headers(ox, oy, desk_w, gap_x, rows_config)
        
        # === DESKS ===
        self._draw_desks(ox, oy, desk_w, desk_h, gap_x, gap_y,
                         chair_h, chair_gap, total_item_h, rows_config)
        
        # === FURNITURE ===
        self._draw_furniture(w, h, page_margin, furniture_margin,
                             has_top, has_bottom, has_left, has_right)
        
        # Atualiza info no header
        total_students = len(self.seating_map)
        self.info_label.configure(text=f"{total_students} alunos")
    
    def _draw_column_headers(self, ox, oy, desk_w, gap_x, rows_config):
        """Desenha cabeçalhos das colunas com nome da turma"""
        class_colors = [
            Theme.CLASS_A_COLOR,
            Theme.CLASS_B_COLOR,
            Theme.CLASS_A_COLOR,
            Theme.CLASS_B_COLOR
        ]
        
        # Deduzir nomes das turmas
        class_names = [None, None, None, None]
        for col_idx in range(4):
            for row_idx in range(rows_config[col_idx] if col_idx < len(rows_config) else 7):
                student = self.seating_map.get((col_idx, row_idx))
                if student:
                    class_names[col_idx] = student.get('class', '').upper()
                    break
        
        font_size = max(int(desk_w * 0.11), 8)
        header_y = oy - font_size - 3
        
        for col_idx in range(4):
            x = ox + (col_idx * (desk_w + gap_x)) + (desk_w / 2)
            name = class_names[col_idx] or ""
            color = class_colors[col_idx]
            
            if name:
                if len(name) > 14:
                    name = name[:13] + "."
                
                self.canvas.create_text(
                    x, header_y,
                    text=name,
                    fill=color,
                    font=(Theme.FONT_FAMILY, font_size, "bold")
                )
    
    def _draw_desks(self, ox, oy, desk_w, desk_h, gap_x, gap_y,
                    chair_h, chair_gap, total_item_h, rows_config):
        """Desenha as carteiras com estilo moderno e sombras simuladas"""
        shadow_offset = max(2, desk_w * 0.03)
        name_font_size = max(int(desk_w * 0.08), 5)
        
        for col_idx in range(4):
            num_seats = rows_config[col_idx]
            
            for row_idx in range(num_seats):
                curr_x = ox + (col_idx * (desk_w + gap_x))
                curr_y = oy + (row_idx * (total_item_h + gap_y))
                
                # === SOMBRA da mesa ===
                self.canvas.create_rectangle(
                    curr_x + shadow_offset,
                    curr_y + shadow_offset,
                    curr_x + desk_w + shadow_offset,
                    curr_y + desk_h + shadow_offset,
                    fill=Theme.SHADOW_COLOR,
                    outline=""
                )
                
                # === MESA ===
                self.canvas.create_rectangle(
                    curr_x, curr_y,
                    curr_x + desk_w, curr_y + desk_h,
                    fill=Theme.DESK_FILL,
                    outline=Theme.DESK_BORDER,
                    width=1
                )
                
                # === CADEIRA ===
                ch_w = desk_w * 0.55
                ch_x = curr_x + (desk_w - ch_w) / 2
                ch_y = curr_y + desk_h + chair_gap
                
                # Sombra da cadeira
                self.canvas.create_rectangle(
                    ch_x + shadow_offset / 2,
                    ch_y + shadow_offset / 2,
                    ch_x + ch_w + shadow_offset / 2,
                    ch_y + chair_h + shadow_offset / 2,
                    fill=Theme.SHADOW_COLOR,
                    outline=""
                )
                
                self.canvas.create_rectangle(
                    ch_x, ch_y,
                    ch_x + ch_w, ch_y + chair_h,
                    fill=Theme.CHAIR_FILL,
                    outline=Theme.DESK_BORDER,
                    width=1
                )
                
                # === NOME DO ALUNO ===
                student = self.seating_map.get((col_idx, row_idx))
                if student:
                    name = student.get('name', '').upper()
                    
                    # Show first + second name (same logic as PDF)
                    parts = name.split()
                    if len(parts) >= 2:
                        name = f"{parts[0]} {parts[1]}"
                        if len(name) > 16:
                            name = f"{parts[0]} {parts[1][0]}."
                    else:
                        name = parts[0] if parts else ""
                    
                    if len(name) > 18:
                        name = name[:17] + "."
                    
                    # Center text in desk
                    self.canvas.create_text(
                        curr_x + desk_w / 2,
                        curr_y + desk_h / 2,
                        text=name,
                        fill=Theme.TEXT_PRIMARY,
                        font=(Theme.FONT_FAMILY, name_font_size, "bold")
                    )
    
    def _draw_furniture(self, w, h, page_margin, furniture_margin,
                        has_top, has_bottom, has_left, has_right):
        """Desenha elementos de mobília com estilo moderno"""
        config = self.current_config
        
        def draw_furniture_label(text, side):
            """Desenha label de mobília com estilo card"""
            rect_w = 120
            rect_h = 28
            corner = 6
            
            if side == "Topo":
                cx = w / 2
                cy = page_margin + furniture_margin / 2
            elif side == "Fundo":
                cx = w / 2
                cy = h - page_margin - furniture_margin / 2
            elif side == "Esq":
                cx = page_margin + furniture_margin / 2
                cy = h / 2
                rect_w, rect_h = rect_h, rect_w  # Swap for vertical
            elif side == "Dir":
                cx = w - page_margin - furniture_margin / 2
                cy = h / 2
                rect_w, rect_h = rect_h, rect_w  # Swap for vertical
            else:
                return
            
            x1 = cx - rect_w / 2
            y1 = cy - rect_h / 2
            x2 = cx + rect_w / 2
            y2 = cy + rect_h / 2
            
            # Sombra
            shadow = 3
            self.canvas.create_rounded_rect(
                x1 + shadow, y1 + shadow, x2 + shadow, y2 + shadow,
                corner, fill=Theme.SHADOW_COLOR, outline=""
            )
            
            # Card
            self.canvas.create_rounded_rect(
                x1, y1, x2, y2,
                corner, fill=Theme.FURNITURE_FILL, outline=Theme.FURNITURE_BORDER,
                width=2
            )
            
            # Texto (com rotação se vertical) - TODOS usam PIL
            font_size = 10
            
            # Converter cor do tema para RGB
            color_hex = Theme.FURNITURE_TEXT
            if color_hex.startswith('#'):
                r_c = int(color_hex[1:3], 16)
                g_c = int(color_hex[3:5], 16)
                b_c = int(color_hex[5:7], 16)
                color = (r_c, g_c, b_c)
            else:
                color = (75, 85, 99)
            
            try:
                font = ImageFont.truetype("segoeuib.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("arialbd.ttf", font_size)
                except:
                    try:
                        font = ImageFont.truetype("arial.ttf", font_size)
                    except:
                        font = ImageFont.load_default()
            
            try:
                temp_img = Image.new('RGBA', (1, 1), (255, 255, 255, 0))
                temp_draw = ImageDraw.Draw(temp_img)
                bbox = temp_draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                img = Image.new('RGBA', (text_width + 10, text_height + 10), (255, 255, 255, 0))
                draw = ImageDraw.Draw(img)
                draw.text((5, 5), text, font=font, fill=color)
                
                is_vertical = side in ["Esq", "Dir"]
                if is_vertical:
                    img = img.rotate(-90, expand=True)
                
                photo = ImageTk.PhotoImage(img)
                self.canvas.create_image(cx, cy, image=photo)
                if not hasattr(self, '_text_images'):
                    self._text_images = []
                self._text_images.append(photo)
            except Exception as e:
                print(f"Erro ao criar texto: {e}")
                self.canvas.create_text(
                    cx, cy,
                    text=text,
                    fill=Theme.FURNITURE_TEXT,
                    font=(Theme.FONT_FAMILY, font_size, "bold")
                )
        
        # Desenha cada elemento
        if config.get("board") not in ["Nenhum", None, ""]:
            draw_furniture_label("QUADRO", config["board"])
        
        if config.get("door") not in ["Nenhum", None, ""]:
            draw_furniture_label("PORTA", config["door"])
        
        if config.get("windows") not in ["Nenhum", None, ""]:
            draw_furniture_label("JANELAS", config["windows"])


# Helper para desenhar retângulos com cantos arredondados no canvas
def _create_rounded_rect_coords(x1, y1, x2, y2, radius):
    """Gera coordenadas para um retângulo arredondado"""
    points = []
    
    # Top left
    points.extend([x1 + radius, y1])
    
    # Top right
    points.extend([x2 - radius, y1])
    points.extend([x2, y1])
    points.extend([x2, y1 + radius])
    
    # Bottom right
    points.extend([x2, y2 - radius])
    points.extend([x2, y2])
    points.extend([x2 - radius, y2])
    
    # Bottom left
    points.extend([x1 + radius, y2])
    points.extend([x1, y2])
    points.extend([x1, y2 - radius])
    
    # Back to top left
    points.extend([x1, y1 + radius])
    points.extend([x1, y1])
    points.extend([x1 + radius, y1])
    
    return points


# Adicionar método helper ao Canvas
def create_rounded_rect(self, x1, y1, x2, y2, radius=20, **kwargs):
    """Cria um retângulo com cantos arredondados"""
    if radius > (x2 - x1) / 2:
        radius = (x2 - x1) / 2
    if radius > (y2 - y1) / 2:
        radius = (y2 - y1) / 2
    
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    
    return self.create_polygon(points, **kwargs, smooth=True)


# Adiciona o método à classe Canvas
ctk.CTkCanvas.create_rounded_rect = create_rounded_rect
