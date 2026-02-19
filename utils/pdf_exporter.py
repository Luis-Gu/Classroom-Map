from fpdf import FPDF


class PDFExporter:
    @staticmethod
    def export(layout_config, seating_map, room_name, date_str, filename):
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_auto_page_break(auto=False)

        # Colors
        CLASS_A = (211, 47, 47)    # Dark Red
        CLASS_B = (25, 118, 210)   # Dark Blue

        # Page Dimensions (A4 Landscape)
        pw, ph = 297, 210

        # ── Margins: only enough room for furniture labels ──
        furniture_margin = 20  # space reserved for furniture labels on each side
        page_margin = 8        # tiny page edge margin

        # Determine which sides have furniture
        board_side = layout_config.get("board")
        door_side = layout_config.get("door")
        windows_side = layout_config.get("windows")

        has_top = board_side == "Topo" or door_side == "Topo" or windows_side == "Topo"
        has_bottom = board_side == "Fundo" or door_side == "Fundo" or windows_side == "Fundo"
        has_left = board_side == "Esq" or door_side == "Esq" or windows_side == "Esq"
        has_right = board_side == "Dir" or door_side == "Dir" or windows_side == "Dir"

        mt = page_margin + (furniture_margin if has_top else 0) + 14  # +14 for room name header
        mb = page_margin + (furniture_margin if has_bottom else 0)
        ml = page_margin + (furniture_margin if has_left else 0)
        mr = page_margin + (furniture_margin if has_right else 0)

        # ── 1. Room Name (Top Right) ──
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(50, 50, 50)
        room_text = room_name.upper()
        text_w = pdf.get_string_width(room_text) + 4
        pdf.set_xy(pw - text_w - page_margin, page_margin)
        pdf.cell(text_w, 10, room_text, align='R')

        # ── 2. Layout Calculation - DYNAMIC SIZING ──
        rows_config = layout_config.get('rows', [7, 7, 7, 7])
        max_rows = max(rows_config)
        num_cols = 4

        avail_w = pw - ml - mr
        avail_h = ph - mt - mb

        # Proportions: corridor gap = 40% of desk width, row gap = 30% of desk height
        # chair_h = 30% of desk_h, chair_gap = 5% of desk_h
        corridor_ratio = 0.30   # gap_x as fraction of desk width
        row_gap_ratio = 0.25    # gap_y as fraction of total item height
        chair_h_ratio = 0.28    # chair height as fraction of desk height
        chair_gap_ratio = 0.08  # gap between desk and chair

        # Solve for desk width:
        # avail_w = 4 * desk_w + 3 * (corridor_ratio * desk_w)
        # avail_w = desk_w * (4 + 3 * corridor_ratio)
        desk_w = avail_w / (num_cols + (num_cols - 1) * corridor_ratio)

        # Solve for desk height:
        # total_item_h = desk_h + chair_gap + chair_h = desk_h * (1 + chair_gap_ratio + chair_h_ratio)
        # avail_h = max_rows * total_item_h + (max_rows - 1) * row_gap
        # row_gap = row_gap_ratio * total_item_h
        # avail_h = total_item_h * (max_rows + (max_rows - 1) * row_gap_ratio)
        # total_item_h = avail_h / (max_rows + (max_rows - 1) * row_gap_ratio)
        total_item_h = avail_h / (max_rows + (max_rows - 1) * row_gap_ratio)

        desk_h = total_item_h / (1 + chair_gap_ratio + chair_h_ratio)
        chair_h = desk_h * chair_h_ratio
        chair_gap = desk_h * chair_gap_ratio

        gap_x = desk_w * corridor_ratio
        gap_y = total_item_h * row_gap_ratio

        # Cap maximum desk size so it doesn't look absurdly large with few rows
        max_desk_w = 50
        max_desk_h = 18
        if desk_w > max_desk_w:
            desk_w = max_desk_w
            gap_x = desk_w * corridor_ratio
        if desk_h > max_desk_h:
            desk_h = max_desk_h
            chair_h = desk_h * chair_h_ratio
            chair_gap = desk_h * chair_gap_ratio
            total_item_h = desk_h + chair_gap + chair_h
            gap_y = total_item_h * row_gap_ratio

        # Recalculate total block size for centering
        block_w = (num_cols * desk_w) + ((num_cols - 1) * gap_x)
        block_h = (max_rows * total_item_h) + ((max_rows - 1) * gap_y)

        ox = ml + (avail_w - block_w) / 2
        oy = mt + (avail_h - block_h) / 2

        # ── 3. Column Headers (class names) ──
        class_a_name = "TURMA 1"
        class_b_name = "TURMA 2"
        for r in range(rows_config[0]):
            s = seating_map.get((0, r))
            if s:
                class_a_name = s['class'].upper()
                break
        for r in range(rows_config[1]):
            s = seating_map.get((1, r))
            if s:
                class_b_name = s['class'].upper()
                break

        headers = [class_a_name, class_b_name, class_a_name, class_b_name]
        h_colors = [CLASS_A, CLASS_B, CLASS_A, CLASS_B]

        header_font_size = min(10, desk_w * 0.4)
        pdf.set_font("Helvetica", "B", header_font_size)
        header_y = oy - header_font_size * 0.5 - 2

        for i in range(num_cols):
            hx = ox + (i * (desk_w + gap_x))
            r, g, b = h_colors[i]
            pdf.set_text_color(r, g, b)
            pdf.set_xy(hx, header_y)
            header_text = headers[i][:14] if len(headers[i]) <= 14 else headers[i][:13] + "."
            pdf.cell(desk_w, header_font_size * 0.4, header_text, align='C')

        pdf.set_text_color(0, 0, 0)

        # ── 4. Draw Desks ──
        # Font size scales with desk dimensions
        name_font_size = min(10, max(6, desk_w * 0.35))

        for col in range(num_cols):
            seats = rows_config[col]
            cx = ox + (col * (desk_w + gap_x))

            for row in range(seats):
                cy = oy + (row * (total_item_h + gap_y))

                # Table
                pdf.set_fill_color(255, 255, 255)
                pdf.set_draw_color(50, 50, 50)
                pdf.set_line_width(0.3)
                pdf.rect(cx, cy, desk_w, desk_h, 'DF')

                # Chair
                ch_w = desk_w * 0.55
                ch_x = cx + (desk_w - ch_w) / 2
                ch_y = cy + desk_h + chair_gap
                pdf.set_fill_color(245, 245, 245)
                pdf.rect(ch_x, ch_y, ch_w, chair_h, 'DF')

                # Student Name
                student = seating_map.get((col, row))
                if student:
                    name = student.get('name', '').upper()

                    # Show first + second name
                    parts = name.split()
                    if len(parts) >= 2:
                        name = f"{parts[0]} {parts[1]}"
                        # If still too long, abbreviate second name
                        if len(name) > 16:
                            name = f"{parts[0]} {parts[1][0]}."
                    else:
                        name = parts[0] if parts else ""

                    if len(name) > 18:
                        name = name[:17] + "."

                    pdf.set_font("Helvetica", "B", name_font_size)
                    pdf.set_text_color(0, 0, 0)

                    # Center text vertically inside desk
                    font_h = name_font_size * 0.35
                    text_y = cy + (desk_h - font_h) / 2
                    pdf.set_xy(cx, text_y)
                    pdf.cell(desk_w, font_h, name, align='C', border=0)

        # ── 5. Furniture Labels ──
        def draw_label(text, side):
            lw, lh = 32, 9
            bg = (255, 255, 255)
            is_vertical = False

            if side == "Topo":
                lx = pw / 2 - lw / 2
                ly = page_margin
            elif side == "Fundo":
                lx = pw / 2 - lw / 2
                ly = ph - page_margin - lh
            elif side == "Esq":
                is_vertical = True
                lx = page_margin
                ly = ph / 2 - lw / 2
            elif side == "Dir":
                is_vertical = True
                lx = pw - page_margin - lh
                ly = ph / 2 - lw / 2
            else:
                return

            pdf.set_fill_color(*bg)
            pdf.set_draw_color(0, 0, 0)
            pdf.set_line_width(0.3)

            if is_vertical:
                pdf.rect(lx, ly, lh, lw, 'DF')
            else:
                pdf.rect(lx, ly, lw, lh, 'DF')

            pdf.set_font("Helvetica", "B", 8)
            pdf.set_text_color(0, 0, 0)

            if is_vertical:
                center_x = lx + lh / 2
                center_y = ly + lw / 2
                with pdf.rotation(90, center_x, center_y):
                    pdf.set_xy(center_x - lw / 2, center_y - lh / 2)
                    pdf.cell(lw, lh, text, align='C')
            else:
                pdf.set_xy(lx, ly)
                pdf.cell(lw, lh, text, align='C')

        if board_side not in ["Nenhum", None, ""]:
            draw_label("QUADRO", board_side)
        if door_side not in ["Nenhum", None, ""]:
            draw_label("PORTA", door_side)
        if windows_side and windows_side != "Nenhum":
            draw_label("JANELAS", windows_side)

        pdf.output(filename)
