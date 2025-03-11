from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.core.serializers import serialize
from .models import Element
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from plotly.offline import plot
import pandas as pd
from firebase_admin import auth
from .utils import verify_firebase_token
from .models import get_or_create_user
from django.contrib.auth.decorators import login_required

json_file_path = os.path.join(os.path.dirname(__file__), 'static/data/team.json')
with open(json_file_path, 'r') as file:
    team_data = json.load(file)
    research = json.load(open(os.path.join(os.path.dirname(__file__), 'static/data/research.json')))

elements = Element.objects.all()


@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def index(request):
    # Load team data from JSON file
    return render(request, 'home.html', {'team': team_data})
@login_required
def about(request):
    return render(request, 'about.html')
@login_required
def contact(request):
    return render(request, 'contact.html')
@login_required
def project(request):
    return render(request, 'lattice.html')
@login_required
def general(request):
    return render(request, 'general.html', {
        'elements': elements,
    })
@login_required
def get_element_info(request, name):
   try:
        element = Element.objects.get(name=name.capitalize())

        print(element.group_block)
        return render(request, 'element.html', {
            'element': element, "research": research["elements"][name.capitalize()],
            })
   except KeyError:
       return render(request, 'lazy.html')


@csrf_exempt
def firebase_login(request):
    if request.method == 'POST':
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'status': 'error', 'message': 'Authorization header missing or invalid'}, status=401)

        id_token = auth_header.split('Bearer ')[1]

        try:
            decoded_token = auth.verify_id_token(id_token)
            print(decoded_token)
            email = decoded_token.get('email')
            uid = decoded_token['uid']
            allowed_domain = "iith.ac.in"  # Replace with your desired domain
            if not email.endswith(f"@{allowed_domain}"):
                return JsonResponse({'status': 'error', 'message': 'Unauthorized email domain'}, status=403)
            
            

            # Create or retrieve a Django user based on UID or email
            from django.contrib.auth.models import User
            user, created = User.objects.get_or_create(username=uid, defaults={'email': email})

            # Optionally log in the user (if using Django's session-based authentication)
            from django.contrib.auth import login
            login(request, user)
            return JsonResponse({'status': 'success', 'user_id': user.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=401)

    else:
        return render(request, 'account/login.html')