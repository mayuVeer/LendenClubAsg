from rest_framework import serializers
from .models import *
class StudentRelativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRelative,
        fields = ('student_relative_name','student_relative_phone','student_relative_type','student_id',)

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ('class_seating_capacity','class_weblecture_support','class_shape_id','class_teachers','class_student',)

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('subject_name','subject_chapters','subject_total_duration','subject_per_class_duration','subject_teachers','subject_student',)

class ShapeSerializer(serializers.ModelSerializer):
    class Meta:
        model= Shape
        fields = ('shape_name',)

class StudentSerializer(serializers.ModelSerializer):
    Relatives = StudentRelativeSerializer(many=True,read_only=True)
    subject_Students = SubjectSerializer(many=True,read_only=True)
    class_Students = ClassroomSerializer(many=True,read_only=True)
    class Meta:
        model = Student
        fields = ('student_name','student_DOJ','student_standard','student_rollno','student_ranking','Relatives''subject_Students','class_Students',)

class TeacherSerializer(serializers.ModelSerializer):
    class_Teachers = ClassroomSerializer(many=True,read_only=True)
    subject_Teachers = SubjectSerializer(many=True,read_only=True)
    class Meta:
        model = Teacher
        fields = ('teacher_name','teacher_DOJ','teacher_salary','class_Teachers','subject_Teachers',)