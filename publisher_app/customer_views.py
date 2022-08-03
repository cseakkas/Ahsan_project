from django.shortcuts import render, redirect
from . import models
from publisher_app.utils import render_to_pdf
from django.http import HttpResponse
from django.http import HttpRequest  
import datetime
from django.utils import timezone
import re, os
import django.conf as conf
from PIL import Image
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
import random
from random import randint
from django.db.models import Sum,Max,Min,Count,Q,F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time 
from datetime import datetime, timedelta, tzinfo
from django.utils import timezone
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
# import urllib.parse
from urllib.parse import urlparse
from datetime import datetime, time
import datetime

 
def my_account(request): 
    if request.session['userid'] == False:
        return redirect('/customer/login/')

    customer_id = request.session.get('userid')
    session_key = request.session.get("abcd")  
    cart_item = models.AddToCart.objects.filter(session_key = session_key)
    print("cart_item :", len(cart_item))
    total_price =  cart_item.aggregate(Sum('qt_price'))['qt_price__sum']
    customer  = models.CustomarAccount.objects.filter(id = request.session.get('userid'), status = True).first()
    
    if request.is_ajax():
        customer_id      = int(request.POST.get('customer_id'))
        current_password = request.POST.get('current_password')
        confirm_password = request.POST.get('confirm_password')
        match_pass = models.CustomarAccount.objects.filter(id = customer_id, password = current_password ).first()

        if match_pass:
            models.CustomarAccount.objects.filter(id = customer_id).update(
                password = confirm_password
            )
            data = "Password Change Successful"
            return JsonResponse(data, safe=False) 
        else:
            data = "Current Password Not Match"
            return JsonResponse(data, safe=False) 
    
    
    context = {
        'count' : models.AddToCart.objects.filter(session_key = session_key).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
        'total_price' : total_price,
        'customer' : customer,
        'website_menu': models.MastarSubCategory.objects.filter(status = True, regular_category__Is_top_category = True).order_by('master_category', 'regular_category'),
    }
    return render(request, 'publisher_app/customer_panel/my_account.html', context)



def my_cart_items(request):
    if request.session['userid'] == False:
        return redirect('/customer/login/')

    
    customer_id = request.session.get('userid')
    session_key = request.session.get("abcd")  
    cart_item = models.AddToCart.objects.raw("SELECT id, book_name_id, quantity, qt_price, (quantity*qt_price) as total_price FROM `addtocart` WHERE session_key = %s", [session_key])
 
    context = {
        'count' : models.AddToCart.objects.filter(session_key = session_key).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
        'cart_item': cart_item,
        'website_menu': models.MastarSubCategory.objects.filter(status = True, regular_category__Is_top_category = True).order_by('master_category', 'regular_category'),
    }
    return render(request, 'publisher_app/customer_panel/my_cart_items.html', context)

def my_wishlist_items(request):
    if request.session['userid'] == False:
        return redirect('/customer/login/')

    customer_id = request.session.get('userid')
    session_key = request.session.get("abcd")  
    wishlist_item = models.AddToWishlist.objects.raw("""
        SELECT bk.id, bk.book_name_bangla, bk.slug, bk.book_image, bk.book_price, bk.sale_price, IF(bk.cover_type = 1, 'পেপারব্যাক', 'হার্ডকভার') as cover_type,
        bp.publisher_name_bangla, bw.writter_name_bangla, bk.discount FROM add_to_wishlist wl 
        INNER JOIN book_list bk ON wl.book_name_id = bk.id INNER JOIN book_publisher_list bp ON bk.publisher_id = bp.id
        INNER JOIN writter_wise_book wwb ON wwb.book_name_id = bk.id INNER JOIN book_writter_list bw ON bw.id = wwb.writter_name_id
        where wl.session_key = %s and bk.status = 1 order by wl.id desc""", [session_key])
    context = {
        'wishlist_item':wishlist_item,
        'count' : models.AddToCart.objects.filter(session_key = session_key).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
        'website_menu': models.MastarSubCategory.objects.filter(status = True, regular_category__Is_top_category = True).order_by('master_category', 'regular_category'),
         
    }
    return render(request, 'publisher_app/customer_panel/my_wishlist_items.html', context)

