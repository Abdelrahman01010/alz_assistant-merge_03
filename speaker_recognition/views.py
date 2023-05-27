from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.shortcuts import render
import face_recognition
import os
import cv2
from main.models import Speaker, Caregiver,Patient
from .serializers import  CaregiverSerializer,SpeakerSerializer,PatientSerializer
from rest_framework import status
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .Tokens import create_jwt_pair_for_user
import jwt
import base64
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .serializers import CaregiverTokenObtainPairSerializer
from speaker_recognition.backends import CaregiverBackend,PatientBackend
from speaker_recognition.auth import JWTAuthentication,PJWTAuthentication
from rest_framework.permissions import BasePermission
import json
from rest_framework.permissions import BasePermission
from django import forms
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from speaker_recognition.check import check_if_patient_exist



class IsCaregiverAuthenticated(BasePermission):
    #  Allows access only to authenticated Caregivers.
    def has_permission(self, request, view):
        return request.user is not None and isinstance(request.user,Caregiver)



class IsPatientAuthenticated(BasePermission):
    #  Allows access only to authenticated patients.
    def has_permission(self, request, view):
        return request.user is not None and isinstance(request.user,Patient)








class CaregiverAddNewSpeaker(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCaregiverAuthenticated]
    def post(self, request, format=None):
        
        image_file = request.FILES.get('picture') #Add Speaker image
        speaker_name = request.POST.get('recognized_name') #Add speaker name
        relationship=request.POST.get('relationship') #Add relationship
        token = request.auth
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        caregiver_id = payload['user_id']
        caregiver = Caregiver.objects.get(id=caregiver_id) #Get Caregiver id
        error_response = check_if_patient_exist(caregiver)
        if error_response:
            return error_response
        speaker_instance = Speaker(recognized_name=speaker_name, caregiver=caregiver, img_path=image_file,relationship=relationship,is_recognized=True)
        speaker_instance.save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

    def get(self, request, format=None):
        return Response({'status': 'error', 'message': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)






   
def facedect(images,filename,names): #Face recognition function 
   path='media/'
   users_images=[]
   users_names=names
   for img in images:
            curImg=cv2.imread(f'{path}\{img}')
            users_images.append(curImg)
   patient_img=cv2.imread(f'{path}\{filename}')
   Encode_list=Encoding(users_images)
   face_1_face_encoding = face_recognition.face_encodings(patient_img)
   checks=face_recognition.compare_faces(face_1_face_encoding[0], Encode_list)
   if True in checks:
      first_match_index = checks.index(True)
      return(users_names[first_match_index])
   else:
       return('Unknown')
    
    
def Encoding(images):  #Function for encoding all images in database
        imgEncodings=[]
        for img in images:
            Encodeimg=face_recognition.face_encodings(img)[0]
            imgEncodings.append(Encodeimg)
        return imgEncodings




class SpeakerImageView(APIView):
   def get(self, request):
      query_set=Speaker.objects.all()
      speaker_serializer=SpeakerSerializer(query_set,many=True)
      return Response(speaker_serializer.data)
   def post(self, request):
        print('I am here') 
        file_obj = request.data['picture']
        id = request.data['id']
        idd = Caregiver.objects.get(id=id)
        image = Speaker(caregiver=idd,img_path=file_obj)
        image.save()
        return Response({'status': 'success'})







class PatientImageView(APIView):
   def get(self, request):
      query_set=Patient.objects.all()
      patient_serializer=PatientSerializer(query_set,many=True)
      return Response(patient_serializer.data)



class Logincaregiver(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCaregiverAuthenticated]
    def post(self, request):
        try:
            token = request.auth
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            caregiver_id = payload['user_id']
            caregiver = Caregiver.objects.get(id=caregiver_id) #Get Caregiver id
            return JsonResponse({'email':caregiver.email})
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)



class Loginpatient(APIView):
    authentication_classes = [PJWTAuthentication]
    permission_classes = [IsPatientAuthenticated]
    def post(self, request):
        try:
            token = request.auth
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            patient_id = payload['user_id']
            patient = Patient.objects.get(id=patient_id) #Get Caregiver id
            return JsonResponse({'email':patient.email})
          
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)







