from django.urls import path
from .views import TaskCreateView, verify_task


urlpatterns = [
    path('', TaskCreateView.as_view(), name ='home'),
    path('verify/<str:id>/', verify_task, name ='verify_task'),
]