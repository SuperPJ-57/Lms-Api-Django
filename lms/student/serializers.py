from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Student
        fields = ['name','email','contact_number','department']

class StudentResponse(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ['student_id','name','email','contact_number','department']