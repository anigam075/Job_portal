from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('add_education/', AddEducationAPIView.as_view(), name='add_education'),
    path('add_job/', AddJobAPIView.as_view(), name='add_job'),
    path('user_info/', UserInfoAPIView.as_view(), name='user_info'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
]
