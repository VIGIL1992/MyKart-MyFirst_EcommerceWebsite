from orders.models import Order, OrderProduct, STATUS1, Payment
from category.form import BrandForm, CategoryForm
from category.models import Brand, Category
from account.models import Account
from store.models import Product
from store.form import ProductForm, ProductGalleryForm

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
import datetime
from django.utils import timezone

import csv
from django.template.loader import render_to_string
import tempfile
from weasyprint import HTML

# Create your views here.

@login_required(login_url = 'login')
def logout(request):
   auth.logout(request)
   messages.success(request, 'You are Logout sucessfully')
   return redirect('index')

# This Function will take to admin dashboard page
@login_required(login_url = 'login')
@user_passes_test(lambda user: user.is_superadmin)
def owner(request):
    products = Product.objects.all()
    total_revenue = Order.objects.aggregate(Sum("order_total"))
    total_orders = OrderProduct.objects.filter(ordered=True).count()
    total_products = Product.objects.filter(is_available=True).count()
    total_user = Account.objects.filter(is_active=True).count()
    
    # Sales/orders
    current_year = timezone.now().year
    status2 = ["New","Placed","Shipped","Accepted","Delivered"]
    order_detail = OrderProduct.objects.filter(created_at__lt=datetime.date(current_year, 12, 31),ordered=True)
    # Using '__' we can access foreign key objects
    
    monthly_order_count = []
    month = timezone.now().month
       
    for i in range(1, month + 1):
        monthly_order = order_detail.filter(created_at__month=i).count() - order_detail.filter(created_at__month=i,status="Cancelled").count()
        monthly_order_count.append(monthly_order)

    # Status
    new_count = OrderProduct.objects.filter(status="New").count()
    placed_count = OrderProduct.objects.filter(status="Placed").count()
    shipped_count = OrderProduct.objects.filter(status="Shipped").count()
    accepted_count = OrderProduct.objects.filter(status="Accepted").count()
    delivered_count = OrderProduct.objects.filter(status="Delivered").count()
    cancelled_count = OrderProduct.objects.filter(status="Cancelled").count()

    # most moving product
    # most_moving_product_count = []
    # most_moving_product = []
    # for i in products:
    #     most_moving_product.append(i)
    #     most_moving_product_count.append(
    #         OrderProduct.objects.filter(product=i, status="New").count()
    #         )
    
    context = {
            "order_detail": order_detail,
            "monthly_order_count": monthly_order_count,
            "status_counter": [
                new_count,
                placed_count,
                shipped_count,
                accepted_count,
                delivered_count,
                cancelled_count,
            ],
            # "most_moving_product_count": most_moving_product_count,
            # "most_moving_product": most_moving_product,
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "total_products": total_products,
            "total_user" : total_user,
    }
    
    # print(monthly_order_count)
    return render(request, 'owner/dashboard.html', context )
 
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
@login_required(login_url = 'login')
@user_passes_test(lambda user: user.is_superadmin)
def blockuser(request, user_id):
    user = Account.objects.get(pk=user_id)
    user.is_active = False
    user.save()
    return redirect('users')
    
# This Function will Un Block user  
@login_required(login_url = 'login')
@user_passes_test(lambda user: user.is_superadmin)  
def unblockuser(request, user_id):
    user = Account.objects.get(pk=user_id)
    user.is_active = True
    user.save()
    return redirect('users')




##########################################################################################

# This Function will take to view product page # Display all Products
def product(request):
    products = Product.objects.all()
    return render(request, 'owner/product.html', {'products' : products})


# This Function will take to add product page
@login_required(login_url = 'login')
@user_passes_test(lambda user: user.is_superadmin)
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
@login_required(login_url = 'login')
@user_passes_test(lambda user: user.is_superadmin)
def deleteproduct(request,product_id):
    pro = Product.objects.get(pk=product_id)
    pro.delete()
    return redirect('product')

# This Function will take to edit product page # This Function will Update
@login_required(login_url = 'login')
@user_passes_test(lambda user: user.is_superadmin)
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
    
    
#Add Product Gallery
@login_required(login_url='login')
@user_passes_test(lambda user: user.is_superadmin)
def addproductgallery(request):
    form = ProductGalleryForm()

    if request.method == "POST":
        form = ProductGalleryForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("product")

    context = {"form": form}
    return render(request, "owner/addproductgallery.html", context)
 
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

############################################################

# This Function will let us see active orders
@login_required(login_url="login")
@user_passes_test(lambda user: user.is_superadmin)
def activeorders(request):
    exclude_list = ["Delivered", "Cancelled"]
    active_orders = OrderProduct.objects.all().exclude(status__in=exclude_list)[::-1]  # for reversing the order.
    status = STATUS1
    
    context = {
        "active_orders": active_orders,
        "status": status,
    }
    return render(request, "owner/activeorders.html", context)

# This Function will let us see completed orders
@login_required(login_url="login")
@user_passes_test(lambda user: user.is_superadmin)
def order_history(request):
    exclude_list = [
        "New",
        "Accepted",
        "Placed",
        "Shipped",
    ]
    active_orders = OrderProduct.objects.all().exclude(
        status__in=exclude_list
    )[::-1]
    status = STATUS1
    context = {
        "active_orders": active_orders,
        "status": status,
    }
    return render(request, "owner/order_history.html", context)


