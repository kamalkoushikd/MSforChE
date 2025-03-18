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
from .utils import get_graph
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
    return render(request, 'home.html', {'team': team_data, 'user': request.user})
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
        # Get the element object from the database
        element = get_object_or_404(Element, name=name.capitalize())
        x, y = get_graph(name.lower())
        graph_data = [{'x': x[i], 'y': y[i]} for i in range(len(x))]

        # Load the JSON file
        json_path = os.path.join(os.path.dirname(__file__), 'static/data/data.json')
        model_path = os.path.join(os.path.dirname(__file__), f'static/models/{name.lower()}.json')
        with open(json_path, 'r') as file:
            data = json.load(file)
        
        # Convert element name to lowercase for consistent matching
        element_name = element.name.capitalize()

        # Find the matching element data in the JSON file
        element_data = next(
            (item for item in data.get('elements', []) if item.get('element') == element_name),
            None
        )

        if element_data is None:
            return render(request, 'lazy.html')

        # Pass only the matched element's data to the template
        return render(request, 'element.html', {
            'element': element,
            "research": research["elements"][name.capitalize()],
            'industry': element_data,
            'data': graph_data,
            'model': model_path,
        })
    except Exception as e:
        print(f"Error: {e}")
        return render(request, 'lazy.html')

