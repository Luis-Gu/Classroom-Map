from fpdf import FPDF

class PDFExporter:
    @staticmethod
    def export(layout_config, seating_map, room_name, date_str, filename):
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        
        # Colors
        CLASS_A = (211, 47, 47) # Dark Red
        CLASS_B = (25, 118, 210) # Dark Blue
        
        # Font
        pdf.set_font("Helvetica", "B", 14)
        
        # Page Dimensions
        pw, ph = 297, 210
        margin = 15
        
        # 1. Header
        pdf.set_text_color(50, 50, 50)
        pdf.set_xy(0, 10)
        pdf.cell(pw, 10, f"MAPA DE SALA - {room_name.upper()}  |  DATA: {date_str}", align='C')
        
        # 2. Layout Calculation
        # Margins for furniture
        mt, mb, ml, mr = 30, 30, 30, 30
        
        avail_w = pw - ml - mr
        avail_h = ph - mt - mb
        
        rows_config = layout_config.get('rows', [7, 7, 7, 7])
        max_rows = max(rows_config)
        
        # Dimensions 
        unit_w = 16
        unit_h = 10 # Table
        unit_ch = 4 # Chair
        unit_gap = 1
        total_item_h = unit_h + unit_gap + unit_ch
        
        gap_x = 6
        gap_y = 5
        
        req_w = (4 * unit_w) + (3 * gap_x)
        req_h = (max_rows * total_item_h) + ((max_rows - 1) * gap_y)
        
        # Scaling
        scale = 1.0
        if req_w > avail_w or req_h > avail_h:
            scale = min(avail_w / req_w, avail_h / req_h)
            
        s_w = unit_w * scale
        s_h = unit_h * scale # Table
        s_ch = unit_ch * scale # Chair
        s_gap = unit_gap * scale
        s_total_h = total_item_h * scale
        
        s_gx = gap_x * scale
        s_gy = gap_y * scale
        
        # Center
        block_w = (4 * s_w) + (3 * s_gx)
        block_h = (max_rows * s_total_h) + ((max_rows - 1) * s_gy)
        
        ox = ml + (avail_w - block_w) / 2
        oy = mt + (avail_h - block_h) / 2
        
        # 3. Headers
        # Deduce names
        class_a_name = "TURMA 1"
        class_b_name = "TURMA 2"
        for r in range(rows_config[0]):
            s = seating_map.get((0, r))
            if s: class_a_name = s['class'].upper(); break
        for r in range(rows_config[1]):
            s = seating_map.get((1, r))
            if s: class_b_name = s['class'].upper(); break
            
        headers = [class_a_name, class_b_name, class_a_name, class_b_name]
        h_colors = [CLASS_A, CLASS_B, CLASS_A, CLASS_B]
        
        pdf.set_font("Helvetica", "B", 9 * scale)
        header_y = oy - (5 * scale)  # Mais perto das carteiras
        
        for i in range(4):
            hx = ox + (i * (s_w + s_gx))
            r, g, b = h_colors[i]
            pdf.set_text_color(r, g, b)
            pdf.set_xy(hx, header_y)
            # Truncar nome da turma se muito longo
            header_text = headers[i][:12] + "..." if len(headers[i]) > 12 else headers[i]
            pdf.cell(s_w, 5, header_text, align='C')
            
        pdf.set_text_color(0, 0, 0) # Reset
        
        # 4. Desks
        for col in range(4):
            seats = rows_config[col]
            cx = ox + (col * (s_w + s_gx))
            
            for row in range(seats):
                cy = oy + (row * (s_total_h + s_gy))
                
                # Table
                pdf.set_fill_color(255, 255, 255)
                pdf.set_draw_color(50, 50, 50)
                pdf.set_line_width(0.3)
                pdf.rect(cx, cy, s_w, s_h, 'DF')
                
                # Chair
                ch_w = s_w * 0.6
                ch_x = cx + (s_w - ch_w)/2
                ch_y = cy + s_h + s_gap
                pdf.set_fill_color(245, 245, 245)
                pdf.rect(ch_x, ch_y, ch_w, s_ch, 'DF')
                
                # Name
                student = seating_map.get((col, row))
                if student:
                    name = student.get('name', '').upper()
                    
                    # Truncar nome se muito longo (usar primeiro nome)
                    if len(name) > 10:
                        parts = name.split()
                        if parts:
                            name = parts[0]
                            if len(name) > 10:
                                name = name[:9] + "."
                    
                    font_size = 8 * scale
                    pdf.set_font("Helvetica", "B", font_size)
                    
                    pdf.set_xy(cx, cy + s_h/2 - (font_size * 0.35 / 2.8))
                    pdf.cell(s_w, s_h, name, align='C', border=0)

        # 5. Furniture Labels
        def draw_label(text, side):
            lw, lh = 30, 8
            bg = (255, 255, 255)
            
            # Coords default to top/left
            lx, ly = 0, 0
            is_vertical = False
            
            if side == "Topo":
                lx = pw / 2 - lw/2
                ly = mt / 2 
            elif side == "Fundo":
                lx = pw / 2 - lw/2
                ly = ph - mb/2
            elif side == "Esq":
                is_vertical = True
                # Para texto vertical, ajustar posição
                lx = ml / 2 - lh/2
                ly = ph/2 - lw/2
            elif side == "Dir":
                is_vertical = True
                lx = pw - ml/2 - lh/2
                ly = ph/2 - lw/2
            
            # Desenhar retângulo (com dimensões trocadas se vertical)
            pdf.set_fill_color(*bg)
            pdf.set_draw_color(0, 0, 0)
            pdf.set_line_width(0.3)
            
            if is_vertical:
                # Retângulo vertical (trocar largura/altura)
                pdf.rect(lx, ly, lh, lw, 'DF')
            else:
                # Retângulo horizontal
                pdf.rect(lx, ly, lw, lh, 'DF')
            
            # Desenhar texto
            pdf.set_font("Helvetica", "B", 8)
            
            if is_vertical:
                # Texto vertical - usar rotação
                center_x = lx + lh/2
                center_y = ly + lw/2
                
                # FPDF rotation: rotacionar 90 graus
                with pdf.rotation(90, center_x, center_y):
                    # Posicionar texto no centro do retângulo rotacionado
                    text_x = center_x - lw/2
                    text_y = center_y - lh/2
                    pdf.set_xy(text_x, text_y)
                    pdf.cell(lw, lh, text, align='C')
            else:
                # Texto horizontal normal
                pdf.set_xy(lx, ly)
                pdf.cell(lw, lh, text, align='C')

        if layout_config.get("board") not in ["Nenhum", None]:
            draw_label("QUADRO", layout_config["board"])
        if layout_config.get("door") not in ["Nenhum", None]:
            draw_label("PORTA", layout_config["door"])
        
        wins = layout_config.get("windows")
        if wins and wins != "Nenhum":
            draw_label("JANELAS", wins)
        
        pdf.output(filename)
