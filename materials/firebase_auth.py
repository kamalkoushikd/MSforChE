from firebase_admin import auth
from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend

class FirebaseBackend(BaseBackend):
    def authenticate(self, request, firebase_token=None):
        if firebase_token:
            try:
                decoded_token = auth.verify_id_token(firebase_token)
                uid = decoded_token['uid']
                email = decoded_token.get('email', '')
                user, created = User.objects.get_or_create(username=uid, email=email)
                return user
            except:
                return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
