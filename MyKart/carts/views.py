from itertools import product
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from account.models import Address
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from coupon.models import Coupon, ReviewCoupon
from datetime import date

from django.http import HttpResponse

# Create your views here.

#This function will get session id
def _cart_id(request):                  # _cart_id is a private function
    cart = request.session.session_key  # geting session_key from browser
    if not cart:
        cart = request.session.create() # if no session create a new session
    return cart


#This function will will add items to cart or increment
def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) #get the product
    # If the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    # If the user is not authenticated
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # existing_variations -> database
            # current variation -> product_variation
            # item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

##########
# This function will remove cart items
def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def update_cart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        # print("from cart: "+ str(prod_id))
        if(CartItem.objects.filter(user=request.user, product__id=prod_id)):
            # print( product_id )
            # print(1)
            prod_qty = int(request.POST.get('product_qty'))
            cart = CartItem.objects.get(product__id=prod_id, user=request.user)
            cart.quantity= prod_qty
            cart.save()
            return JsonResponse({'status': "Updated Successfully"})
    return redirect('/')
    # return redirect('cart')
    
##########
# This function will take to cart  
def cart(request, total=0, quantity=0, cart_items=None):
    # print('from cart 1') 
    try:
        tax = 0
        amount = 0
        # print('from cart 2')
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active = True)
            # print('from cart 3')
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart = cart, is_active = True)
            # print('from cart 4')
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            # print('from cart 5')
        tax = (18 * total)/100
        # grand_total = total + tax     
        amount = total - tax
        
    except ObjectDoesNotExist:
        pass
    
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        # 'grand_total' : grand_total,
        'amount' : amount,
        
    }
    return render(request, 'store/cart.html', context)

# This function will take us to checkout
@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (18 * total)/100
        grand_total = total 
    except ObjectDoesNotExist:
        pass #just ignore
    
    addresses = Address.objects.filter(user=request.user)
    # addresses = UserProfile.objects.filter(user=request.user)
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
        'addresses' : addresses,
    }
    return render(request, 'store/checkout.html', context)

############################################################
# This function will check the coupen valid or not   #This function will apply coupon
@never_cache
@login_required(login_url="login")
def Check_coupon(request):

    if "coupon_code" in request.session:
        del request.session["coupon_code"]
        del request.session["amount_pay"]
        
    flag = 0
    discount_price = 0
    amount_pay = 0
    coupon_code = request.POST.get("coupon_code")
  
    grand_total = float(request.POST.get("grand_total"))
    print(coupon_code)
    if Coupon.objects.filter(code=coupon_code, coupon_limit__gte=1).exists():
        coupon = Coupon.objects.get(code=coupon_code)
        print(coupon)
        
        if coupon.active == True:
            flag = 1
            if not ReviewCoupon.objects.filter(user=request.user, coupon=coupon):
                today = date.today()

                if coupon.valid_from <= today and coupon.valid_to >= today:
                    discount_price = grand_total - coupon.discount

                    amount_pay = grand_total - discount_price
                    flag = 2
                    request.session["amount_pay"] = amount_pay
                    request.session["coupon_code"] = coupon_code
                    request.session["discount_price"] = discount_price

                    # Reduce Coupon Limit
                    coupon.coupon_limit = coupon.coupon_limit - 1
                    coupon.save()

                    # Move to ReviewCoupon if all coupons are used
                    if coupon.coupon_limit == 0:
                        reviewcoupon = ReviewCoupon()
                        reviewcoupon.user = request.user
                        reviewcoupon.coupon = coupon
                        reviewcoupon.save()
                    
                    


    context = {
        "amount_pay": amount_pay,
        "flag": flag,
        "discount_price": discount_price,
        "coupon_code": coupon_code,
    }

    return JsonResponse(context)
