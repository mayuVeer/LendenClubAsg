from rest_framework import serializers
from .models import *
class StudentRelativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRelative
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('teacher_name', 'teacher_DOJ', 'teacher_salary','classroom','subject',)

class StudentSerializer(serializers.ModelSerializer):
    Relatives = StudentRelativeSerializer(many=True,read_only=True)


    class Meta:
        model = Student
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    subject_Teachers = TeacherSerializer(many=True, read_only=True)
    subject_Students = StudentSerializer(many=True, read_only=True)
    class Meta:
        model = Subject
        fields = ('subject_name','subject_chapters','subject_total_duration','subject_per_class_duration','subject_Teachers','subject_Students',)

class ShapeSerializer(serializers.ModelSerializer):
    class Meta:
        model= Shape
        fields = ('shape_name',)



class ClassroomSerializer(serializers.ModelSerializer):
    class_Students = StudentSerializer(many=True, read_only=True)
    class_Teachers = TeacherSerializer(many=True, read_only=True)
    class Meta:
        model = Classroom
        fields = ('class_name','class_seating_capacity','class_weblecture_support','class_shape_id','class_Teachers','class_Students',)