class GalleryAddedByCaregiver(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCaregiverAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            token = request.auth
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            caregiver_id = payload['user_id']
            caregiver=Caregiver.objects.get(id=caregiver_id)
            speakers = Speaker.objects.filter(caregiver=caregiver).values('id','img_path','recognized_name','relationship')
            return JsonResponse(list(speakers), safe=False)
        except Speaker.DoesNotExist:
            return JsonResponse({'message': 'Caregiver with id {} not found'.format(id)}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)






class SpeakerEdit(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCaregiverAuthenticated]
    def put(self, request, speaker_id):
        speaker = Speaker.objects.get(id=speaker_id)
        data = request.data
        if 'recognized_name' in data:
            speaker.recognized_name = data['recognized_name']
        if 'relationship' in data:
            speaker.relationship = data['relationship']
        speaker.save()
        return Response({'message': f'Speaker with id {speaker_id} has been updated'}, status=status.HTTP_200_OK)


# class CaregiverAddNewSpeakerView(APIView):
#     def post(self, request, id):
#         try:
#             image_file = request.FILES.get('picture') #Add Speaker image
#             speaker_name = request.POST.get('name') #Add speaker name
#             caregiver = Caregiver.objects.get(id=id) #Get Caregiver id
#             speaker_instance = Speaker(recognized_name=speaker_name,caregiver=caregiver, img_path=image_file)
#             speaker_instance.save()
#             return JsonResponse({'status': 'success'})
#         except :
#             return JsonResponse({'status': 'error', 'message': 'Caregiver with the specified ID does not exist.'})
        


class SpeakerDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCaregiverAuthenticated]
    def delete(self, request, speaker_id):
        speaker = Speaker.objects.filter(id=speaker_id)
        speaker.delete()
        return Response({'message': f'Speaker with id {speaker_id} has been deleted'}, status=status.HTTP_204_NO_CONTENT)
    



class caregiverLogin(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        caregiver = CaregiverBackend().authenticate(request=request, email=email, password=password)
        token = CaregiverBackend().generate_token(caregiver)
        return Response(token)




class patientLogin(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        patient = PatientBackend().authenticate(request=request, email=email, password=password)
        token = PatientBackend().generate_token(patient)
        return Response(token)
    
    


class MyCargiver_id(APIView):
   authentication_classes = [JWTAuthentication]
   permission_classes = [IsCaregiverAuthenticated]
   def get(self, request):
        token = request.auth
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        caregiver_id = payload['user_id']
        query_set=Caregiver.objects.get(pk=caregiver_id)
        cargiver_serializer=CaregiverSerializer(query_set)
        return Response(cargiver_serializer.data)  



class Mypatient_id(APIView):
   authentication_classes = [PJWTAuthentication]
   permission_classes = [IsPatientAuthenticated]
   def get(self, request):
        token = request.auth
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        patient_id = payload['user_id']
        
        query_set=Patient.objects.get(pk=patient_id)
        patient_serializer=PatientSerializer(query_set)
        return Response(patient_serializer.data)  

class upload_image(APIView):
    authentication_classes = [PJWTAuthentication]
    permission_classes = [IsPatientAuthenticated]
    def post(self,request): 
        users_images_paths=[]
        users_names=[]
        response_data = []
        token = request.auth
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        id = payload['user_id']
        image_file = request.data['picture'] # Image uploaded by Patient
        patient=Patient.objects.get(id=id) #Get Patient id from url 
        if image_file:
           filename = default_storage.save('images/' + image_file.name, image_file) #Store image in Images folder
           caregiver_id=patient.caregiver #Get Patient's Caregiver id
           images=Speaker.objects.filter(caregiver=caregiver_id) #Get all images uploaded by Caregiver
           names=Speaker.objects.filter(caregiver=caregiver_id)  #Get all names uploaded by Caregiver
           for name in names:
             users_names.append(name.recognized_name) 
           for image in images: #Here i get images that caregiver 
             users_images_paths.append(image.img_path)
           result=facedect(users_images_paths,filename,users_names)
           print(result)
           #get relationship using name and caregiver_id
           if result == 'Unknown':
               response_data.append({
                'status': 'success',
                'url':  default_storage.url(filename),
                'name': result,
                })
                
           else :
            speaker=Speaker.objects.get(caregiver=caregiver_id,recognized_name=result)
            Relationship=speaker.relationship
            print(Relationship)
            print(speaker.pk)
            response_data.append({
                'status': 'success',
                'url':  default_storage.url(filename),
                'name': result,
                'relationship':Relationship,
                'id':speaker.pk,
                })
        return JsonResponse(list(response_data), safe=False)
        # else:
        #     return JsonResponse({'status': 'error', 'message': 'No image file uploaded.'})
        







class CaregiverSignupView(APIView):
    authentication_classes = []  # disable authentication for this view
    permission_classes = [AllowAny] 
    def post(self, request, format=None):
        
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        
        if not email or not password or not first_name or not last_name:
            return Response({'error': 'Please provide all required fields'}, status=status.HTTP_400_BAD_REQUEST)

        caregiver = Caregiver.objects.create(email=email, first_name=first_name, last_name=last_name,password=password)
        
        caregiver.save()

        return Response({'message': 'Caregiver created successfully'}, status=status.HTTP_201_CREATED)
    






    
class PatientSignupView(APIView):
    authentication_classes = []  # disable authentication for this view
    permission_classes = [AllowAny] 
    def post(self, request, format=None):
        caregiver_email=request.data.get('caregiver_email')
        caregiver=Caregiver.objects.get(email=caregiver_email)
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        if not email or not password or not first_name or not last_name:
            return Response({'error': 'Please provide all required fields'}, status=status.HTTP_400_BAD_REQUEST)
        patient = Patient.objects.create(email=email, first_name=first_name, last_name=last_name,password=password,caregiver=caregiver)
        patient.save()
        return Response({'message': 'Patient created successfully'}, status=status.HTTP_201_CREATED)
    







class CaregiverPatientSignupView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsCaregiverAuthenticated]
    def post(self, request, format=None):
        token = request.auth
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        caregiver_id = payload['user_id']
        caregiver=Caregiver.objects.get(id=caregiver_id)
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        if Patient.objects.filter(caregiver=caregiver).exists():
            return Response({'error': 'You can only create one account per patient'}, status=status.HTTP_403_FORBIDDEN)
        if not email or not password or not first_name or not last_name:
            return Response({'error': 'Please provide all required fields'}, status=status.HTTP_400_BAD_REQUEST)
        patient = Patient.objects.create(email=email, first_name=first_name, last_name=last_name,password=password,caregiver=caregiver)
        patient.save()
        return Response({'message': 'Patient created successfully'}, status=status.HTTP_201_CREATED)
    




class patientAddSpeaker(APIView):
    authentication_classes = [PJWTAuthentication]
    permission_classes = [IsPatientAuthenticated]
    def post(self, request):
        response_data=[]
        try:
            image_file = request.FILES.get('picture') #Add Speaker image
            speaker_name = request.POST.get('recognized_name') #Add speaker name
            token = request.auth
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            patient_id = payload['user_id']
            patient = Patient.objects.get(id=patient_id) #Get Caregiver id
            caregiver_id=patient.caregiver
            speaker_instance = Speaker(recognized_name=speaker_name, caregiver=caregiver_id, img_path=image_file,is_recognized=True)
            speaker_instance.save()
            # return Response({'message': 'New Speaker Added'}, status=status.HTTP_201_CREATED)
            response_data.append({
                'status': 'success',
                'id':speaker_instance.pk,
                })
            return JsonResponse(list(response_data), safe=False)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)




