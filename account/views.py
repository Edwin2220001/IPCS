from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username= username).exists():
            return render(request, 'register.html', {'error': 'Username is already taken'})

        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)

        login(request, user)
        return redirect('/')
    return render(request, 'register.html')
    return redirect('account:logout')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        emailid = request.POST['emailid']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password, emailid=emailid)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('/')
    return render(request, 'logout.html')