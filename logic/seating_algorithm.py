import random

class SeatingAlgorithm:
    def __init__(self):
        pass

    def generate_seating(self, layout_config, student_manager):
        """
        layout_config: dict {'rows': [n1, n2, n3, n4], ...}
        student_manager: instance of StudentManager
        
        Returns: dict { (col_idx, row_idx): {'name': str, 'class': str} }
        """
        # 1. Get capacity per column
        rows_per_col = layout_config.get('rows', [0,0,0,0])
        
        # 2. Get students
        classes = student_manager.classes # dict {name: [list]}
        class_names = sorted(list(classes.keys())) # Sort to ensure consistent order (Class A, Class B)
        # If user didn't name them A/B, we just take keys.
        
        if not class_names:
            return {}
            
        # Shuffle students within classes
        for name in class_names:
            random.shuffle(classes[name])
            
        seating_map = {}
        
        # 3. Column Distribution Strategy
        # Assign classes to columns in round-robin:
        # Col 0 -> Class 0
        # Col 1 -> Class 1
        # Col 2 -> Class 0 (if only 2 classes)
        # ...
        
        num_classes = len(class_names)
        
        for col_idx in range(4): # Fixed 4 columns
            capacity = rows_per_col[col_idx]
            if capacity <= 0: continue
            
            # Determine which class goes here
            class_idx = col_idx % num_classes
            class_name = class_names[class_idx]
            student_list = classes[class_name]
            
            # Fill column
            for row_idx in range(capacity):
                if not student_list:
                    break # No more students in this class
                
                # Pop student
                student_name = student_list.pop(0) 
                # Note: This modifies the list in place!
                # Since we might need students for next column (e.g. Col 2 uses Class A again),
                # popping is correct because we don't want to place the same student twice.
                
                seating_map[(col_idx, row_idx)] = {
                    'name': student_name,
                    'class': class_name
                }
                
        return seating_map