# This Function will let us see orders detail page
@login_required(login_url='login')
@user_passes_test(lambda user: user.is_superadmin)
def admin_order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)  # with the '__' we can access foreign key objects
    order = Order.objects.get(order_number=order_id)
    subtotal = 0

    for i in order_detail:
        subtotal = subtotal + i.product_price * i.quantity

    context = {
        "order_detail": order_detail,
        "order": order,
        "subtotal": subtotal,
    }

    return render(request, "owner/admin_order_detail.html", context)

# This Function will change order status to new to complete or
@login_required(login_url="login")
@user_passes_test(lambda user: user.is_superadmin)
def order_status_change(request):
    id = request.POST["id"]
    status = request.POST["status"]
    order_product = OrderProduct.objects.get(id=id)
    order_product.status = status
    order_product.save()
    return JsonResponse({"success": True})

######################################################################
# This Function will take us to product report page
@login_required(login_url="login")
@user_passes_test(lambda user: user.is_superadmin)
def product_report(request):
    products = Product.objects.all()
    orders = OrderProduct.objects.filter(ordered=True).order_by("-created_at")

    if request.GET.get("from"):
        date_from = datetime.datetime.strptime(
            request.GET.get("from"), "%Y-%m-%d"
        )
        date_to = datetime.datetime.strptime(
            request.GET.get("to"), "%Y-%m-%d"
        )
        date_to += datetime.timedelta(days=1)
        orders = OrderProduct.objects.filter(
            created_at__range=[date_from, date_to]
        )

    if request.GET.get("from"):
        date_from = datetime.datetime.strptime(
            request.GET.get("from"), "%Y-%m-%d"
        )
        date_to = datetime.datetime.strptime(
            request.GET.get("to"), "%Y-%m-%d"
        )
        date_to += datetime.timedelta(days=1)
        products = Product.objects.filter(
            created_date__range=[date_from, date_to]
        )

    context = {
        "products": products,
        "orders": orders,
    }
    return render(request, "owner/product_report.html", context)


# This Function will take us to sales report page
@login_required(login_url="login")
@user_passes_test(lambda user: user.is_superadmin)
def sales_report(request):
    products = Product.objects.all()
    orders = OrderProduct.objects.filter(ordered=True).order_by("-created_at") and OrderProduct.objects.exclude(status="Cancelled").order_by("-created_at")

    if request.GET.get("from"):
        date_from = datetime.datetime.strptime(
            request.GET.get("from"), "%Y-%m-%d"
        )
        date_to = datetime.datetime.strptime(
            request.GET.get("to"), "%Y-%m-%d"
        )
        date_to += datetime.timedelta(days=1)
        orders = OrderProduct.objects.filter(
            created_at__range=[date_from, date_to]
        )

    if request.GET.get("from"):
        date_from = datetime.datetime.strptime(
            request.GET.get("from"), "%Y-%m-%d"
        )
        date_to = datetime.datetime.strptime(
            request.GET.get("to"), "%Y-%m-%d"
        )
        date_to += datetime.timedelta(days=1)
        products = Product.objects.filter(
            created_date__range=[date_from, date_to]
        )

    context = {
        "products": products,
        "orders": orders,
    }
    return render(request, "owner/sales_report.html", context)


######################################################################
# This Function will let us export product csv
@login_required(login_url="login")
@user_passes_test(lambda user: user.is_superadmin)
def product_export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response[
        "Content-Disposition"
    ] = 'attachement; filename=Product_Report_' + \
        str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(
        [
            "Product Name",
            "Brand Name",
            "Category Name",
            "Rating",
            "Price",
            "Stock",
        ]
    )

    products = Product.objects.all().order_by("id")

    for product in products:
        writer.writerow(
            [
                product.product_name,
                product.category,
                product.averageReview(),
                product.price,
                product.stock,
            ]
        )

    return response

# This Function will let us export product pdf
@login_required(login_url="login")
@user_passes_test(lambda user: user.is_superadmin)
def product_export_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; attachement; filename=Product_Report.pdf"

    response["Content-Transfer-Encoding"] = "binary"

    products = Product.objects.all().order_by("id")

    html_string = render_to_string(
        "owner/product_pdf_output.html", {"products": products, "total": 0}
    )

    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        # output = open(output.name, "rb")
        response.write(output.read())

    return response

# This Function will let us export product csv
@login_required(login_url="login")
@user_passes_test(lambda user: user.is_superadmin)
def sales_export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=orders.csv"

    writer = csv.writer(response)
    orders = OrderProduct.objects.filter(ordered=True).order_by("-created_at")

    writer.writerow(
        [
            "Order Number",
            "Customer",
            "Product",
            "Amount",
            "Payment",
            "Qty",
            "Status",
            "Date",
        ]
    )

    for order in orders:
        writer.writerow(
            [
                order.order.order_number,
                order.user.full_name(),
                order.product,
                order.product_price,
                order.payment.payment_method,
                order.quantity,
                order.status,
                order.updated_at,
            ]
        )
    return response


@login_required(login_url="login")
@user_passes_test(lambda user: user.is_superadmin)
def sales_export_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response[
        "Content-Disposition"
    ] = "inline; attachement; filename=sales_report.pdf"

    response["Content-Transfer-Encoding"] = "binary"

    orders = OrderProduct.objects.filter(ordered=True).order_by("-created_at")

    html_string = render_to_string(
        "owner/sales_pdf_output.html", {"orders": orders, "total": 0}
    )

    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, "rb")
        response.write(output.read())

    return response
