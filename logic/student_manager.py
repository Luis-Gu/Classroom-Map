class StudentManager:
    def __init__(self):
        self.classes = {} # class_name -> list of students

    def parse_input(self, data):
        """
        Parses the dictionary from Sidebar.get_data()
        data format: {'classes': {'Class A': ['Name 1', 'Name 2'], ...}}
        """
        self.classes = data.get('classes', {})
        
    def get_all_students(self):
        """
        Returns a flat list of items: {'name': name, 'class': class_name}
        """
        all_students = []
        for class_name, students in self.classes.items():
            for student in students:
                all_students.append({'name': student, 'class': class_name})
        return all_students

    def get_student_count(self):
        return sum(len(s) for s in self.classes.values())
