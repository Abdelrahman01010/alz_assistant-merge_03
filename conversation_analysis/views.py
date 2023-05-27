from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from django.shortcuts import render
from .diarization import main_function
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from django.utils import timezone # If you want to set a specific timestamp, you can use this module
import ffmpeg
from main.models import *
# Create your views here.
from main.models import Patient as PatientModel
from main.models import Conversation as ConversationModel

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from main.models import Conversation, Patient, Speaker

class check_audio_exists(APIView):
    def get(self, request):
        email = request.GET.get('email')

        try:
            patient = Patient.objects.get(email=email)
        except Patient.DoesNotExist:
            return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)
        
        flag = os.path.exists(str(patient.audio_path))
        
        return Response({'audio_flag': flag})

@csrf_exempt
def last_conversation_api(request):
    patient_email = request.GET.get('patient_email')
    speaker_id = request.GET.get('speaker_id')

    patient = get_object_or_404(Patient, email=patient_email)
    speaker = get_object_or_404(Speaker, id=speaker_id)

    conversation = Conversation.objects.filter(patient=patient, speaker=speaker).order_by('-conversation_timestamp').last()

    if conversation is None:
        return JsonResponse({'message': 'No conversation found for the specified patient and speaker.'}, status=404)

    response_data = {
        'conversation_text': conversation.conversation_text,
        'summarized_text': conversation.summarized_text,
        'conversation_timestamp': conversation.conversation_timestamp.isoformat(),
        'patient_email': conversation.patient.email,
        'speaker_id': conversation.speaker.id,
    }

    return JsonResponse(response_data)


class LastConversationView(APIView):
    def get(self, request):
        email = request.GET.get('email')
        try:
            patient = Patient.objects.get(email=email)
            last_conversation = patient.conversation_set.latest('conversation_timestamp')
            serializer = ConversationSerializer(last_conversation)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
        except Conversation.DoesNotExist:
            return Response({'error': 'No conversations found for this patient'}, status=status.HTTP_404_NOT_FOUND)

class ConversationAudioUploadView(APIView):
    def post(self, request):
        # Get patient email and audio file from request
        email = request.data.get('email')
        sp_id = request.data.get('speaker_id')
        audio_file = request.FILES.get('audio_file')

        # Get the patient from the email
        try:
            patient = PatientModel.objects.get(email=email)
        except PatientModel.DoesNotExist:
            return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create the directory for the conversation audio files if it doesn't exist
        conversation_audio_path = 'conversation_analysis/conversation_audio/'
        os.makedirs(conversation_audio_path, exist_ok=True)

        # Save the audio file with the name conversation00.wav
        filepath = os.path.join(conversation_audio_path, 'conversation00.aac')
        filepath_wav = os.path.join(conversation_audio_path, 'conversation00.wav')##
        with open(filepath, 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)
        # transcription
        stream = ffmpeg.input(filepath)
        stream = ffmpeg.output(stream, filepath_wav)
        ffmpeg.run(stream)
        Patient = f'conversation_analysis/patients_audio/patient_{patient.id}.wav'
        Conversation = 'conversation_analysis/conversation_audio/conversation00.wav'
        transcription = main_function(Patient, Conversation)

        # summarization
        model_name = "Lidiya/bart-large-xsum-samsum"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        # Tokenize the input text
        inputs = tokenizer(transcription, return_tensors='pt')

        # Generate the summary
        summary_ids = model.generate(
            inputs['input_ids'], num_beams=4, max_length=100, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        conversation = ConversationModel()
        conversation.conversation_text = transcription
        conversation.summarized_text = summary
        conversation.patient = patient
        conversation.conversation_timestamp = timezone.now()
        conversation.speaker = sp_id
        conversation.save()


        return Response({'success': f'File saved as {filepath}', 'summary': summary}, status=status.HTTP_201_CREATED)

class PatientAudioUploadView(APIView):
    def post(self, request):
        # Get patient email and audio file from request
        email = request.data.get('email')
        audio_file = request.FILES.get('audio_file')

        # Get the patient from the email
        try:
            patient = Patient.objects.get(email=email)
        except Patient.DoesNotExist:
            return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create the directory for the patient's audio files if it doesn't exist
        audio_path = 'conversation_analysis/patients_audio/'
        os.makedirs(audio_path, exist_ok=True)

        # Save the audio file with the patient's ID as the filename
        filename = f'patient_{patient.id}.wav'
        filepath = os.path.join(audio_path, filename)
        with open(filepath, 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

        filename_wav = f'patient{patient.id}.wav'
        filepath_wav = os.path.join(audio_path, filename_wav)
        stream = ffmpeg.input(filepath)
        stream = ffmpeg.output(stream, filepath_wav)
        ffmpeg.run(stream)
        # Update the patient's audio_path field in the database
        patient.audio_path = filepath_wav
        patient.save()

        return Response({'success': f'File saved as {filename}', 'audio_path': filepath}, status=status.HTTP_201_CREATED)

class GetPatientByEmail(APIView):
    def get(self, request):
        email = request.GET.get('email')

        try:
            patient = Patient.objects.get(email=email)
        except Patient.DoesNotExist:
            return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'patient_id': patient.id})

class GetCaregiverByEmail(APIView):
    def get(self, request):
        email = request.GET.get('email')

        try:
            caregiver = Caregiver.objects.get(email=email)
        except Caregiver.DoesNotExist:
            return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'caregiver_id': caregiver.id})

@csrf_exempt
def say_hello(request):
    return render(request, 'sumUp.html')

@csrf_exempt
def upload_audio(request):
    if request.method == 'POST':
        file = request.FILES['audio']
        filename = 'conversation00.wav'
        filepath = os.path.join('conversation_analysis',
                                'conversation_audio', filename)

        with open(filepath, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # transcription
        Patient = 'conversation_analysis/patients_audio/patient00.wav'
        Conversation = 'conversation_analysis/conversation_audio/conversation00.wav'
        transcription = main_function(Patient, Conversation)

        # summarization
        model_name = "Lidiya/bart-large-xsum-samsum"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        # Tokenize the input text
        inputs = tokenizer(transcription, return_tensors='pt')

        # Generate the summary
        summary_ids = model.generate(
            inputs['input_ids'], num_beams=4, max_length=100, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return JsonResponse({'transcription': transcription, 'summary': summary})

@csrf_exempt
def summarize(request):
    if request.method == 'POST':
        conversation_text = request.POST.get('conversation_text', '')
        if conversation_text:
            # Load the model and tokenizer
            model_name = "Lidiya/bart-large-xsum-samsum"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

            # Tokenize the input text
            inputs = tokenizer(conversation_text, return_tensors='pt')

            # Generate the summary
            summary_ids = model.generate(
                inputs['input_ids'], num_beams=4, max_length=100, early_stopping=True)
            summary = tokenizer.decode(
                summary_ids[0], skip_special_tokens=True)

            # Return the summary as JSON response
            return JsonResponse({'summary': summary})
        else:
            return JsonResponse({'error': 'conversation_text parameter is missing'}, status=400)
    else:
        return JsonResponse({'error': 'POST method is required'}, status=400)


from rest_framework import serializers
from main.models import Conversation, Patient

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ('summarized_text', 'conversation_timestamp')

class PatientSerializer(serializers.ModelSerializer):
    conversation_set = ConversationSerializer(many=True)

    class Meta:
        model = Patient
        fields = ('email', 'conversation_set')
