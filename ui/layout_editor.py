import customtkinter as ctk
from .theme import Theme

class LayoutEditor(ctk.CTkFrame):
    def __init__(self, master, rows=14, cols=18, cell_size=40, **kwargs):
        super().__init__(master, **kwargs)
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid_data = {} # (row, col) -> "active" or "inactive"
        self.furniture = [] # list of dicts: {id, type, x, y, width, height, text}
        self.seating_map = {} # (row, col) -> {'name': str, 'class': str}
        
        self.drag_data = {"item": None, "x": 0, "y": 0}

        self.configure(fg_color=Theme.SURFACE, corner_radius=Theme.CORNER_RADIUS)

        # Canvas for the grid
        self.canvas_width = cols * cell_size
        self.canvas_height = rows * cell_size
        
        self.canvas = ctk.CTkCanvas(
            self,
            width=self.canvas_width,
            height=self.canvas_height,
            bg=Theme.SURFACE,
            highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=20)
        
        self.draw_grid()
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def draw_grid(self):
        self.canvas.delete("all")
        # Draw Grid Cells
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                state = self.grid_data.get((r, c), "inactive")
                
                if state == "active":
                    fill_color = Theme.ACTIVE_SEAT
                    outline_color = Theme.ACTIVE_SEAT
                    dash = None
                else:
                    fill_color = Theme.SURFACE
                    outline_color = Theme.INACTIVE_SEAT_OUTLINE
                    dash = (4, 4)
                
                self.canvas.create_rectangle(
                    x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                    fill=fill_color,
                    outline=outline_color,
                    width=2,
                    dash=dash,
                    tags=f"cell_{r}_{c}"
                )
                
                # Draw Student Name if occupied
                student = self.seating_map.get((r, c))
                if student and state == "active":
                    # Truncate name to fit
                    name = student['name']
                    short_name = name[:10] + "..." if len(name) > 10 else name
                    
                    self.canvas.create_text(
                        x1 + self.cell_size/2, 
                        y1 + self.cell_size/2,
                        text=short_name,
                        fill="white",
                        font=("Arial", 8, "bold"),
                        tags=f"text_{r}_{c}"
                    )
        
        # Draw Furniture
        for item in self.furniture:
            x, y = item['x'], item['y']
            w, h = item['width'], item['height']
            color = "#333333" if item['type'] == 'board' else "#666666"
            if item['type'] == 'door': color = "#8B4513"
            if item['type'] == 'window': color = "#87CEEB"
            
            # Draw rectangle
            self.canvas.create_rectangle(
                x, y, x + w, y + h,
                fill=color, outline="black", tags=f"furniture_{item['id']}"
            )
            # Draw Text
            self.canvas.create_text(
                x + w/2, y + h/2,
                text=item['text'], fill="white", font=("Arial", 10, "bold"),
                tags=f"furniture_{item['id']}"
            )

    def on_click(self, event):
        # Check if clicked on furniture
        clicked_item = None
        for item in reversed(self.furniture): # Check top-most first
            if (item['x'] <= event.x <= item['x'] + item['width'] and 
                item['y'] <= event.y <= item['y'] + item['height']):
                clicked_item = item
                break
        
        if clicked_item:
            self.drag_data["item"] = clicked_item
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
        else:
            # Grid interaction
            col = event.x // self.cell_size
            row = event.y // self.cell_size
            
            if 0 <= row < self.rows and 0 <= col < self.cols:
                current_state = self.grid_data.get((row, col), "inactive")
                new_state = "active" if current_state == "inactive" else "inactive"
                self.grid_data[(row, col)] = new_state
                self.draw_grid()

    def on_drag(self, event):
        item = self.drag_data["item"]
        if item:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            
            item['x'] += dx
            item['y'] += dy
            
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
            self.draw_grid()

    def on_release(self, event):
        self.drag_data["item"] = None

    def add_furniture(self, f_type):
        new_id = len(self.furniture) + 1
        width = 100
        height = 20
        text = f_type.capitalize()
        
        if f_type == "board":
            width, height = 150, 20
        elif f_type == "door":
            width, height = 40, 60
        elif f_type == "window":
            width, height = 60, 10
            
        self.furniture.append({
            "id": new_id,
            "type": f_type,
            "x": 50,
            "y": 50,
            "width": width,
            "height": height,
            "text": text
        })
        self.draw_grid()

    def set_seating(self, seating_map):
        self.seating_map = seating_map
        self.draw_grid()

    def get_layout(self):
        return {
            "grid": {f"{r},{c}": v for (r,c), v in self.grid_data.items()},
            "furniture": self.furniture,
            "dimensions": {"rows": self.rows, "cols": self.cols}
        }

    def set_layout(self, data):
        # Restore grid
        self.grid_data = {}
        for key, val in data.get("grid", {}).items():
            r, c = map(int, key.split(','))
            self.grid_data[(r, c)] = val
            
        self.furniture = data.get("furniture", [])
        self.draw_grid()