def my_wishlist_items_delete(request,book_name):
    if request.session['userid'] == False:
        return redirect('/customer/login/')
        
    models.AddToWishlist.objects.filter(book_name_id = book_name, session_key = request.session.get('abcd')).delete()
    return redirect('/my-wishlist/')
    

def my_order_list(request):
    if request.session['userid'] == False:
        return redirect('/customer/login/')
    
    user_id =  request.session.get('userid')
    session_key = request.session.get('abcd')

    if request.is_ajax():
        OrderId = request.GET.get('OrderId')
        
        models.SalesOrder.objects.filter(order_number = OrderId).update(
            order_status = 7, update_date =  datetime.datetime.now()
        )
        data = "Order Cancel Successful."
        return JsonResponse(data, safe=False)
 

    if request.method == "GET": 
        orderlist = ""
        order_list = models.SalesOrder.objects.filter( customer_name_id = user_id)
        total_order_list = len(list(order_list))

        page_number = request.GET.get('page')
        if request.method == "POST":
            btnvalue = request.POST.get('btnPage')
            page_number = btnvalue
        index_count = 0
        if page_number and int(page_number) > 1:
            index_count = 25 * (int(page_number)-1)

        paginator = Paginator(order_list, 25)
        pagination = paginator.get_page(page_number)
        if page_number is None:
            page_number = 1
            
        order_list =  order_list[index_count:25 * int(page_number)] 

        context = {
            'count' : models.AddToCart.objects.filter(session_key = request.session.get('abcd')).count(),
            'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
            'order_list': order_list,
            'order_list_len': total_order_list, 
            "index_count": index_count,
            "page_number": pagination, 
            "current_page_no": page_number,  
            'website_menu': models.MastarSubCategory.objects.filter(status = True, regular_category__Is_top_category = True).order_by('master_category', 'regular_category'),
        }
        return render(request, 'publisher_app/customer_panel/my_order_list.html', context) 

    else:
        order_number = request.POST['order_number']
        order_status = request.POST['order_status'] 
 
        total_order_list = models.SalesOrder.objects.filter( customer_name_id = user_id) 
 
        my_order_list = "" 
        my_order_list = models.SalesOrder.objects.filter( customer_name_id = user_id).order_by('-id') 
        get_filter_order = len(list(my_order_list))

        page_number = request.GET.get('page')
        if request.method == "POST":
            btnvalue = request.POST.get('btnPage')
            page_number = btnvalue
        index_count = 0
        if page_number and int(page_number) > 1:
            index_count = 24 * (int(page_number)-1)

        paginator = Paginator(my_order_list, 24)
        pagination = paginator.get_page(page_number)
        if page_number is None:
            page_number = 1
            
        my_order_list =  my_order_list[index_count:24 * int(page_number)] 

        context = {
            'total_order_list':total_order_list,
            'my_order_list':my_order_list,
            'my_order_list_len':get_filter_order, 
            'order_number':order_number,
            'order_status':order_status,
            "index_count": index_count,
            "page_number": pagination, 
            "current_page_no": page_number,
            'count' : models.AddToCart.objects.filter(session_key = request.session.get('abcd')).count(),
            'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
            'website_menu': models.MastarSubCategory.objects.filter(status = True, regular_category__Is_top_category = True).order_by('master_category', 'regular_category'),
        }
        return render(request, 'publisher_app/customer_panel/my_order_list.html', context)

 
