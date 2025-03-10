from django.urls import path
from . import views

app_name = 'materials'

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('project/', views.general, name='project'),  # Add this line
    path('general/', views.general, name='general'),  # Add this line
    path('element/<str:name>', views.get_element_info, name='get_element_info'),
    path('firebase-login/', views.firebase_login, name='firebase_login'),
]