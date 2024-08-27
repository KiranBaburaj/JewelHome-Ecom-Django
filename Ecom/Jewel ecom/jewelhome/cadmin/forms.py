
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django import forms
from product.models import Products, Category

class RegisterUser(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","email","password1","password2",]
from django import forms



class EditForm(UserChangeForm):
    password=None
    class Meta:
        model =User
        fields =["username","email","is_superuser"]
        widgets ={
            "username":forms.TextInput(attrs={'class':'form-control'}),
            "email":forms.EmailInput(attrs={'class':'form-control'})
        }

from django.forms import inlineformset_factory
from django import forms
from product.models import Products

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'  # Adjust as needed based on desired fields
        exclude = ['image']  # Exclude image field (handled in ImageForm)

    def clean(self):
        cleaned_data = super().clean()
        # Add custom validation if needed
        return cleaned_data
from django import forms
from product.models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'  # Adjust as needed based on desired fields

    def clean(self):
        cleaned_data = super().clean()
        # Add custom validation for image size, format, etc.
        return cleaned_data

from django import forms
from product.models import Category  # Assuming your Category model is in the same app

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'  # Adjust as needed to include desired fields

    def clean_name(self):
        name = self.cleaned_data.get('name')
        # Add custom validation for name uniqueness, formatting, etc.
        return name


from django import forms
from product.models import Category

class EditCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'  # Adjust as needed to include desired fields

    def clean(self):
        cleaned_data = super().clean()
        # Add custom validation if needed
        return cleaned_data
from django import forms
from product.models import Products
from django import forms
# forms.py

from django import forms

class ProductForm(forms.ModelForm):
    Category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)

    class Meta:
        model = Products
        fields = ['name', 'description', 'price', 'discount','Category', 'weight', 'size',  'making_charge',]

ImageFormSet = inlineformset_factory(Products, Image, fields=('images',), extra=3)

from django import forms
from product.models import DailyRate

class DailyRateForm(forms.ModelForm):
    class Meta:
        model = DailyRate
        fields = ['rate']
