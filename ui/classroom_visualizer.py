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
        """Desenho principal da sala com estilo premium"""
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
        
        rows_config = self.current_config.get("rows", [7, 7, 7, 7])
        max_rows = max(rows_config)
        
        # === MARGENS E LAYOUT ===
        margin_top = 100  # Maior para dar espaço para mobília superior
        margin_bottom = 60
        margin_left = 60
        margin_right = 60
        
        avail_w = w - margin_left - margin_right
        avail_h = h - margin_top - margin_bottom
        
        # Dimensões base das carteiras (maiores para nomes caberem)
        item_w = 75
        item_h = 55
        gap_x = 15
        gap_y = 12
        
        # === ESCALA RESPONSIVA ===
        req_w = (4 * item_w) + (3 * gap_x)
        req_h = (max_rows * item_h) + ((max_rows - 1) * gap_y)
        
        scale = 1.0
        if req_w > avail_w or req_h > avail_h:
            scale_w = avail_w / req_w
            scale_h = avail_h / req_h
            scale = min(scale_w, scale_h, 1.0)
        
        scaled_w = item_w * scale
        scaled_h = item_h * scale
        scaled_gap_x = gap_x * scale
        scaled_gap_y = gap_y * scale
        
        # === CENTRALIZAÇÃO ===
        total_w = (4 * scaled_w) + (3 * scaled_gap_x)
        total_h = (max_rows * scaled_h) + ((max_rows - 1) * scaled_gap_y)
        
        offset_x = margin_left + (avail_w - total_w) / 2
        offset_y = margin_top + (avail_h - total_h) / 2
        
        # === CABEÇALHOS DAS COLUNAS ===
        self._draw_column_headers(offset_x, offset_y, scaled_w, scaled_gap_x, rows_config, scale)
        
        # === CARTEIRAS ===
        self._draw_desks(offset_x, offset_y, scaled_w, scaled_h, scaled_gap_x, scaled_gap_y, rows_config, scale)
        
        # === MOBÍLIA ===
        self._draw_furniture(w, h, margin_top, margin_bottom, margin_left, margin_right, scale)
        
        # Atualiza info no header
        total_students = len(self.seating_map)
        self.info_label.configure(text=f"{total_students} alunos")
    
    def _draw_column_headers(self, offset_x, offset_y, scaled_w, scaled_gap_x, rows_config, scale):
        """Desenha cabeçalhos das colunas com nome da turma (similar ao PDF)"""
        header_y = offset_y - 28 * scale  # Mais afastado da mobília superior
        
        # Pegar nomes das turmas do seating_map
        class_names = [None, None, None, None]  # 4 colunas
        class_colors = [
            Theme.CLASS_A_COLOR,
            Theme.CLASS_B_COLOR,
            Theme.CLASS_A_COLOR,
            Theme.CLASS_B_COLOR
        ]
        
        # Deduzir nomes das turmas
        for col_idx in range(4):
            for row_idx in range(rows_config[col_idx] if col_idx < len(rows_config) else 7):
                student = self.seating_map.get((col_idx, row_idx))
                if student:
                    class_names[col_idx] = student.get('class', '').upper()
                    break
        
        # Desenhar nome de cada coluna
        for col_idx in range(4):
            x = offset_x + (col_idx * (scaled_w + scaled_gap_x)) + (scaled_w / 2)
            name = class_names[col_idx] or ""
            color = class_colors[col_idx]
            
            if name:
                # Truncar nome se muito longo
                max_chars = 12
                if len(name) > max_chars:
                    name = name[:max_chars-1] + "..."
                
                font_size = max(int(10 * scale), 9)
                self.canvas.create_text(
                    x, header_y,
                    text=name,
                    fill=color,
                    font=(Theme.FONT_FAMILY, font_size, "bold")
                )
    
    def _draw_desks(self, offset_x, offset_y, scaled_w, scaled_h, scaled_gap_x, scaled_gap_y, rows_config, scale):
        """Desenha as carteiras com estilo moderno e sombras simuladas"""
        for col_idx in range(4):
            num_seats = rows_config[col_idx]
            curr_x = offset_x + (col_idx * (scaled_w + scaled_gap_x))
            
            for row_idx in range(num_seats):
                curr_y = offset_y + (row_idx * (scaled_h + scaled_gap_y))
                
                # Proporções da carteira
                table_h = 38 * scale
                chair_h = 16 * scale
                gap_part = 4 * scale
                
                # === SOMBRA (simulada com retângulo deslocado) ===
                shadow_offset = 3 * scale
                self.canvas.create_rectangle(
                    curr_x + shadow_offset,
                    curr_y + shadow_offset,
                    curr_x + scaled_w + shadow_offset,
                    curr_y + table_h + shadow_offset,
                    fill=Theme.SHADOW_COLOR,
                    outline=""
                )
                
                # === MESA ===
                self.canvas.create_rectangle(
                    curr_x, curr_y,
                    curr_x + scaled_w, curr_y + table_h,
                    fill=Theme.DESK_FILL,
                    outline=Theme.DESK_BORDER,
                    width=max(int(1 * scale), 1)
                )
                
                # === CADEIRA ===
                chair_w = 42 * scale
                chair_x = curr_x + (scaled_w - chair_w) / 2
                chair_y = curr_y + table_h + gap_part
                
                # Sombra da cadeira
                self.canvas.create_rectangle(
                    chair_x + shadow_offset / 2,
                    chair_y + shadow_offset / 2,
                    chair_x + chair_w + shadow_offset / 2,
                    chair_y + chair_h + shadow_offset / 2,
                    fill=Theme.SHADOW_COLOR,
                    outline=""
                )
                
                self.canvas.create_rectangle(
                    chair_x, chair_y,
                    chair_x + chair_w, chair_y + chair_h,
                    fill=Theme.CHAIR_FILL,
                    outline=Theme.DESK_BORDER,
                    width=max(int(1 * scale), 1)
                )
                
                # === NOME DO ALUNO ===
                student = self.seating_map.get((col_idx, row_idx))
                if student:
                    name = student.get('name', '').upper()
                    
                    # Truncar nome para caber na desk - limite bem restrito
                    max_chars = 18  # Limite fixo pequeno
                    
                    font_size = max(int(5 * scale), 5)  # Fonte pequena para caber na desk
                    
                    # Texto com nome
                    self.canvas.create_text(
                        curr_x + scaled_w / 2,
                        curr_y + table_h / 2,
                        text=name,
                        fill=Theme.TEXT_PRIMARY,
                        font=(Theme.FONT_FAMILY, font_size, "bold")
                    )
    
    def _draw_furniture(self, w, h, mt, mb, ml, mr, scale):
        """Desenha elementos de mobília com estilo moderno"""
        config = self.current_config
        
        def draw_furniture_label(text, side):
            """Desenha label de mobília com estilo card"""
            rect_w = 120 * scale  # Menor
            rect_h = 28 * scale   # Menor
            corner = 6 * scale
            
            # Posicionamento - móveis bem afastados para não sobrepor nome da turma
            if side == "Topo":
                cx, cy = w / 2, 25  # Fixo bem no topo
            elif side == "Fundo":
                cx, cy = w / 2, h - (mb / 2) + 5  # Um pouco mais para baixo
            elif side == "Esq":
                cx, cy = ml / 2, h / 2
                rect_w, rect_h = rect_h, rect_w  # Swap para vertical
            elif side == "Dir":
                cx, cy = w - (mr / 2), h / 2
                rect_w, rect_h = rect_h, rect_w  # Swap para vertical
            else:
                return
            
            x1 = cx - rect_w / 2
            y1 = cy - rect_h / 2
            x2 = cx + rect_w / 2
            y2 = cy + rect_h / 2
            
            # Sombra
            shadow = 4 * scale
            self.canvas.create_rounded_rect(
                x1 + shadow, y1 + shadow, x2 + shadow, y2 + shadow,
                corner, fill=Theme.SHADOW_COLOR, outline=""
            )
            
            # Card
            self.canvas.create_rounded_rect(
                x1, y1, x2, y2,
                corner, fill=Theme.FURNITURE_FILL, outline=Theme.FURNITURE_BORDER,
                width=max(int(2 * scale), 1)
            )
            
            # Texto (com rotação se vertical) - TODOS usam PIL para ficarem iguais
            font_size = max(int(11 * scale), 9)
            
            # Converter cor do tema para RGB
            color_hex = Theme.FURNITURE_TEXT
            if color_hex.startswith('#'):
                r = int(color_hex[1:3], 16)
                g = int(color_hex[3:5], 16)
                b = int(color_hex[5:7], 16)
                color = (r, g, b)
            else:
                color = (75, 85, 99)  # Fallback
            
            # Usar fonte do sistema (bold)
            try:
                font = ImageFont.truetype("segoeuib.ttf", font_size)  # Segoe UI Bold
            except:
                try:
                    font = ImageFont.truetype("arialbd.ttf", font_size)  # Arial Bold
                except:
                    try:
                        font = ImageFont.truetype("arial.ttf", font_size)
                    except:
                        font = ImageFont.load_default()
            
            try:
                # Criar imagem temporária para medir
                temp_img = Image.new('RGBA', (1, 1), (255, 255, 255, 0))
                temp_draw = ImageDraw.Draw(temp_img)
                bbox = temp_draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                # Criar imagem com texto
                img = Image.new('RGBA', (text_width + 10, text_height + 10), (255, 255, 255, 0))
                draw = ImageDraw.Draw(img)
                draw.text((5, 5), text, font=font, fill=color)
                
                is_vertical = side in ["Esq", "Dir"]
                if is_vertical:
                    # Rotacionar 90 graus para vertical
                    img = img.rotate(-90, expand=True)
                
                # Converter e desenhar
                photo = ImageTk.PhotoImage(img)
                self.canvas.create_image(cx, cy, image=photo)
                # Manter referência para evitar garbage collection
                if not hasattr(self, '_text_images'):
                    self._text_images = []
                self._text_images.append(photo)
            except Exception as e:
                # Fallback: texto horizontal se houver erro
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
    
    def _create_vertical_text_image(self, text, font_size, color):
        """Cria uma imagem com texto rotacionado 90 graus para elementos verticais"""
        try:
            # Usar fonte do sistema
            try:
                font = ImageFont.truetype("segoeui.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()
            
            # Criar imagem temporária para medir o texto
            temp_img = Image.new('RGBA', (1, 1), (255, 255, 255, 0))
            temp_draw = ImageDraw.Draw(temp_img)
            bbox = temp_draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Criar imagem com o texto horizontal
            img = Image.new('RGBA', (text_width + 10, text_height + 10), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            
            # Desenhar texto
            draw.text((5, 5), text, font=font, fill=color)
            
            # Rotacionar 90 graus no sentido horário
            img_rotated = img.rotate(-90, expand=True)
            
            # Converter para PhotoImage
            return ImageTk.PhotoImage(img_rotated)
        except Exception as e:
            print(f"Erro ao criar texto vertical: {e}")
            return None


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

