from django.urls import path
from . import views
# from .views import ReminderView
# from .views import ReminderListAPIView

# URLConf
urlpatterns = [
    path('hello/', views.say_hello),
    path('api/tasks/', views.PatientTasksAPIView.as_view(), name='patient-tasks'),
    path('api/tasks/add/', views.AddTaskAPIView.as_view(), name='add-task'),
    path('api/tasks/<int:pk>/', views.TaskDetailAPIView.as_view(), name='task-detail'),
    path('api/tasks/<int:pk>/complete/', views.CompleteTaskAPIView.as_view(), name='complete-task'),

    # path('reminders/', ReminderView.as_view()),
    # path('reminders/patient/<int:patient_id>/', ReminderListAPIView.as_view(), name='reminder-list')

]

