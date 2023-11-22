from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import User
from firebase_admin import credentials, initialize_app, storage
from datetime import timedelta
import io

# Initialize Firebase
cred = credentials.Certificate(r"C:\Users\mrliv\Documents\Skolas Lietas\Prakse (4. kurss)\opencvimages-68d985d98e03.json")
initialize_app(cred, {'storageBucket': 'opencvimages.appspot.com'})

bucket = storage.bucket()

# Create your views here.

@ensure_csrf_cookie
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('users_view'))
        else:
            return render(request, 'myapp/login.html', {'error': 'Invalid login'})
    else:
        return render(request, 'myapp/login.html')

def users_view(request):
    users = User.objects.all()
    for user in users:
        blobs = bucket.list_blobs(prefix=f'{user.identifier}/')
        user.images = []
        for blob in blobs:
            if blob.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                url = blob.generate_signed_url(timedelta(minutes=15), method='GET')
                user.images.append(url)
    return render(request, 'myapp/users.html', {'users': users})

def edit_user_view(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user.name = request.POST['name']
        user.surname = request.POST['surname']
        user.save()
        if 'image' in request.FILES:
            images = request.FILES.getlist('image')
            for image in images:
                blob = bucket.blob(f'{user.identifier}/{image.name}')
                blob.upload_from_file(image, content_type=image.content_type)
        if 'delete_images' in request.POST:
            for image_name in request.POST.getlist('delete_images'):
                blob = bucket.blob(f'{user.identifier}/{image_name}')
                blob.delete()
        return redirect('edit_user', user_id=user.id)
    else:
        blobs = bucket.list_blobs(prefix=f'{user.identifier}/')
        user.images = [{'url': blob.generate_signed_url(timedelta(minutes=15), method='GET'), 'name': blob.name.split('/')[-1], 'size': blob.size / 1024 / 1024} for blob in blobs if blob.name != f'{user.identifier}/']
        return render(request, 'myapp/edit_user.html', {'user': user})

def delete_user_view(request, user_id):
    user = User.objects.get(id=user_id)
    blobs = bucket.list_blobs(prefix=f'{user.identifier}/')
    for blob in blobs:
        blob.delete()
    user.delete()
    return redirect('users_view')

def delete_image_view(request, user_id, image_name):
    user = User.objects.get(id=user_id)
    blob = bucket.blob(f'{user.identifier}/{image_name}')
    blob.delete()
    return redirect('edit_user', user_id=user.id)

def add_user_view(request):
    if request.method == 'POST':
        identifier = request.POST['identifier']
        name = request.POST['name']
        surname = request.POST['surname']
        pictures = request.FILES.getlist('image')

        # Check if a user with the same identifier already exists
        if User.objects.filter(identifier=identifier).exists():
            return render(request, 'myapp/add_user.html', {'error': 'A user with this identifier already exists.'})

        # Create a new user
        user = User.objects.create(identifier=identifier, name=name, surname=surname)

        # Upload the pictures to Firebase Storage
        for picture in pictures:
            blob = bucket.blob(f'{identifier}/{picture.name}')
            blob.upload_from_file(picture, content_type=picture.content_type)

        return redirect('users_view')
    else:
        return render(request, 'myapp/add_user.html')

def about_view(request):
    return render(request, 'myapp/about.html')