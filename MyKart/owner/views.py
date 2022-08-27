from django.shortcuts import render, redirect
from category.form import BrandForm, CategoryForm
from category.models import Brand, Category
from account.models import Account
from store.models import Product
from store.form import ProductForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url = 'login')
def logout(request):
   auth.logout(request)
   messages.success(request, 'You are Logout sucessfully')
   return redirect('index')

# This Function will take to admin dashboard page
@login_required(login_url = 'login')
def owner(request):
    return render(request, 'owner/dashboard.html')
 
# This Function will take to viewuser page
def users(request):
    users = Account.objects.all()
    return render(request, 'owner/users.html', {'users' : users})

# This Function will take to add user page
def adduser(request):
    return render(request, 'owner/adduser.html')


# This Function will delete user
def deleteuser(request, user_id):
    usr = Account.objects.get(pk=user_id)
    usr.delete()
    return redirect('users')

# This Function will Block user
def blockuser(request, user_id):
    user = Account.objects.get(pk=user_id)
    user.is_active = False
    user.save()
    return redirect('users')
    
# This Function will Un Block user    
def unblockuser(request, user_id):
    user = Account.objects.get(pk=user_id)
    user.is_active = True
    user.save()
    return redirect('users')




##########################################################################################

# This Function will take to view product page
def product(request):
    products = Product.objects.all()
    return render(request, 'owner/product.html', {'products' : products})


# This Function will take to add product page
def addnewproduct(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect('product')
        
    context = { 'form' : form}
    return render(request, 'owner/addproduct.html', context)



# This Function will delete product
def deleteproduct(request,product_id):
    pro = Product.objects.get(pk=product_id)
    pro.delete()
    return redirect('product')

# This Function will take to edit product page # This Function will Update
def product_edit(request, product_id):
    if request.method == "POST":
        pro_id = Product.objects.get(pk=product_id)
        fm = ProductForm(request.POST, instance=pro_id)
        if fm.is_valid():
            fm.save()
            return redirect('product')
    else:
        pro_id = Product.objects.get(pk=product_id)
        fm = ProductForm(instance=pro_id) 
        
    context ={
        'pro_id' : fm,
    }
    return render(request, 'owner/productedit.html', context)
    
 
 ######################################################################################
    
# This Function will take to show category page    
def category(request):
    categories = Category.objects.all()
    form = CategoryForm()
    context = { 
                'form' : form,
                'categories' : categories
        }
    return render(request, 'owner/category.html', context)


# This Function will take to add new category
def category_add(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category')
    return redirect('category')

# This Function will take to delete category
def category_delete(request, category_id):
    category = Category.objects.get(pk=category_id)
    category.delete()
    return redirect('category')

# This Function will take to Update Category
def category_edit(request, cat_id):
    if request.method == "POST":
        category_id = Category.objects.get(pk=cat_id)
        fm = CategoryForm(request.POST, request.FILES, instance=category_id)
        if fm.is_valid():
            fm.save()
            return redirect('category')
    else:
        category_id = Category.objects.get(pk=cat_id)
        fm = CategoryForm(instance=category_id) 
        
    context = {
        'cat_id' : fm,
    }
    # return redirect('category')
    return render(request, 'owner/category_edit.html', context)

############################################################

# This Function will take to show brand page
def brand(request):
    brands = Brand.objects.all()
    form = BrandForm()
    context = { 
                'form' : form,
                'brands' : brands
        }
    return render(request, 'owner/brand.html', context)


# This Function will take to add new brand
def brand_add(request):
    if request.method == "POST":
        form = BrandForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect('brand')
    return redirect('brand')

# This Function will take to delete brand
def brand_delete(request, brand_id):
    brand = Brand.objects.get(pk=brand_id)
    brand.delete()
    return redirect('brand')

# This Function will take to Update brand
def brand_edit(request, brand_id):
    if request.method == "POST":
        br_id = Brand.objects.get(pk=brand_id)
        fm = BrandForm(request.POST, instance=br_id)
        if fm.is_valid():
            fm.save()
            return redirect('brand')
    else:
        br_id = Brand.objects.get(pk=brand_id)
        fm = BrandForm(instance=br_id) 
        
    context ={
        'br_id' : fm,
    }
    return render(request, 'owner/brand_edit.html', context)