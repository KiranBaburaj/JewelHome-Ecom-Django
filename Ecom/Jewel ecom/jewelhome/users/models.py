from django.db import models
from django.core.mail import send_mail
import random


# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    is_phone_verified = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=False)
    # Add other custom fields (if needed)

    def generate_otp(self):
        # Implement OTP generation logic (e.g., random 6-digit number)
        otp = str(random.randint(100000, 999999))
        return otp

  # CustomUser model
    def send_otp(self,otp, method='email'):
        otp = self.generate_otp()  # Generate OTP before sending
        if method == 'email':
            subject = 'Your OTP for Signup or Login'
            message = f'Your OTP is {otp}'
            send_mail(subject, message, 'your_email_address', [self.email])
    # Add logic for other OTP methods (e.g., SMS using Twilio)
from django.db import models

# Create your models here.
