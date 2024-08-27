from django.contrib.auth import authenticate, login as adlogin
from django.contrib.auth import authenticate, logout as adlogout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .forms import RegisterUser,EditForm,DailyRateForm
from django.contrib import messages
from product.models import Products






@never_cache
def superuser_login(request):
    if request.user.is_authenticated:
        return redirect('custom_admin_homepage')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            adlogin(request, user)
            # Redirect to the custom admin panel homepage
            return redirect('custom_admin_homepage')
        else:
            # Display invalid login error
            error_message = 'Invalid username or password.'
            return render(request, 'admin/superuser_login.html', {'error_message': error_message})
    else:
        return render(request, 'admin/superuser_login.html')







@login_required(login_url='superuser_login')  # Apply login_required if needed
def create_user(request):
    if request.method == "POST":
        form = RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!")
            return redirect('user_list')
        else:
            messages.error(request, form.errors)
    else:
        form = RegisterUser()
    return render(request, "admin/create_user.html", {'form': form})



    """if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        User.objects.create_user(username, email, password)  # Assuming password hashing is handled
        return redirect('user_list')  # Redirect to user list
    else:
        return render(request, 'create_user.html')"""


@never_cache
@login_required(login_url='superuser_login')
def custom_admin_homepage(request):

    context = {} 
    return render(request, 'admin/custom_admin_homepage.html', context)

@never_cache
@login_required(login_url='superuser_login')
def user_list(request):
    users = User.objects.all()  
    context = {'users': users}
    return render(request, 'user_list.html', context)

    

@never_cache
@login_required(login_url='superuser_login')
def search_users(request):
    # Same logic as the user_list function, but with a different name
    query = request.GET.get('query')
    print(query)
    if query:
        users = User.objects.filter(username__icontains=query)
    else:
        users = User.objects.all()

    context = {'users': users}
    return render(request, 'admin/user_list.html', context)




@never_cache
@login_required(login_url='superuser_login')
def edit_user(request, user_id):
    request.session.pop('_messages', None)

    user = get_object_or_404(User, id=user_id)
    form=EditForm(instance=user)
    
    if request.method=="POST":
        form=EditForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,"")
            return redirect('user_list')
        else:
            messages.error(request,form.errors)
            form=EditForm(instance=user)

            return render(request,'edit_user.html',{'form':form})
    return render(request,'edit_user.html',{'form':form})

    """if request.method == 'POST':
        # Handle form data
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        

        user.save()
        return redirect('user_list')  # Redirect to user list upon success
    
    else:
        # Render the edit form for GET requests
        context = {'user': user}
        return render(request, 'edit_user.html', context)"""






@never_cache
@login_required(login_url='superuser_login')
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')  # Redirect to user list
    else:
        context = {'user': user}
        return render(request, 'delete_user.html', context)


@never_cache
@login_required(login_url='superuser_login')
def logout_view(request):
    adlogout(request)
    return redirect('superuser_login')  # Redirect to your login page after logout
from django.shortcuts import render


def products_list(request):
    products = Products.objects.all().order_by('-is_active','name')
    context = {    'products': products, }

    return render(request, 'admin/product/prod_list.html', context)

# views.py
from django.shortcuts import render, redirect
from .forms import ProductForm, ImageFormSet


def create_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())

        if product_form.is_valid() and formset.is_valid():
            product = product_form.save(commit=False)
            category_id = request.POST.get('Category')
            category = Category.objects.get(pk=category_id)
            product.Category = category
   
            product.save()

            for form in formset:
                if form.cleaned_data:
                    image = form.cleaned_data['images']
                    photo = Image(product=product, images=image)
                    photo.save()

            return redirect('products_list')
    else:
        product_form = ProductForm()
        formset = ImageFormSet(queryset=Image.objects.none())

    categories = Category.objects.all()

    return render(request, 'admin/product/create_product.html', {'product_form': product_form, 'formset': formset, 'categories': categories})


from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required  # Assuming login is required

# views.py
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ProductForm, ImageForm
from django.forms import inlineformset_factory

def product_edit(request,pk):
    product = get_object_or_404(Products, pk=pk)
    ImageFormSet = inlineformset_factory(Products, Image, form=ImageForm, extra=3, can_delete=True)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        formset = ImageFormSet(request.POST, request.FILES, instance=product)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()

            return redirect('products_list')
    else:
        form = ProductForm(instance=product)
        formset = ImageFormSet(instance=product)

    return render(
        request,
        'admin/product/product_edit.html',
        {'form': form, 'formset': formset, 'product': product}
    )

def product_detail(request, product_pk):
    product = get_object_or_404(Products, pk=product_pk)
    images = Image.objects.filter(product=product)  # Fetch related images

    context = {
        'product': product,
        'images': images,
        # Add other context variables as needed (e.g., related products, reviews)
    }

    return render(request, 'admin/product/product_detail.html', context)

from django.shortcuts import render




from django.shortcuts import render, redirect, get_object_or_404
from product.models import Category,Image
from .forms import CategoryForm  # Assuming you have a form for creation/editing

# ... (functions for different actions)

def viewcategory(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'admin/category/viewcategory.html', context)


def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('viewcategory')
        else:
            pass
            # Handle form errors
    else:
        form = CategoryForm()
    context = {'form': form}
    return render(request, 'admin/category/create_category.html', context)

# ... (similar functions for edit, delete, etc.)

from django.shortcuts import render, get_object_or_404


def category_detail(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    # Optionally fetch related products:
    products = Products.objects.filter(Category=category, is_active=True)
    context = {'category': category, 'products': products}
    return render(request, 'admin/category/category_detail.html', context)

from django.shortcuts import render, get_object_or_404, redirect

from .forms import EditCategoryForm  # Assuming you have a form for editing
# Update the imports
from .forms import EditCategoryForm


def edit_category(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)

    if request.method == 'POST':
        form = EditCategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_detail', category_pk)
    else:
        form = EditCategoryForm(instance=category)

    context = {'form': form}
    return render(request, 'admin/category/edit_category.html', context)


from django.shortcuts import redirect


def soft_delete_category(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    category.is_active = False
    category.save()
    return redirect('viewcategory')  # Redirect to category list page

from django.shortcuts import redirect, get_object_or_404


from django.shortcuts import redirect, get_object_or_404




def product_delete(request, product_pk):
    product = get_object_or_404(Products, pk=product_pk)
    if request.method == 'POST':
        if request.user.has_perm('products.delete_product'):
            product.soft_delete()
            return redirect('products_list')  # Redirect to product list
        else:
            pass
    else:
        pass
    return redirect('products_list') 


def soft_delete_product(request, product_pk):
    Product = get_object_or_404(Products, pk=product_pk)
    Product.is_active = False
    Product.save()
    return redirect('products_list')  # Redirect to category list page



from django.shortcuts import render, redirect
from product.models import DailyRate
from django.contrib.auth.decorators import login_required  # Assuming login is required

@login_required
def create_gold_rate(request):
    if request.method == 'POST':
        form = DailyRateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gold_rate_list')  # Redirect to list view
    else:
        form = DailyRateForm()

    return render(request, 'admin/goldrate/create_gold_rate.html', {'form': form})

from django.shortcuts import render


def gold_rate_list(request):
    # Get all gold rates, possibly with filters depending on your needs
    rates = DailyRate.objects.all().order_by('-date')

    return render(request, 'admin/goldrate/gold_rate_list.html', {'rates': rates})

