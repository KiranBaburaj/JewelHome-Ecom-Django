from django import forms
from .models import Coupon

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = '__all__'




from django import forms
from .models import ProductOffers, CategoryOffers

class ProductOfferForm(forms.ModelForm):
    class Meta:
        model = ProductOffers
        fields = '__all__'  # You can customize the fields as needed

class CategoryOfferForm(forms.ModelForm):
    class Meta:
        model = CategoryOffers
        fields = '__all__'  # You can customize the fields as needed
