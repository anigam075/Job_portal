from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'jobs', JobSearchAPIView, basename='jobs')

urlpatterns = [
    path('', index, name='home'),    
    path('', include(router.urls)),    
]