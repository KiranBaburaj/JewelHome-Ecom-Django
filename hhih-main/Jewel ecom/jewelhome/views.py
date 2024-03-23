import os
import random
import string
from datetime import datetime, timedelta
from aiohttp import request
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from .forms import SignupForm, OTPForm
from .models import User as CustomUser
from product.models import Banner, Products,Category
from django.utils.translation import gettext as _
from twilio.rest import Client


def home(request):
    user = request.user
    products = Products.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    banner = Banner.objects.get(id=1)
    context = {'products': products, 'banner': banner, 'categories': categories}

    # Check if the user is authenticated and modify the context accordingly
    if user.is_authenticated:
        context['authenticated_user'] = user

    return render(request, 'user/home.html', context)

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data.get('password'))
            if user is not None  :
                
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'user/signin.html', {'form': form})

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_otp_twilio(user):
    account_sid = 'ACe8cae81e087c6c60d31751fd56d7fd99'
    auth_token = 'eb8a7fd3b2c48e57610370218ab62b84'
    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body=f"Your OTP is {user.otp}",
            from_='+19402455707',
            to=user.phone_number
        )
        print(f"Message SID: {message.sid}")
    except TwilioRestException as e:
        print(f"Twilio error: {e}")

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.otp = generate_otp()
            user.otp_generated_at = datetime.now() + timedelta(minutes=10)
            user.save()
            send_otp_twilio(user)
            return redirect('verify_otp')
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = SignupForm()
    return render(request, 'user/signup.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            phone_number = form.cleaned_data.get('phone_number')

            try:
                user = CustomUser.objects.get(phone_number=phone_number)
            except CustomUser.DoesNotExist:
                messages.error(request, _('Invalid OTP or OTP has expired'))
                return redirect('verify_otp')

            if user.otp == otp:
                user.is_verified = True
                user.save()
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, _('Invalid OTP or OTP has expired'))
    else:
        form = OTPForm()
    return render(request, 'user/verify_otp.html', {'form': form})

from django.shortcuts import render, get_object_or_404


def category_product_list(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Products.objects.filter(Category=category, is_active=True)
    
    context = {
        'category': category,
        'products': products,
    }
    
    return render(request, 'user/category_product_list.html', context)




def product_detail(request, product_id):
    product = get_object_or_404(Products, pk=product_id,is_active=True)
    related_products = Products.objects.filter(Category=product.Category, is_active=True).exclude(pk=product_id)
    random_related_products = random.sample(list(related_products), min(3, len(related_products)))

    context = {
        'product': product,
        'random_related_products': random_related_products
    }

    return render(request, 'user/product_detail.html', context)


from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    # Redirect to the home page or any other page after logout
    return redirect('home')