from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework import viewsets
# Create your views here.
class ClassDetailView(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

class ShapeDetailView(viewsets.ModelViewSet):
    queryset = Shape.objects.all()
    serializer_class = ShapeSerializer