# class MyCargiver(APIView):
#    def get(self, request):
#       query_set=Caregiver.objects.all()
#       cargiver_serializer=CaregiverSerializer(query_set,many=True)
#       return Response(cargiver_serializer.data)           
#    def post(self, request):
#         first_name = request.data['first_name']
#         last_name = request.data['last_name']
#         email = request.data['email']
#         password = request.data['password']
#         user = Caregiver(first_name=first_name, last_name=last_name, email=email, password=password)
#         user.save()
#         return Response({'status': 'success'})

 

# class SpeakerImageView_id(APIView):
#    def get(self, request,id):
#       query_set=Speaker.objects.get(pk=id)
#       speaker_serializer=PatientSerializer(query_set)
#       return Response(speaker_serializer.data)



# def delete_speaker(request, speaker_id):
#     speaker = Speaker.objects.filter(id=speaker_id)
#     speaker.delete()
#     return JsonResponse({'message': f'Speaker with id {speaker_id} has been deleted'})



# def GalleryaddedbyCaregiver(request,id):
    
#     if request.method == 'GET':
        
#       speakers = Speaker.objects.filter(caregiver=id)
#       response_data = []
#       path='media/'
#       for speaker in speakers:
#         image_path = speaker.img_path
#         r=f'{path}{image_path}'
#         image_data = open(r, 'rb').read()
#         response_data.append({
#             'image': base64.b64encode(image_data).decode(),
#             'speaker_name': speaker.recognized_name,
#             'speaker_relationship': speaker.relationship,
#         })
#       return JsonResponse(list(response_data), safe=False)
#return HttpResponse({'status': 'success'})

# class CaregiverTokenObtainPairView(TokenObtainPairView):
#     #permission_classes = [AllowAny]
#     serializer_class = CaregiverTokenObtainPairSerializer



# def extract_token(request):
#      auth_header = request.headers.get('Authorization')
     
#      #if not auth_header:
#       #  return JsonResponse('None')
#      if auth_header.startswith('Bearer '):
#          token=auth_header[7:]
#          decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        
#         # Extract the user ID from the decoded token
#      user_id = decoded_token['user_id']
#      return JsonResponse({'user_id': user_id})

# class LoginView(APIView):
#     authentication_classes = []
#     permission_classes = []

#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         caregiver = Caregiver.objects.filter(email=email).first()
#         if not caregiver:
#             return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

#         #if not caregiver.check_password(password):
#          #   return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

#         token, created = Token.objects.get_or_create(user=caregiver)

#         return Response({'token': token.key})



# class HelloView(APIView):
    
#     authentication_classes = [PJWTAuthentication]
#     permission_classes = [IsPatientAuthenticated]

#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response({'Success': content})
# def hello(request):
#     if request.method =='GET':
#         print('hello')

# class HelloView(APIView):
#     permission_classes = (IsAuthenticated,)
#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response(content)