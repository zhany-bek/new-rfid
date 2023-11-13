from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from decouple import config
import pyrebase

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


def firebase_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            user = authe.current_user
            if user is not None:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "User authentication failed.")
                return redirect('login')  # Redirect to login page if not authenticated
        except Exception as e:
            print(f"Error checking authentication: {e}")
            messages.error(request, "An error occurred during authentication.")
            return redirect('login')  # Redirect to login page in case of an error
    return _wrapped_view