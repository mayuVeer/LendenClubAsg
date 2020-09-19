from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.db.models import Sum,Count
# Create your views here.
class ClassDetailView(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

class ShapeDetailView(viewsets.ModelViewSet):
    queryset = Shape.objects.all()
    serializer_class = ShapeSerializer

class SubjectDetailView(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class TeacherDetailView(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class StudentDetailView(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    def create(self, request, *args, **kwargs):
         Relatives= request.data.pop('Relatives')
         student = request.data
         classes = Classroom.objects.filter(id__in=request.data.pop('class_student'))
         subjects = Subject.objects.filter(id__in=request.data.pop('subject_student'))
         stud_created = Student.objects.create(**student)
         stud_created.class_student.set(classes)
         stud_created.subject_student.set(subjects)
         bulk_list_stud_rel=[]
         for Relative in Relatives:
             stud_rel = {'student_id':stud_created}
             Relative.update(stud_rel)
             rel_created = StudentRelative(**Relative)
             bulk_list_stud_rel.append(rel_created)
         StudentRelative.objects.bulk_create(bulk_list_stud_rel)
         return Response(StudentSerializer.data)

@api_view(['GET'])
def statementTwo(request,t_name):
    name = t_name
    students = Student.objects.distinct().prefetch_related('class_student').filter(class_student__class_Teachers__teacher_name=name)
    student_serializer = StudentSerializer(students,many=True)
    return Response(student_serializer.data)

@api_view(['GET'])
def statementThree(request,t_name):
    name = t_name
    student_count = Student.objects.distinct().prefetch_related('class_student').filter(class_student__class_Teachers__teacher_name=name,class_student__class_Teachers__teacher_salary__gt=100000).count()
    sum_salary = Student.objects.distinct().prefetch_related('class_student').filter(class_student__class_Teachers__teacher_name=name,class_student__class_Teachers__teacher_salary__gt=100000).aggregate(total=Sum('class_student__class_Teachers__teacher_salary'))
    students = Student.objects.distinct().prefetch_related('class_student').filter(class_student__class_Teachers__teacher_name=name,class_student__class_Teachers__teacher_salary__gt=100000)
    student_name = [{student.student_name} for student in students]
    response = {
        'teacher_name': name,
        'students': student_name,
        'total_count': student_count,
        'sum':sum_salary
    }
    return Response(response)

@api_view(['GET'])
def statementFour(request):
    subjects = Subject.objects.distinct().prefetch_related('subject_Teachers').annotate(co = Count('subject_Teachers')).filter(co__gte = 2).annotate(Number_of_teachers = Count('subject_Teachers__id'),Number_of_students=Count('subject_Students__id'))
    response = [ {'Number_of_teachers':sub.Number_of_teachers,'Number_of_students':sub.Number_of_students,'total_hour':sub.subject_total_duration}  for sub in subjects]
    return Response(response)