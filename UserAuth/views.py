from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm


# Create your views here.

def user_register(request):


    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confPassword']

        form_data = {
            'username': username, 
            'email': email, 
           
        }

        if username == '' or email == '' or password == '' or confirm_password == '':
            messages.error(request, 'All fields are required.')
            return render(request, 'UserAuth/signup.html', context=form_data)
        
        if password!= confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'UserAuth/signup.html', context=form_data)
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'UserAuth/signup.html', context=form_data)
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'UserAuth/signup.html', context=form_data)
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'UserAuth/signup.html', context=form_data)

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        messages.success(request, 'Your account has been created successfully.')
    

        return redirect('user_login')


    return render(request, 'UserAuth/signup.html')

def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username == '' or password == '':
            messages.error(request, 'All fields are required.')
            return render(request, 'UserAuth/login.html')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')

            if 'next' in request.GET:
                return redirect(request.GET['next'])
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'UserAuth/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')

    return redirect('user_login')

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  
    else:
        form = ProfileForm(instance=profile) 

    return render(request, 'UserAuth/profile.html', {'profile': profile, 'form': form})