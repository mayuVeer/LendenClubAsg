from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register(r'classroom_detail',views.ClassDetailView)
router.register(r'shape_detail',views.ShapeDetailView)
urlpatterns = [
    path('',include(router.urls)),
]