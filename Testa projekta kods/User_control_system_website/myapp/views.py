from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

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
    return render(request, 'myapp/users.html')