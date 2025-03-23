from .models import Student
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password, make_password


class StudentRepository:
    def create_student(self, student_data):
        return Student.objects.create(**student_data)

    def get_student_by_id(self, student_id):
        return Student.objects.get(student_id=student_id, is_deleted=False)

    def list_students(self, query=None):
        students = Student.objects.filter(is_deleted=False)
        if query:
            students = students.filter(name__icontains=query)
        return students

    def update_student(self, student_id, updated_data):
        student = self.get_student_by_id(student_id)
        if not student:
            return None
        
        for key, value in updated_data.items():
            setattr(student, key, value)
        
        student.save()  # Save to commit changes
        return student

    def delete_student(self, student_id):
        student = self.get_student_by_id(student_id)
        if not student:
            return None
        
        student.is_deleted = True  # Mark as deleted without actually removing from DB
        student.save()  # Save to commit the change
        return student

