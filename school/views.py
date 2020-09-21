from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django.db.models import Sum,Count
import logging,traceback
# Create your views here.
logger = logging.getLogger('django')

class ClassDetailView(viewsets.ModelViewSet):
    logger.info("Class detail view is running",exc_info=True)
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    logger.info("Class detail view has ended",exc_info=True)

class ShapeDetailView(viewsets.ModelViewSet):
    logger.info("Shape detail view is running", exc_info=True)
    queryset = Shape.objects.all()
    serializer_class = ShapeSerializer
    logger.info("Shape detail view has ended", exc_info=True)

class SubjectDetailView(viewsets.ModelViewSet):
    logger.info("Subject detail view is running", exc_info=True)
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    logger.info("Subject detail view has ended", exc_info=True)

class TeacherDetailView(viewsets.ModelViewSet):
    logger.info("Teacher detail view is running", exc_info=True)
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    logger.info("Teacher detail view has ended", exc_info=True)

class StudentDetailView(viewsets.ModelViewSet):
    logger.info("Student detail view is running", exc_info=True)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    def create(self, request, *args, **kwargs):
         Relatives= request.data.pop('Relatives')
         student = request.data
         classes = Classroom.objects.filter(id__in=request.data.pop('class_student'))
         subjects = Subject.objects.filter(id__in=request.data.pop('subject_student'))
         stud_created = Student.objects.create(**student)
         logger.info(stud_created.student_name," has inserted in student")
         if classes == [] and subjects == []:
             logger.error("Classes and subjects choosen are not valid")
             return Response("Classes and subjects choosen are not valid")
         elif classes == [] and subjects != []:
             logger.error("Classes are not valid")
             return Response("Classes are not valid")
         else:
             if subjects == [] and classes != []:
                 logger.error("Subjects are not valid")
                 return Response("Subjects are not valid")
         stud_created.class_student.set(classes)
         stud_created.subject_student.set(subjects)
         bulk_list_stud_rel=[]
         for Relative in Relatives:
             stud_rel = {'student_id':stud_created}
             Relative.update(stud_rel)
             rel_created = StudentRelative(**Relative)
             bulk_list_stud_rel.append(rel_created)
         StudentRelative.objects.bulk_create(bulk_list_stud_rel)
         logger.info(bulk_list_stud_rel,"Relatives are added in ",stud_created.student_name)
         logger.info("Student detail view has ended", exc_info=True)
         return Response(StudentSerializer.data)
    logger.info("Student detail view has ended", exc_info=True)

@api_view(['GET'])
def statementTwo(request,t_name):
    logger.info("Statement Two is running", exc_info=True)
    students = Student.objects.distinct().prefetch_related('class_student').filter(class_student__class_Teachers__teacher_name=t_name)
    student_serializer = StudentSerializer(students,many=True)
    if student_serializer.data == []:
        logger.warning("No records found in statement Two")
        return Response("No records found",status=404)
    logger.info("Statement Two has ended", exc_info=True)
    return Response(student_serializer.data)

@api_view(['GET'])
def statementThree(request,t_name):
    logger.info("Statement Three is running", exc_info=True)
    student_count = Student.objects.distinct().prefetch_related('class_student').filter(class_student__class_Teachers__teacher_name=t_name,class_student__class_Teachers__teacher_salary__gt=100000).count()
    if student_count == 0:
        logger.warning("No records found in statement three")
        return Response("No records found",status=404)
    sum_salary = Student.objects.distinct().prefetch_related('class_student').filter(class_student__class_Teachers__teacher_name=t_name,class_student__class_Teachers__teacher_salary__gt=100000).aggregate(total=Sum('class_student__class_Teachers__teacher_salary'))
    students = Student.objects.distinct().prefetch_related('class_student').filter(class_student__class_Teachers__teacher_name=t_name,class_student__class_Teachers__teacher_salary__gt=100000)
    student_name = [{student.student_name} for student in students]
    response = {
        'teacher_name': t_name,
        'students': student_name,
        'total_count': student_count,
        'sum':sum_salary
    }
    logger.info("Statement Three has ended", exc_info=True)
    return Response(response)

@api_view(['GET'])
def statementFour(request):
    logger.info("Statement Four is running",exc_info=True)
    subjects = Subject.objects.distinct().prefetch_related('subject_Teachers').annotate(co = Count('subject_Teachers')).filter(co__gte = 2).annotate(Number_of_teachers = Count('subject_Teachers__id'),Number_of_students=Count('subject_Students__id'))
    response = [ {'Subject_name':sub.subject_name,'Number_of_teachers':sub.Number_of_teachers,'Number_of_students':sub.Number_of_students,'total_hour':sub.subject_total_duration}  for sub in subjects]
    logger.info("Statement Four has ended", exc_info=True)
    return Response(response)