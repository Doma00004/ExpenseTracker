from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . forms import *
import random
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model


# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm

def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account Created Successfully!") # Auto login after registration
            return redirect("/register")  # Redirect to homepage after login
        else:
            messages.error(request, "Please provide correct details")

    else:
        form = CustomUserCreationForm()

    return render(request, "users/register.html", {"form": form})



# def register_user(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.add_message(request, messages.SUCCESS, 'Account Created')
#             return redirect('/register')
#         else:
#             messages.add_message(request, messages.ERROR, 'Please provide correct details')
#             return render(request, 'users/register.html',{
#                 'form':form
#             })
        
#     context = {
#         'form':UserCreationForm
#     }
#     return render(request, 'users/register.html', context)



def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])

            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('/')
                else:
                    return redirect('/')
            else:
                messages.add_message(request, messages.ERROR, 'Please provide correct credential')
                return render(request, 'users/login.html', {
                    'form':form
                })
            
    form = LoginForm
    context = {
            'form': form
    }
    return render(request, 'users/login.html', context)



def logout_user(request):
    logout(request)
    return redirect('/')



def homepage(request):
    return render(request, 'users/homepage.html')



otp_storage = {}  # Temporary storage for OTPs (use database in production)

def forgot_password(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
            otp_storage[email] = otp  # Store OTP (reset after successful login)

            # Send OTP via email
            send_mail(
                'Your Password Reset OTP',
                f'Your OTP for password reset is: {otp}',
                'lhakpadomas08@gmail.com',  # Change this to your sender email
                [email],
                fail_silently=False,
            )

            messages.success(request, "OTP sent to your email!")
            return redirect('verify_otp', email=email)
    else:
        form = ForgotPasswordForm()

    return render(request, "users/forgot_password.html", {"form": form})



def verify_otp(request, email):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        if otp_storage.get(email) == int(entered_otp):  # Check if OTP matches
            return redirect(reverse('reset_password', kwargs={'email': email}))  # Redirect to reset password
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "users/verify_otp.html", {"email": email})



User = get_user_model()

def reset_password(request, email):
    user = User.objects.get(email=email)
    if request.method == "POST":
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
        else:
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successfully!")
            return redirect('login')  # Redirect to login page

    return render(request, "users/reset_password.html", {"email": email})
