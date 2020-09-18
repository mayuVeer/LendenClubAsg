from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register(r'classroom_detail',views.ClassDetailView)
router.register(r'shape_detail',views.ShapeDetailView)
router.register(r'subject_detail',views.SubjectDetailView)
router.register(r'teacher_detail',views.TeacherDetailView)
router.register(r'student_detail',views.StudentDetailView)
urlpatterns = [
    path('',include(router.urls)),
    path('statement-two/<str:username>',views.statementTwo)
]