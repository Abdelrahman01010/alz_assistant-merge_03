from django.shortcuts import render

# Create your views here.
def say_hello(request):
    return render(request, 'hello.html', {'name': 'Mosh'})


from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Patient, Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class PatientTasksAPIView(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        if email:
            try:
                patient = Patient.objects.get(email=email)
                tasks = Task.objects.filter(patient=patient)
                task_serializer = TaskSerializer(tasks, many=True)
                return Response(task_serializer.data)
            except Patient.DoesNotExist:
                return Response({'error': 'Patient not found.'}, status=404)
        else:
            return Response({'error': 'Email parameter is required.'}, status=400)

class AddTaskAPIView(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response({'task_id': task.id}, status=201)
        return Response(serializer.errors, status=400)


class TaskDetailAPIView(APIView):
    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            task.delete()
            return Response({'message': 'Task deleted successfully.'})
        except Task.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=404)


class CompleteTaskAPIView(APIView):
    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            task.is_completed = True
            task.save()
            return Response({'message': 'Task marked as completed.'})
        except Task.DoesNotExist:
            return Response({'error': 'Task not found.'}, status=404)



# from django.http import JsonResponse
# from django.views import View
# from django.utils import timezone
# from main.models import Reminder

# from rest_framework import generics
# from rest_framework.response import Response
# from .serializers import ReminderSerializer

# class ReminderView(View):
#     def get(self, request):
#         current_time = timezone.now()
#         reminders = Reminder.objects.filter(time__gte=current_time)  # Fetch reminders whose time is greater than or equal to current time
#         reminders_data = []  # List to store reminders data
#         for reminder in reminders:
#             # Create a dictionary to store reminder data
#             reminder_data = {
#                 'title': reminder.title,
#                 'description': reminder.description,
#                 'time': reminder.time.strftime('%Y-%m-%d %H:%M:%S'),  # Convert time to string format
#                 'caregiver': reminder.caregiver.first_name,  # Assuming Caregiver model has a 'name' field
#                 'patient': reminder.patient.first_name  # Assuming Patient model has a 'name' field
#             }
#             reminders_data.append(reminder_data)  # Append reminder data to the list
#         return JsonResponse({'reminders': reminders_data})  # Return reminders data as JSON response



# class ReminderListAPIView(generics.ListAPIView):
#     serializer_class = ReminderSerializer

#     def get_queryset(self):
#         patient_id = self.kwargs['patient_id']
#         queryset = Reminder.objects.filter(patient_id=patient_id)
#         return queryset
