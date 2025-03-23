from .repositories import  StudentRepository


class StudentService:
    def __init__(self):
        self.repo = StudentRepository()

    def add_student(self, student_data):
        return self.repo.create_student(student_data)
    
    def update_student(self, student_id, updated_data):
        # Fetch existing student details first
        student = self.repo.get_student_by_id(student_id)
        if not student:
            return {"error": "Student not found"}
        
        # Update the student details
        updated_student = self.repo.update_student(student_id, updated_data)
        return updated_student

    def list_students(self, query=None):
        return self.repo.list_students(query)

    def get_student_detail(self, student_id):
        # Fetch student details by ID
        student = self.repo.get_student_by_id(student_id)
        if not student:
            return {"error": "Student not found"}
        return student

    def delete_student(self, student_id):
        # Fetch existing student details first
        student = self.repo.get_student_by_id(student_id)
        if not student:
            return {"error": "Student not found"}
        
        # Delete the student
        self.repo.delete_student(student_id)
        return {"message": "Student deleted successfully"}
