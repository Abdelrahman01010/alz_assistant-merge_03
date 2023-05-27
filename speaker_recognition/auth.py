import jwt
from django.conf import settings

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from main.models import Caregiver,Patient



class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the JWT token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        # Parse the JWT token and get the user ID
        try:
            _, token = auth_header.split(' ')
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            caregiver_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed('Invalid token')

        # Authenticate the user and return the user and token
        try:
            if(payload['user_type']=='caregiver'):
                caregiver = Caregiver.objects.get(pk=caregiver_id)
                return (caregiver, token)
        except Caregiver.DoesNotExist:
            raise AuthenticationFailed('User not found')


class PJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the JWT token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        # Parse the JWT token and get the user ID
        try:
            _, token = auth_header.split(' ')
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            patient_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed('Invalid token')

        # Authenticate the user and return the user and token
        try:
            if(payload['user_type']=='patient'):
                patient = Patient.objects.get(id=patient_id)
                return (patient, token)
        except Patient.DoesNotExist:
            raise AuthenticationFailed('User not found')
