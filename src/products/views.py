from django.shortcuts import render, redirect
from decouple import config
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .decorators import firebase_login_required
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

# Homepage
def index(request):
    return render(request, 'products/home.html')

# Login
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = authe.sign_in_with_email_and_password(email, password)
            # Store user information in session or handle as needed
            request.session['uid'] = user['localId']

            # Redirect to the dashboard or another page
            return render(request, 'products/dash.html')

        except pyrebase.pyrebase.HTTPError as e:
            error_message = e.args[1].get('error', {}).get('message', 'An error occurred.')
            messages.error(request, error_message)

    return render(request, 'products/login.html')

@firebase_login_required
def user_logout(request):
    logout(request)
    return redirect('home')

# Dashboard
@firebase_login_required
def dash(request):
    return redirect('dashboard')


# Adding new products with RFID tags
def reg_product(request):
    available_tags = []
    prod_uids = []

    try:
        tags_d = database.child('Tags').get()
        for tags in tags_d.each():
            available_tags.append(tags.key())
    except:
        error_message = 'No tags available!'
        return render(request, 'products/home.html', {'error': error_message, 'tags': available_tags})
    try:
        products_d = database.child('Products').get()
        for products in products_d.each():
            prod_uids.append(products.key())
        available_tags = [tag for tag in available_tags if tag not in prod_uids]
    except:
        pass

    if request.method == 'POST':
        try:
            uid = request.POST.get('uid')
            block_type = request.POST.get('block_type')
            price_per_kg = request.POST.get('price_per_kg')
            
            # Create and save the new product:
            data = {uid: {'block_type': block_type, 'price_per_kg': price_per_kg}}
            database.child('Products').update(data)
            available_tags.remove(uid)
            # If successful, redirect to a success page
            return render(request, 'products/reg_product.html', {
                'success': "Saved successfully!",
                'tags': available_tags
            })
        except:
            error_message = 'Could not save :('
            return render(request, 'products/reg_product.html', {'error': error_message, 'tags': available_tags})
    return render(request, 'products/reg_product.html', {'tags': available_tags})


def product_list(request):
    return render(request, 'products/product_list.html')