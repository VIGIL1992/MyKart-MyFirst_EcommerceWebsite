from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth

from .models import Account, UserProfile
from .forms import RegistrationForm, UserForm, UserProfileForm, AddressForm
from orders.models import Order, OrderProduct
from account.models import Address
from carts.views import _cart_id
from carts.models import Cart, CartItem
from store.models import Product

# Razorpay
from orders.models import Payment
import razorpay
from django.conf import settings


#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

import requests

# Create your views here.

#This function will register new Users
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phonenumber = form.cleaned_data['phonenumber']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            
            user = Account.objects.create_user( first_name=first_name, last_name=last_name, email=email, username=username, password=password )
            user.phonenumber = phonenumber
            user.save()
            
            #USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string('accounts/account_verification_email.html',{
                'user': user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            
            # messages.success(request, 'Thanks for registering, we have send you a verification email to your email address, Please verfy it')
            return redirect('/account/login/?command=verification&email='+email)
           
    else:
        form = RegistrationForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/register.html', context)

#This function will check the Username and Password
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            try:
                print("from try block")
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                print(is_cart_item_exists)
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    print(cart_item)

                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                print("from execpt block")
                pass  
            
            auth.login(request, user)
            messages.success(request, 'you are logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                # return redirect('user_dashboard')
                return redirect('index')
             
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')
        
    return render(request, 'accounts/signin.html')


@login_required(login_url = 'login')
def logout(request):
   auth.logout(request)
   messages.success(request, 'You are Logout sucessfully')
   return redirect('login')
   

#This function will activate user account
#user Activation  
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
       
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations your account is activated')
        return redirect('login')
    else:
        messages.success(request, 'Invalid activation link')
        return redirect('register')

####################################################################################        
#This function will take to the user dashboard and its functions        
@login_required(login_url = 'login')
def user_dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()

    userprofile = UserProfile.objects.get(user_id=request.user.id)  # for getting user profile for user images
    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/user_dashboard.html', context)

##########################################################################

#This function will
def forgetPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact=email)
            
            #RESET PASSWORD EMAIL
            current_site = get_current_site(request)
            mail_subject = "Reset your password"
            message = render_to_string('accounts/reset_password _email.html',{
                'user': user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            
            messages.success(request, 'Password Reset email has been sent to your email address')
            return redirect('login')
            
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgetPassword') 
        
    return render(request, 'accounts/forgetPassword.html')



def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link is expired')
        return redirect('login')
    
    
def resetPassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset sucessfully')
            return redirect('login')
        else:
            messages.error(request, 'Password is does not match!')
            return redirect('resetPassword')
                                    
    else:
        return render(request, 'accounts/resetPassword.html')
    
#####################################################################################################    
@login_required(login_url='login')
def my_orders(request):
    orderproducts = OrderProduct.objects.filter(user=request.user,ordered=True).order_by("-created_at")
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
        'orderproducts': orderproducts,
    }
    return render(request, 'accounts/my_orders.html', context)

@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'accounts/order_detail.html', context)


def cancel_order(request,pk):
    product = OrderProduct.objects.get(pk=pk)
    
    messages.success(request,"Order has been cancelled and refund initiated")
    
    payment_id = product.payment.id

    order = Order.objects.get(user=request.user,payment_id=payment_id)

    payment = product.payment


    if str(payment).__contains__("pay"):
        
        paymentId = payment
        amount = int(product.order_total)
        refund_amount = int(amount*100)
        
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        
        client.payment.refund(paymentId,{
            "amount": refund_amount,
            "speed": "optimum",
        })
        product = OrderProduct.objects.get(pk=pk)
        product.status = 'Cancelled'
        product.order_total = 0
        product.save()
    
        item = Product.objects.get(pk=product.product.id)
        item.stock += product.quantity
        item.save()

    else:
        product = OrderProduct.objects.get(pk=pk)
        product.status = 'Cancelled'
        product.order_total = 0
        product.save()
    
        item = Product.objects.get(pk=product.product.id)
        item.stock += product.quantity
        item.save()

    
    # mail_subject = 'Order Cancellation'
    # message = render_to_string('orders/order_cancelled_email.html', {
    #     'user': request.user,
    #     'order': order,
    # })
    # to_email = request.user.email
    # send_email = EmailMessage(mail_subject, message, to=[to_email])
    # send_email.send()

    return redirect('my_orders')

################################################################################################

#Wishlist - add to wishlist
@login_required(login_url = 'login')
def add_to_wishlist(request,id):
    product = get_object_or_404(Product,id=id)
    if product.user_wishlist.filter(id=request.user.id).exists():
        messages.error(request,"Product already in wishlist")
    else:
        product.user_wishlist.add(request.user)
        messages.success(request,"Successfully added to wishlist")
    return redirect('wishlist')


#Wishlist - delete from wishlist
@login_required(login_url = 'login')
def delete_wishlist(request,id):
    product = get_object_or_404(Product,id=id)
    product.user_wishlist.remove(request.user)
    messages.success(request,"Removed from wishlist")
    return redirect('wishlist')


#Wishlist
def wishlist(request):
    products = Product.objects.filter(user_wishlist=request.user)
    context = {
        'products': products
    }
    return render(request,'accounts/wishlist.html',context)

###########################################################################

@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)

################################################################################################
@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')





############################################################################
# Address Management
@login_required(login_url="login")
def add_address(request):
    form = AddressForm()
    addresses = Address.objects.filter(user=request.user)

    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, "New Address added successfully")
            return redirect("add_address")

    context = {"form": form, "addresses": addresses}
    return render(request, "accounts/add_address.html", context)


@login_required(login_url = 'login')
def edit_address(request, pk):
    address = Address.objects.get(pk=pk)
    form = AddressForm(instance=address)

    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)

        if form.is_valid():
            form.save()
            messages.success(request, "Your address has been updated")
            return redirect("add_address")

    context = {"form": form}
    return render(request, "accounts/edit_address.html", context)


@login_required(login_url = 'login')
def delete_address(request, pk):
    dlt = Address.objects.filter(id=pk)
    print(dlt)
    dlt.delete()
    messages.success(request, "Your Address has been deleted")
    return redirect("add_address")


@login_required(login_url = 'login')
def set_default_address(request, pk):
    Address.objects.filter(user=request.user, default=True).update(
        default=False
    )
    address = Address.objects.get(pk=pk)
    address.default = True
    address.save()
    messages.success(request, "Default address changed")
    return redirect("add_address")

###################################################################


