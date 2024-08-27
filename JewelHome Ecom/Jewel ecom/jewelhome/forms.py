from datetime import timedelta
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User  # Use your custom user model
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        # Phone number validation logic (e.g., check valid format, length)
        return phone_number
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import User
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import User

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    def clean(self):
        cleaned_data = super().clean()
        otp = cleaned_data.get('otp')
        phone_number = cleaned_data.get('phone_number')

        # Retrieve the user's stored OTP and generated time
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise ValidationError("Invalid phone number")

        stored_otp = user.otp
        otp_generated_at = user.otp_generated_at

        # Check if OTP matches and is not expired
        if otp != stored_otp:
            raise ValidationError("Invalid OTP")
        if otp_generated_at < timezone.now() - timedelta(minutes=10):  # Adjust expiration time as needed
            raise ValidationError("OTP has expired")

        return cleaned_data


class ResendOTPForm(forms.Form):
    phone_number = forms.CharField(max_length=15)

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data['phone_number']
        # Verify phone number exists and is associated with a user
        if not User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("Invalid phone number")

        # Resend OTP logic (send new OTP using Twilio or other method)

        return cleaned_data
