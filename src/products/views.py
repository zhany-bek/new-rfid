from django.shortcuts import render, redirect
from decouple import config
import pyrebase

# Create your views here.
fb_config = {
    'apiKey': config('API_KEY'),
    'authDomain': config('AUTH_DOMAIN'),
    'databaseURL': config('DATABASE_URL'),
    'projectId': config('PROJECT_ID'),
    'storageBucket': config('STORAGE_BUCKET'),
    'messagingSenderId': config('MESSAGING_SENDER_ID'),
    'appId': config('APP_ID'),
}

firebase = pyrebase.initialize_app(fb_config)
authe = firebase.auth()
database = firebase.database()

def index(request):
    return render(request, 'products/home.html')

def reg_product(request):
    pass