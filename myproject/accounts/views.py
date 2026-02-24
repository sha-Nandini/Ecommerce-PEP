from orders.models import Address, Order
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile


@login_required
def add_address(request):
    if request.method == 'POST':
        Address.objects.create(
            user=request.user,
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            postal_code=request.POST['postal_code'],
            country=request.POST['country'],
            phone=request.POST['phone'],
        )
        messages.success(request, 'Address added!')
        return redirect('profile')
    return render(request, 'add_address.html')


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            user.backend = 'django.contrib.auth.backends.ModelBackend'

            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')


# @login_required
# def profile(request):
#     profile = Profile.objects.get(user=request.user)
#     return render(request, 'profile.html', {'profile': profile})
@login_required
def profile(request):
    profile = request.user.profile
    addresses = Address.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'profile.html', {
        'profile': profile,
        'addresses': addresses,
        'orders': orders
    })


@login_required
def update_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'update_profile.html', {'profile': profile})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully!")
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})
