# Import necessary modules
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import User
from firebase_admin import credentials, initialize_app, storage
from datetime import timedelta
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import base64

# Initialize Firebase
cred = credentials.Certificate(r"C:\Users\mrliv\Documents\Skolas Lietas\Prakse (4. kurss)\opencvimages-68d985d98e03.json")
initialize_app(cred, {'storageBucket': 'opencvimages.appspot.com'})

# Get a reference to the storage service
bucket = storage.bucket()

# Ensure CSRF cookie is set
@ensure_csrf_cookie
def login_view(request):
    # Handle POST request
    if request.method == 'POST':
        # Authenticate user
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # If user is authenticated, log them in and redirect to users view
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('users_view'))
        # If authentication fails, return error
        else:
            return render(request, 'myapp/login.html', {'error': 'Invalid login'})
    # Handle GET request
    else:
        return render(request, 'myapp/login.html')

def users_view(request):
    # Get all users
    users = User.objects.all()
    # For each user, get their images from Firebase Storage
    for user in users:
        blobs = bucket.list_blobs(prefix=f'{user.identifier}/')
        user.images = []
        for blob in blobs:
            if blob.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                url = blob.generate_signed_url(timedelta(minutes=15), method='GET')
                user.images.append(url)
    # Render users view with users data
    return render(request, 'myapp/users.html', {'users': users})

def edit_user_view(request, user_id):
    # Get user by id
    user = User.objects.get(id=user_id)
    # Handle POST request
    if request.method == 'POST':
        # Update user details
        user.name = request.POST['name']
        user.surname = request.POST['surname']
        user.save()
        # If new images are uploaded, save them to Firebase Storage
        if 'image' in request.FILES:
            images = request.FILES.getlist('image')
            for image in images:
                blob = bucket.blob(f'{user.identifier}/{image.name}')
                blob.upload_from_file(image, content_type=image.content_type)
        # If images are selected for deletion, delete them from Firebase Storage
        if 'delete_images' in request.POST:
            for image_name in request.POST.getlist('delete_images'):
                blob = bucket.blob(f'{user.identifier}/{image_name}')
                blob.delete()
        # If captured images are uploaded, save them to Firebase Storage
        for key in request.FILES.keys():
            if key.startswith('captured_image'):
                image = request.FILES[key]
                imageIndex = key.replace('captured_image', '')
                unique_filename = f"{user.identifier}_captured_image{imageIndex}"
                # Save the image to the local file system
                local_image_path = default_storage.save(f'{unique_filename}.png', image)
                with open(local_image_path, 'rb') as image_file:
                    blob = bucket.blob(f'{user.identifier}/{unique_filename}.png')
                    blob.upload_from_file(image_file)
                # Delete the local image file
                os.remove(local_image_path)
        # Redirect to edit user view
        return redirect('edit_user', user_id=user.id)
    # Handle GET request
    else:
        # Get user's images from Firebase Storage
        blobs = bucket.list_blobs(prefix=f'{user.identifier}/')
        user.images = [{'url': blob.generate_signed_url(timedelta(minutes=15), method='GET'), 'name': blob.name.split('/')[-1], 'size': blob.size / 1024 / 1024} for blob in blobs if blob.name != f'{user.identifier}/']
        # Render edit user view with user data
        return render(request, 'myapp/edit_user.html', {'user': user})

def delete_user_view(request, user_id):
    # Get user by id
    user = User.objects.get(id=user_id)
    # Delete user's images from Firebase Storage
    blobs = bucket.list_blobs(prefix=f'{user.identifier}/')
    for blob in blobs:
        blob.delete()
    # Delete user from database
    user.delete()
    # Redirect to users view
    return redirect('users_view')

def delete_image_view(request, user_id, image_name):
    # Get user by id
    user = User.objects.get(id=user_id)
    # Delete specified image from Firebase Storage
    blob = bucket.blob(f'{user.identifier}/{image_name}')
    blob.delete()
    # Redirect to edit user view
    return redirect('edit_user', user_id=user.id)

def add_user_view(request):
    # Handle POST request
    if request.method == 'POST':
        # Get user details from request
        identifier = request.POST['identifier']
        name = request.POST['name']
        surname = request.POST['surname']
        # Check if a user with the same identifier already exists
        if User.objects.filter(identifier=identifier).exists():
            return redirect('add_user')
        # Create a new user
        user = User.objects.create(identifier=identifier, name=name, surname=surname)
        # If new images are uploaded, save them to Firebase Storage
        if 'image' in request.FILES:
            images = request.FILES.getlist('image')
            for image in images:
                blob = bucket.blob(f'{identifier}/{image.name}')
                blob.upload_from_file(image, content_type=image.content_type)
        # If captured images are uploaded, save them to Firebase Storage
        for key in request.POST.keys():
            if key.startswith('captured_image'):
                dataUrl = request.POST[key]
                # Convert the data URL to a bytes object
                header, data = dataUrl.split(',', 1)
                data = base64.b64decode(data)
                # Create a ContentFile object from the bytes object
                image = ContentFile(data, name=f'{identifier}/{key}.png')
                # Upload the image to Firebase Storage
                blob = bucket.blob(f'{identifier}/{key}.png')
                blob.upload_from_file(image, content_type='image/png')
        # Redirect to users view
        return redirect('users_view')
    # Handle GET request
    else:
        return render(request, 'myapp/add_user.html')

def about_view(request):
    # Render about view
    return render(request, 'myapp/about.html')