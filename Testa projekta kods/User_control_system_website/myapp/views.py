from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import User
import boto3

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
    s3 = boto3.client('s3')
    users = User.objects.all()
    for user in users:
        response = s3.list_objects(Bucket='opencvimages', Prefix=f'{user.identifier}/')
        user.images = ['https://s3.eu-north-1.amazonaws.com/opencvimages/' + obj['Key'] for obj in response.get('Contents', []) if obj['Key'].lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return render(request, 'myapp/users.html', {'users': users})

def edit_user_view(request, user_id):
    s3_resource = boto3.resource('s3')
    s3_client = boto3.client('s3')
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user.name = request.POST['name']
        user.surname = request.POST['surname']
        user.save()
        if 'image' in request.FILES:
            images = request.FILES.getlist('image')
            for image in images:
                s3_resource.Object('opencvimages', f'{user.identifier}/{image.name}').put(Body=image.read())
        if 'delete_images' in request.POST:
            for image_name in request.POST.getlist('delete_images'):
                s3_resource.Object('opencvimages', f'{user.identifier}/{image_name}').delete()
        return redirect('edit_user', user_id=user.id)
    else:
        response = s3_client.list_objects(Bucket='opencvimages', Prefix=f'{user.identifier}/')
        user.images = [{'url': 'https://s3.eu-north-1.amazonaws.com/opencvimages/' + obj['Key'], 'name': obj['Key'].split('/')[-1], 'size': s3_resource.Object('opencvimages', obj['Key']).get()['ContentLength'] / 1024 / 1024} for obj in response.get('Contents', []) if obj['Key'] != f'{user.identifier}/']
        return render(request, 'myapp/edit_user.html', {'user': user})
    
def delete_user_view(request, user_id):
    s3 = boto3.resource('s3')
    user = User.objects.get(id=user_id)
    for obj in s3.Bucket('opencvimages').objects.filter(Prefix=f'{user.identifier}/'):
        obj.delete()
    user.delete()
    return redirect('users_view')

def delete_image_view(request, user_id, image_name):
    s3 = boto3.resource('s3')
    user = User.objects.get(id=user_id)
    s3.Object('opencvimages', f'{user.identifier}/{image_name}').delete()
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

        # Upload the pictures to S3
        s3 = boto3.client('s3', region_name='eu-north-1')
        for picture in pictures:
            s3.upload_fileobj(picture, 'opencvimages', f'{identifier}/{picture.name}')

        return redirect('users_view')
    else:
        return render(request, 'myapp/add_user.html')

def about_view(request):
    return render(request, 'myapp/about.html')