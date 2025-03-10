from django.contrib.auth import authenticate, login
from django.utils.deprecation import MiddlewareMixin

class FirebaseAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        firebase_token = request.headers.get('Authorization')
        if firebase_token:
            user = authenticate(request, firebase_token=firebase_token)
            if user:
                login(request, user)
        return None