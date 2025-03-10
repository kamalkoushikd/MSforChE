from firebase_admin import auth
from django.http import JsonResponse

def verify_firebase_token(request):
    token = request.headers.get('Authorization')
    if not token:
        return JsonResponse({'error': 'No token provided'}, status=401)

    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token  # Contains user info like uid, email, etc.
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=401)