def my_order_view(request, order_number):
    if request.session['userid'] == False:
        return redirect('/customer/login/')

    session_key = request.session.get('abcd')
    user_id = request.session.get('userid') 
 
    get_order_items = models.SalesDetails.objects.raw("""
        SELECT sod.id, bk.id as book_id, bk.slug as book_slug, bk.book_name_bangla, bk.book_name_english, 
        sod.order_number, sod.book_price, sod.sale_price, sod.book_quantity, (sod.sale_price * sod.book_quantity) as total_sales_price, 
        bk.book_image, bk.cover_type, bw.writter_name_bangla, pub.publisher_name_bangla FROM sales_details sod 
        INNER JOIN book_list bk on sod.book_name_id = bk.id
        INNER JOIN writter_wise_book wwb ON bk.id = wwb.book_name_id 
        INNER JOIN book_writter_list bw ON wwb.writter_name_id = bw.id
        INNER JOIN book_publisher_list pub ON bk.publisher_id = pub.id
        WHERE sod.order_number = %s """, [order_number]
    )
    
    order_summary = models.SalesOrder.objects.filter(order_number = order_number).first()
    
    total_amount = order_summary.total_amount
    vat_amount = order_summary.vat_amount
    discount_amount = order_summary.discount_amount
    shipping_charge = order_summary.shipping_charge
    less_amount = order_summary.less_amount
    due_amount = order_summary.due_amount 
    grand_total = ((total_amount + shipping_charge + vat_amount) - less_amount)  
    context = {
        'count' : models.AddToCart.objects.filter(session_key = request.session.get('abcd')).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
        'get_order_items':get_order_items,
        'shipping_charge':shipping_charge,
        'order_summary':order_summary,
        'vat_amount':vat_amount,
        'subtotal':total_amount, 
        'less_amount':less_amount,
        'due_amount':due_amount,
        'discount_amount':discount_amount,
        'grand_total':grand_total,
        'website_menu': models.MastarSubCategory.objects.filter(status = True, regular_category__Is_top_category = True).order_by('master_category', 'regular_category'),
    }
    return render(request, 'publisher_app/customer_panel/mycart_item_view.html', context)



def customer_profile_update(request, id):
    if request.session['userid'] == False:
        return redirect('/customer/login/')

    get_pro_id = models.CustomarAccount.objects.get(id = id)
  
    if request.method=="POST":
 
        customer_profile_images = str(get_pro_id.profile_images) if get_pro_id.profile_images else ""
        if bool(request.FILES.get('profile_images', False)) == True:
            if os.path.exists(str(customer_profile_images)):
                os.remove(str(get_pro_id.customer_profile_images))

            file = request.FILES['profile_images']
            customer_profile_images = "profile_images/"+file.name
            if not os.path.exists("profile_images/"):
                os.mkdir("profile_images/")
            customer_profile_images = default_storage.save("profile_images/"+file.name, ContentFile(file.read()))
            if customer_profile_images:
                customer_profile_images = str("profile_images/")+str(customer_profile_images).split("/")[-1]
         
        data = models.CustomarAccount.objects.filter(id=id).update(
            customer_name = request.POST['customer_name'], mobile = request.POST['customer_mobile'],
            email = request.POST['customer_email'], address = request.POST['full_address'], profile_images = customer_profile_images,
        )
        if data:
            request.session['customername'] = request.POST['customer_name']
            request.session['customer_photo'] = customer_profile_images
              
            messages.success(request, "Profile Update Successful.")
            return redirect("/my-account/")
        
        else:
            messages.error(request, "Profile Update Failed")
            return redirect("/my-account/")


    context = {
        'count' : models.AddToCart.objects.filter(session_key = request.session.get('abcd')).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
        'get_pro_id' : get_pro_id,
        'website_menu': models.MastarSubCategory.objects.filter(status = True, regular_category__Is_top_category = True).order_by('master_category', 'regular_category'),
    }
    return render(request, 'publisher_app/customer_panel/update_customer_account.html', context)
 

