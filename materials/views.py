from django.http import JsonResponse
from django.shortcuts import render
import json
import os
from django.core.serializers import serialize
from .models import Element
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from plotly.offline import plot
import pandas as pd


json_file_path = os.path.join(os.path.dirname(__file__), 'static/data/team.json')
with open(json_file_path, 'r') as file:
    team_data = json.load(file)

elements = Element.objects.all()



def home(request):
    return render(request, 'home.html')

def index(request):
    # Load team data from JSON file
    return render(request, 'home.html', {'team': team_data})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def project(request):
    return render(request, 'lattice.html')

def general(request):
    return render(request, 'general.html', {
        'elements': elements,
    })

def get_element_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        atomic_number = data.get('atomic_number')
        
        try:
            element = Element.objects.get(atomic_number=atomic_number)
            # Serialize the element object to JSON
            element_data = json.loads(serialize('json', [element]))[0]['fields']
            element_data['atomic_number'] = atomic_number  # Add atomic_number back in
            return JsonResponse(element_data)
        except Element.DoesNotExist:
            return JsonResponse({'error': 'Element not found'}, status=404)