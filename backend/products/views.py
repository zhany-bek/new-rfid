from django.shortcuts import render, redirect
from decouple import config
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
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
    context = {'current_page': 'home'}
    return render(request, 'products/home.html', context)

# Adding new products with RFID tags
def reg_product(request):
    context = {'current_page': 'reg-product'}
    available_tags = []
    prod_uids = []

    try:
        tags_d = database.child('Tags').get()
        for tags in tags_d.each():
            available_tags.append(tags.key())
    except:
        error_message = 'No tags available!'
        context['error'] = 'No tags available!'
        context['tags'] = available_tags
        return render(request, 'products/home.html', context)
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
            context['success'] = 'Saved successfully!'
            context['tags'] = available_tags
            return render(request, 'products/reg_product.html', context)
        except:
            context['error'] = 'Could not save :('
            context['tags'] = available_tags
            error_message = 'Could not save :('
            return render(request, 'products/reg_product.html', context)
    context['tags'] = available_tags
    return render(request, 'products/reg_product.html', context)


def product_list(request):
    context = {'current_page': 'product-list'}
    products_d = database.child('Products').get()
    locations_d = database.child('Tags').get()
    locs_d = {}
    prod_d = {}
    for prod in products_d.each():
        prod_d[prod.key()] = prod.val()
    for locs in locations_d.each():
        locs_d[locs.key()] = locs.val()

    combined_dict = {}
    for key, value in prod_d.items():
        combined_dict[key] = (value, locs_d[key])

    context = {
        'combined_d': combined_dict,
        'current_page': 'product-list'
    }

    return render(request, 'products/product_list.html', context)

def product_cat(request, product):

    if request.method == 'POST':
        key = request.POST.get('key')
        key_product = database.child('Products').child(key).get()
        key_tag = database.child('Tags').child(key).get()
        database.child('Archive').child('Products').update({key_product.key(): key_product.val()})
        database.child('Archive').child('Tags').update({key_tag.key(): key_tag.val()})
        database.child('Products').child(key).remove()
        database.child('Tags').child(key).remove()
        return redirect('product-list')

    product_frame = database.child('Products').child(product).get()
    tag_frame = database.child('Tags').child(product).get()
    prod_d = {product_frame.key(): product_frame.val()}
    locs_d = {tag_frame.key(): tag_frame.val()}
    
    return render(request, 'products/product-cat.html', {
        'prod_d': prod_d,
        'locs_d': locs_d
    })
    

def archive(request):
    context = {'current_page': 'archive'}
    products_d = database.child('Archive').child('Products').get()
    locations_d = database.child('Archive').child('Tags').get()
    locs_d = {}
    prod_d = {}
    for prod in products_d.each():
        prod_d[prod.key()] = prod.val()
    for locs in locations_d.each():
        locs_d[locs.key()] = locs.val()

    combined_dict = {}
    for key, value in prod_d.items():
        combined_dict[key] = (value, locs_d[key])

    context = {
        'combined_d': combined_dict,
        'current_page': 'archive'
    }

    return render(request, 'products/archive.html', context)