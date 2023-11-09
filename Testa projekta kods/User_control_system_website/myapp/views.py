from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import User
from django.shortcuts import redirect
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
            return HttpResponseRedirect(reverse('users_view'))  # Redirect to users_view
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
            image = request.FILES['image']
            s3_resource.Object('opencvimages', f'{user.identifier}/{image.name}').put(Body=image.read())
        if 'delete_images' in request.POST:
            for image_name in request.POST.getlist('delete_images'):
                s3_resource.Object('opencvimages', f'{user.identifier}/{image_name}').delete()
        return redirect('edit_user', user_id=user.id)
    else:
        response = s3_client.list_objects(Bucket='opencvimages', Prefix=f'{user.identifier}/')
        user.images = [{'url': 'https://s3.eu-north-1.amazonaws.com/opencvimages/' + obj['Key'], 'name': obj['Key'].split('/')[-1]} for obj in response.get('Contents', []) if obj['Key'] != f'{user.identifier}/']
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

def about_view(request):
    return render(request, 'myapp/about.html')