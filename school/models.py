from django.db import models

# Create your models here.
class Teacher(models.Model):
    teacher_name = models.CharField(max_length=10,null=False,unique=False)
    teacher_DOJ = models.DateTimeField(auto_now_add=True,null=False,unique=False)
    teacher_salary = models.DecimalField(max_digits=8,decimal_places=2)

    class Meta:
        db_table = "teacher"

class Student(models.Model):
    student_name = models.CharField(max_length=10,null=False,unique=False)
    student_DOJ = models.DateTimeField(auto_now_add=True,null=False,unique=False)
    student_standard = models.CharField(max_length=8,null=False,unique=False)
    student_rollno = models.IntegerField(null=False,unique=True)
    student_ranking = models.IntegerField(null=False)

    class Meta:
        db_table = "student"

class StudentRelative(models.Model):
    student_relative_name = models.CharField(max_length=10,null=False,unique=False)
    student_relative_phone_number=models.CharField(max_length=10,unique=True,null=False)
    student_relative_type = models.CharField(max_length=10,null=False,unique=False)
    student_id = models.ForeignKey(Student,on_delete=models.CASCADE, related_name='Relatives')

    class Meta:
        db_table = "student_relative"

class Shape(models.Model):
    shape_name = models.CharField(max_length=10,null=False,unique=True)

    class Meta:
        db_table = "shape"

class Classroom(models.Model):
    class_seating_capacity = models.IntegerField(null=False)
    class_weblecture_support = models.BooleanField(null=False)
    class_shape_id = models.ForeignKey(Shape,on_delete=models.CASCADE,related_name="Shapes")
    class_teachers= models.ManyToManyField(Teacher,related_name="class_Teachers")
    class_student = models.ManyToManyField(Student,related_name="class_Students")

    class Meta:
        db_table = "classroom"

class Subject(models.Model):
    subject_name = models.CharField(max_length=10,unique=True,null=False)
    subject_chapters = models.IntegerField(null=False)
    subject_total_duration = models.TimeField(null=False)
    subject_per_class_duration = models.TimeField(null=False)
    subject_teachers = models.ManyToManyField(Teacher, related_name="subject_Teachers")
    subject_student = models.ManyToManyField(Student, related_name="subject_Students")

    class Meta:
        db_table = "subject"
