from django.shortcuts import render
import json
import os

def home(request):
    return render(request, 'home.html')

def index(request):
    # Load team data from JSON file
    json_file_path = os.path.join(os.path.dirname(__file__), 'static/data/team.json')
    with open(json_file_path, 'r') as file:
        team_data = json.load(file)
    
    return render(request, 'home.html', {'team': team_data})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def project(request):
    return render(request, 'lattice.html')