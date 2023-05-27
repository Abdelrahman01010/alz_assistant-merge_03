from rest_framework import serializers
from main.models import Speaker, Caregiver,Patient
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class CaregiverTokenObtainPairSerializer(TokenObtainPairSerializer):
   # email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('username')
        password = attrs.get('password')

        if email and password:
            caregiver = Caregiver.objects.filter(email=email).first()
        if caregiver is not None:
            user, created = User.objects.get_or_create(
            username=caregiver.email,
            email=caregiver.email
            )
            if user :
                payload = {
                    'id': caregiver.id,
                    'email': caregiver.email,
                }
                return super().validate(attrs)

            raise serializers.ValidationError('Invalid email or password')

        raise serializers.ValidationError('Email and password are required')


   



class CaregiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caregiver
        fields = ['id', 'first_name','last_name','email','password']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caregiver
        fields = ['id', 'first_name','last_name','email','password']


class Caregiver_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Caregiver
        fields = ['id']

class SpeakerSerializer(serializers.ModelSerializer):
  class Meta:
      model=Speaker
      fields=['id','img_path','caregiver','is_recognized','entry_date','audio_path','recognized_name']
   
  


    

