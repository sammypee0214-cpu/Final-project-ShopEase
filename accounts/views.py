
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not all([username, email, password, confirm_password]):
            return render(request, 'products/register.html', {
                'error': 'Please complete all fields.'
            })

        if password != confirm_password:
            return render(request, 'products/register.html', {
                'error': 'Passwords do not match.'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'products/register.html', {
                'error': 'This username is already taken.'
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'products/register.html', {
                'error': 'This email is already registered.'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return render(request, 'products/register.html', {
            'success': True,
            'username': user.username
        })

    return render(request, 'products/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'products/login.html', {
            'error': 'Invalid username or password.'
        })

    return render(request, 'products/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')