from urllib import response
from django.shortcuts import redirect, render 
from . import models
from publisher_app.utils import render_to_pdf
from django.http import HttpResponse
from django.http import HttpRequest   
from django.utils import timezone
import re, os
from publisher_app.decorators import employeeLogin
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
from datetime import datetime, timedelta, tzinfo, date 
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
from django.core.mail import send_mail
from django.http import HttpResponseRedirect 
from urllib.parse import urlparse 
import requests
import json
import datetime 
from num2words import num2words

# This is test 
# This is test Project by akkas.

def check_user_permission(request, menu_url):
    chk_privilege    = models.UserAccessControl.objects.filter(user_id = int(request.session.get("user_id")), menu_id__menu_url = menu_url, menu_id__status = True, status = True).first()
    
    if chk_privilege: return chk_privilege
    else: None
  
def index_page(request):
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)
 
    slider_list = models.SliderInfo.objects.filter(status = True).order_by('slider_order') 
    today_date = date.today()  
    one_month_ago = today_date - datetime.timedelta(days=130) 
    
    new_pub_book_list = models.BookList.objects.raw('''
        SELECT bk.id, bk.book_name_bangla, bk.book_name_english, bk.sale_price, bk.book_price, bk.discount, bc.cat_name_bangla, cwb.category_name_id, bc.menu_url, bw.writter_name_bangla FROM book_list bk 
        LEFT JOIN category_wise_book cwb ON bk.id = cwb.book_name_id
        LEFT JOIN book_category_list bc ON cwb.category_name_id = bc.id LEFT JOIN writter_wise_book wwb ON bk.id = wwb.book_name_id
        LEFT JOIN book_writter_list bw ON  wwb.writter_name_id = bw.id WHERE bk.status = 1 and bc.Is_homepage = 1 and (bk.add_date >= %s and bk.add_date <= %s) and bc.id = 7  GROUP by wwb.book_name_id ORDER BY bk.id desc limit 12
    ''', [one_month_ago, today_date])

    book_list = models.BookList.objects.raw('''
        SELECT bk.id, bk.book_name_bangla, bk.book_name_english, bk.sale_price, wl.book_name_id as wl_id, bk.book_price, bk.discount, bc.cat_name_bangla, cwb.category_name_id, bc.menu_url, bw.writter_name_bangla FROM book_list bk 
        LEFT JOIN category_wise_book cwb ON bk.id = cwb.book_name_id LEFT JOIN add_to_wishlist wl ON wl.book_name_id = bk.id
        LEFT JOIN book_category_list bc ON cwb.category_name_id = bc.id LEFT JOIN writter_wise_book wwb ON bk.id = wwb.book_name_id
        LEFT JOIN book_writter_list bw ON  wwb.writter_name_id = bw.id WHERE bk.status = 1 and bc.Is_homepage = 1 and bc.id <> 7 GROUP by wwb.book_name_id ORDER BY bc.ordering asc, bc.cat_name_bangla ASC, bk.id desc 
    ''')
    writer_book = models.BookList.objects.raw('''
        SELECT bw.id, bw.writter_name_bangla, COUNT(bw.id) as total_book, bw.menu_url,bw.writter_images FROM `book_list` bk 
        LEFT JOIN writter_wise_book wwb ON bk.id = wwb.book_name_id
        LEFT JOIN book_writter_list bw ON wwb.writter_name_id = bw.id  GROUP BY bw.id order by COUNT(bw.id) DESC limit 20'''
    )
 
    wish_list = models.AddToWishlist.objects.filter(session_key = request.session.get("abcd"))
    if request.method == "POST": 
        search_txt = request.POST['search_txt']  
        search_book_list = models.BookList.objects.filter(Q(book_name_english = search_txt) | Q(book_name_bangla = search_txt))
        context  = {
            'search_book_list':search_book_list,
        }
        return render(request,'publisher_app/search_products.html', context)
    
    if request.is_ajax():
        book_name_id = request.GET.get('book_id')
        cart_items_list = models.AddToCart.objects.filter( book_name_id = book_name_id, session_key = request.session.get("abcd")).first()
        if not cart_items_list:
            models.AddToCart.objects.create(
                book_name_id = request.GET.get('book_id'), qt_price = request.GET.get('sale_price'),
                book_price = request.GET.get('book_price'), discount = request.GET.get('discount'), 
                session_key = request.session.get("abcd"),  
            )
            data = "success"
            return JsonResponse(data, safe=False) 
        else:
            data = "Book Already Exsit"
            return JsonResponse(data, safe=False) 
    
    cart_item = models.AddToCart.objects.filter(session_key = request.session.get("abcd"))
    get_cart_item = []
    for data in cart_item:
        get_item_id = data.book_name_id
        get_cart_item.append(get_item_id) 
     
    total_price =  cart_item.aggregate(Sum('qt_price'))['qt_price__sum']
    # recent_book_list = models.AddToRecentView.objects.filter(session_key = request.session.get("abcd")).order_by('-id')
 
    context = {
        'new_pub_book_list':new_pub_book_list,
        'slider_list':slider_list,
        'book_list':book_list,  
        'wish_list':wish_list,  
        'cart_item' : cart_item, 
        'writer_book' : writer_book, 
        'get_cart_item' : get_cart_item,  
        'count' : models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
        'total_price' : total_price,   
        'prev_images' : models.PreviewImages.objects.raw("SELECT * FROM book_list bk INNER JOIN preview_images pi ON bk.id = pi.book_name_id GROUP BY bk.id"),
    } 
    return render(request, 'publisher_app/index.html', context)
 

def addToWishList(request):
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)

    session_key = request.session.get("abcd")
    if request.is_ajax():
        book_name_id = request.GET.get('book_id') 
        wl_status = request.GET.get('status')  
        wishlist_item = models.AddToWishlist.objects.filter(book_name_id = book_name_id, session_key = session_key).first() 
        if not wishlist_item:
            models.AddToWishlist.objects.create(
                book_name_id = book_name_id, session_key = session_key,
            ) 
            data = "active"
            return JsonResponse(data, safe=False) 
        else:
            models.AddToWishlist.objects.filter(book_name_id = book_name_id).delete()
            data = "inactive"
            return JsonResponse(data, safe=False) 
 

def AdvanceBookSearch(request): 
    search_text = "" 
    if request.is_ajax():
        book_name_id = request.GET.get('book_id')
        cart_items_list = models.AddToCart.objects.filter(book_name_id = book_name_id, session_key = request.session.get("abcd")).first()
        if not cart_items_list:
            models.AddToCart.objects.create(
                book_name_id = request.GET.get('book_id'), qt_price = request.GET.get('sale_price'),
                book_price = request.GET.get('book_price'), discount = request.GET.get('discount'),
                session_key = request.session.get("abcd")
            )
            data = "success"
            return JsonResponse(data, safe=False) 
        else:
            data = "Book Already Exsit"
            return JsonResponse(data, safe=False) 

    if request.method == "POST":
        search_text = request.POST.get('search_txt').strip()    
        src_data_txt = str("%")+search_text+str("%")
        
        book_list = models.BookList.objects.raw("""
            SELECT bk.id as book_id, bk.book_name_bangla, bk.book_name_english, wwb.book_name_id, wwb.writter_name_id, bw.id, bk.book_image, bk.slug as book_url, 
            bw.writter_name_bangla, bw.writter_name_english, bp.publisher_name_bangla, bp.publisher_name_english, bk.book_price, bk.sale_price, bk.discount as book_sale_discount FROM book_list bk 
            left join writter_wise_book wwb ON bk.id = wwb.book_name_id 
            left join book_publisher_list bp ON bk.publisher_id = bp.id
            LEFT JOIN book_writter_list bw ON wwb.writter_name_id = bw.id
            WHERE bk.status <> 0 and (bk.book_name_bangla like %s OR bk.book_name_english like %s OR bp.publisher_name_bangla like %s OR bp.publisher_name_english like %s OR bw.writter_name_bangla like %s OR bw.writter_name_english like %s ) GROUP BY wwb.book_name_id limit 15
        """,[src_data_txt, src_data_txt, src_data_txt, src_data_txt, src_data_txt, src_data_txt])
         
        context = {
            'book_list':book_list,
            'search_text':search_text,
            'count' : models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count(),
            'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
        }
        return render(request, 'publisher_app/advance_search.html', context)
    else:
        context = { 
            'search_text':search_text,
            'count' : models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count(),
            'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
        }
        return render(request, 'publisher_app/index.html', context)


getBookId = None
def book_details(request, id, slug):
    view_book_id = id
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)
    
    getcatid = models.BookList.objects.get(id = id)
    # recent_book_list = models.AddToRecentView.objects.filter( session_key = request.session.get("abcd")).exclude(book_name_id=id).order_by('-id') 
    global getBookId
    def getBookId():
        return view_book_id

    get_review = models.ClientReview.objects.filter(book_name_id = id).order_by('-id')
    category = models.CategoryWiseBook.objects.filter(book_name_id = getcatid.id)
    parent_cat = category[0].category_name_id  
    related_books = models.BookList.objects.raw('''
        SELECT bk.id, bk.book_name_bangla, bk.book_name_english, bk.sale_price, wl.book_name_id as wl_id, bk.book_price, bk.discount, bc.cat_name_bangla, cwb.category_name_id, bc.menu_url, bw.writter_name_bangla FROM book_list bk 
        LEFT JOIN category_wise_book cwb ON bk.id = cwb.book_name_id LEFT JOIN add_to_wishlist wl ON wl.book_name_id = bk.id
        LEFT JOIN book_category_list bc ON cwb.category_name_id = bc.id  
        LEFT JOIN writter_wise_book wwb ON bk.id = wwb.book_name_id
        LEFT JOIN book_writter_list bw ON  wwb.writter_name_id = bw.id  
        WHERE bk.status = 1 and bk.id <> %s and cwb.category_name_id = %s GROUP by wwb.book_name_id
    ''', [id, parent_cat])

    ### Package Book List 
    package_book_list = models.BookPackageDetails.objects.raw("""
        SELECT bk.id, bpd.book_name_id as book_id, bk.book_name_bangla,bk.slug as book_url, bk.book_price, bk.sale_price, bk.discount, bw.writter_name_bangla, bc.cat_name_bangla, bk.book_image  FROM `book_package_list` bpd 
        LEFT JOIN book_list bk ON bpd.book_name_id = bk.id
        LEFT JOIN category_wise_book cwb ON bk.id = cwb.book_name_id  
        LEFT JOIN writter_wise_book wwb ON bk.id = wwb.book_name_id
        LEFT JOIN book_writter_list bw ON  wwb.writter_name_id = bw.id  
        LEFT JOIN book_category_list bc ON cwb.category_name_id = bc.id
        WHERE bpd.booklist_master_id = %s GROUP by bk.id ORDER BY bk.id asc
    """,[getcatid.id])
 
    total_package_price = models.BookList.objects.raw("SELECT id, book_price as total_book_price, sale_price as total_sale_price, (book_price - sale_price) as total_save_price FROM book_list  WHERE id = %s", [getcatid.id])
    
    session_key = request.session.get("abcd")
    wish_list = models.AddToWishlist.objects.filter(session_key = session_key)
    is_wish_list_item = models.AddToWishlist.objects.filter(book_name_id = id, session_key = session_key).first()
    writter = models.WritterWiseBook.objects.filter(book_name_id = getcatid.id)
    translator = models.TranslatorWiseBook.objects.filter(book_name_id = getcatid.id)
    editor_list    = models.EditorWiseBook.objects.filter(book_name_id = getcatid.id)
    writter_details = models.WritterWiseBook.objects.filter(book_name_id = getcatid.id).first()
    
    save_amount = int(getcatid.book_price) - int(getcatid.sale_price)
    book_offer = models.ProductOffer.objects.filter(status = True)
    preview_file = models.PreviewPdfFile.objects.filter(book_name_id = getcatid.id).last()

    cart_item = models.AddToCart.objects.filter(session_key = request.session.get("abcd"))
    total_price =  cart_item.aggregate(Sum('qt_price'))['qt_price__sum']

    if request.is_ajax():
        book_name_id = request.GET.get('book_id')
        cart_items_list = models.AddToCart.objects.filter( book_name_id = book_name_id, session_key = request.session.get("abcd")).first()
        if not cart_items_list:
            models.AddToCart.objects.create(
                book_name_id = request.GET.get('book_id'), qt_price = request.GET.get('sale_price'),
                book_price = request.GET.get('book_price'), discount = request.GET.get('discount'),
                quantity = request.GET.get('view_bookqty'), session_key = request.session.get("abcd"),
            )
            data = "success"
            return JsonResponse(data, safe=False) 
        else:
            data = "Book Already Exsit"
            return JsonResponse(data, safe=False) 
            
    context = {
        'getcatid' : getcatid,
        'preview_file' : preview_file,
        'cart_item' : cart_item,
        'count' : models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
        'total_price' : total_price,
        'save_amount' : save_amount,
        'wish_list' : wish_list,
        'is_wish_list_item' : is_wish_list_item,
        'book_offer' : book_offer,
        'category' : category,
        'writter' : writter,
        'editor_list' : editor_list,
        'translator' : translator,
        'writter_details' : writter_details,
        'get_review' : get_review, 
        'related_books' : related_books, 
        # 'recent_book_list' : recent_book_list, 
        'package_book_list' : package_book_list, 
        'total_book_price' : total_package_price[0].total_book_price, 
        'total_sale_price' : total_package_price[0].total_sale_price,  
        'total_save_price' : total_package_price[0].total_save_price,  
    }
    return render(request,'publisher_app/view_details.html', context)



def add_to_cart_page(request): 
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)
        
    session_key = request.session.get("abcd")
    count = models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count() 
    if count > 0:
        cart_item = models.AddToCart.objects.raw('''
            SELECT cart.id, cart.book_name_id, cart.book_price, cart.qt_price, ((cart.book_price-cart.qt_price)*cart.quantity) as save_price, (cart.quantity*cart.book_price) as total_book_price, 
            (cart.quantity*cart.qt_price) as total_price, cart.quantity, wwb.book_name_id, wwb.writter_name_id, 
            bw.writter_name_bangla FROM `add_to_cart`cart LEFT JOIN writter_wise_book 
            wwb ON cart.book_name_id = wwb.book_name_id LEFT JOIN book_writter_list bw ON wwb.writter_name_id = bw.id 
            LEFT JOIN book_list bk on bk.id = cart.book_name_id  WHERE bk.status = 1 and session_key = %s GROUP BY cart.book_name_id''', [session_key]
        )
        save_amount = 0
        for i in cart_item:
            save_amount = save_amount + i.save_price
        total_price, shipping_charge = 0, 0
        if cart_item:
            total_cart_price = models.AddToCart.objects.raw("SELECT id, qt_price, quantity, sum((quantity * qt_price)) as total_price  FROM add_to_cart WHERE session_key = %s ", [session_key])
            total_price = total_cart_price[0].total_price
            shipping_charge = 50 
            if cart_item:
                if (total_price > 1499):
                    shipping_charge = 0 
        grand_total = total_price + shipping_charge
    
        if request.is_ajax():
            status = request.POST.get('status')
            cart_item_id = request.POST.get('cart_item_id')
            if status == "plus":
                models.AddToCart.objects.filter(id = cart_item_id).update(
                    quantity = F('quantity')+1
                )
            else:
                models.AddToCart.objects.filter(id = cart_item_id).update(
                    quantity = F('quantity') - 1
                )
            data = "Cart Itam Change" 
            return JsonResponse(data, safe=False)
    else:
        context = {
            'count' : count,
        }
        return render(request,'publisher_app/empty_cart.html', context)
        
    context = {
        'cart_item': cart_item,
        'total_price': total_price,
        'shipping_charge': shipping_charge,
        'grand_total': grand_total,
        'count': count,
        'wishlist_count': models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
        'save_amount' : save_amount,
    }
    return render(request,'publisher_app/open_cart.html', context)


def loadCartItemByAjax(request): 
    if request.is_ajax():
        customerSessionId = request.GET.get('customerSessionId')
        cart_items_list = models.AddToCart.objects.filter(session_key = customerSessionId)
        total_sale_price, total_book_price = 0, 0
        for val in cart_items_list:
            total_sale_price += int(val.qt_price) * int(val.quantity)
            total_book_price += int(val.book_price) * int(val.quantity)
         
        results = [] 
        for value in  cart_items_list:  
            total_price = int(value.quantity) * int(value.qt_price) 
            place_json = {}
            place_json['card_id'] = value.id
            place_json['book_id'] = value.book_name.id
            place_json['sale_price'] = value.book_name.sale_price
            place_json['book_slug'] = value.book_name.slug
            place_json['book_name_bangla'] = value.book_name.book_name_bangla
            place_json['book_mrp'] = value.book_price
            place_json['sales_price'] = value.qt_price
            place_json['quantity'] = value.quantity
            place_json['total_price'] = total_price
            place_json['total_sale_price'] = str(total_sale_price)
            place_json['total_book_price'] = str(total_book_price)
            place_json['publisher_name'] = value.book_name.publisher.publisher_name_bangla
            place_json['book_image'] = value.book_name.book_image if value.book_name.book_image else "N/A"
         
            results.append(place_json)
        return JsonResponse(results, safe=False) 
     
def ajaxQuantityUpDown(request): 
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)
        
    session_key = request.session.get("abcd")  
    if request.is_ajax():
        status = request.GET.get('status')   
        customer_book_id = request.GET.get('book_id') 
         
        if status == "plus":
            models.AddToCart.objects.filter(book_name_id = customer_book_id, session_key = session_key).update(
                quantity = F('quantity')+1
            ) 
            data = "plus"    
            return JsonResponse(data, safe=False)
        else:
            models.AddToCart.objects.filter(book_name_id = customer_book_id, session_key = session_key).update(
                quantity = F('quantity')-1
            ) 
            data = "minus"    
            return JsonResponse(data, safe=False)

def deleteCartItemByAjax(request):
    if request.is_ajax():
        cart_id = request.GET.get('cart_id') 
        delete_item = models.AddToCart.objects.filter(id = cart_id)
        if delete_item:
            delete_item.delete() 
            data = "Success"
        return JsonResponse(data, safe=False) 


def delete_to_cart(request): 
    if request.is_ajax():
        cartItemId = request.GET.get('cartItemId') 
        models.AddToCart.objects.filter(id = cartItemId, session_key = request.session.get("abcd")).delete() 
        data = "Item Deleted Successful"
        return JsonResponse(data, safe=False)


def loadPublisherWiseBook(request):
    if request.is_ajax():
        author_list = int(request.GET.get('auth_id'))
        print("author_list:", author_list)
         
        # book_list_by_pub_id = models.BookList.objects.filter(publisher_id = publisher_id)
         
        # results = []  
        # for val in book_list_by_pub_id:
        #     print("val.book_name_english :", val.book_name_english)
        #     place_json = {}  
        #     place_json['book_name_bangla'] = val.book_name_english 
 
        #     results.append(place_json) 
        data = "success"
        return JsonResponse(data, safe=False)


 
def quick_login(request): 
    if request.is_ajax():
        userId = request.GET.get('userId')
        password = request.GET.get('password')

        login_data = models.CustomarAccount.objects.filter(mobile = userId, password = password, status = True )
        if login_data:
            request.session['userid'] = login_data[0].id
            request.session['usermobile'] = login_data[0].mobile
            request.session['customername'] = login_data[0].customer_name 
            request.session['customer_photo'] = str(login_data[0].profile_images)  
 
            data = "success"
            return JsonResponse(data, safe=False)
         
        else:
            data = "Failed"
            return JsonResponse(data, safe=False)

def user_logout(request): 
    request.session['userid'] = False  
    request.session['customer_photo'] = False  
    request.session['is_guest'] = "guest"

    return redirect('/customer/login/')
 
def checkout_order(request):   
    year = str(timezone.now().year) 
    sm_year = year[-2:]  
    customer_info = ""
    session_key = request.session.get("abcd") 
      
    if request.session.get('userid'):   
        customer_info = models.CustomarAccount.objects.filter(id = request.session.get('userid'), status = True).first()
    
    district = models.DistrictEntry.objects.filter(status = True)
    cart_list = models.AddToCart.objects.filter(session_key = session_key)
    checkout_item = models.AddToCart.objects.raw("SELECT id, book_name_id, quantity, qt_price, book_price, (quantity*qt_price) as total_price FROM add_to_cart WHERE session_key = %s", [session_key])
    subtotal_amount = models.AddToCart.objects.raw("SELECT id, quantity, qt_price, (quantity*qt_price) as total_price, sum((quantity*qt_price)) as subtotal FROM add_to_cart WHERE session_key = %s  GROUP BY session_key", [session_key])
    sutotalamount = int(subtotal_amount[0].subtotal)
      
    shipping_charge = 50
    if sutotalamount > 1499:
        shipping_charge = 0

    grand_total = sutotalamount + shipping_charge
 
    if request.method == "POST":
        postal_code_id = request.POST.get('postal_code') 
        get_id = models.SalesOrder.objects.last()
        if get_id:
            last_id = get_id.id
            last_prefix = int(last_id)+1  
            if len(str(last_prefix))<2:
                last_prefix = '0'+str(last_prefix) 
        else:
            last_prefix = '01'

        slo_no = str(sm_year)+str(last_prefix)  
        order_number   = slo_no 
        customer_id    = int(request.POST['customer_name'])
        del_per_name   =  request.POST['del_per_name'] 
        customer_mobile = request.POST.get('mobile_number')
        optional_number = request.POST.get('optional_number')
 
        customer_email  = request.POST.get('customer_email')
        password  = request.POST.get('password')
        total_amount    = sutotalamount 
        payment_method  = request.POST.get('payment_type')
        payment_number_b  = request.POST.get('accounts_number_b')
        pay_amount_b      = request.POST.get('pay_amount_b')
        payment_number_r  = request.POST.get('accounts_number_r')
        pay_amount_r      = request.POST.get('pay_amount_r')
        payment_number_n  = request.POST.get('accounts_number_n')
        pay_amount_n      = request.POST.get('pay_amount_n')
        shipping_address = request.POST.get('delivery_address')
        upozilla_id = request.POST.get('upozilla_name')
         
        payment_number = ""
        pay_amount = ""
        if payment_number_b and pay_amount_b:
            payment_number = payment_number_b
            pay_amount = pay_amount_b
        elif payment_number_r and pay_amount_r:
            payment_number = payment_number_r
            pay_amount = pay_amount_r
        elif payment_number_n and pay_amount_n:
            payment_number = payment_number_n
            pay_amount = pay_amount_n

        # today           = datetime.now()
        request.session['redirect_session'] = None 
        if not request.session.get('userid'):
            chk_customer = models.CustomarAccount.objects.filter(mobile = customer_mobile, status = True).first()
            if not chk_customer: 
                customer_id = models.CustomarAccount.objects.create(
                    customer_name = del_per_name, mobile = customer_mobile, email = customer_email,
                    password = customer_mobile, is_guest = 1
                ) 
                if customer_id:
                    request.session['userid'] = customer_id.id
                    request.session['usermobile'] = customer_id.mobile
                    request.session['customername'] = customer_id.customer_name 
  
                models.SalesOrder.objects.create(
                    order_number = order_number, customer_name_id = customer_id.id, 
                    delivery_per_name = del_per_name, customer_mobile = customer_mobile, customer_email = customer_email,  
                    shipping_address = shipping_address, optional_number = optional_number, district_id = request.POST.get('district_name'),
                    upozilla_id = upozilla_id, postal_code_id = request.POST.get('postal_code'),shipping_charge = shipping_charge, 
                    total_amount = total_amount, vat_amount = 0, discount_amount = 0, less_amount = 0, due_amount = 0, 
                    service_charge = 0, payment_method = payment_method,payment_status = 1, order_status = 1, session_key = session_key
                ) 
                for i in checkout_item:    
                    models.SalesDetails.objects.create(
                        order_number = order_number, book_name_id = int(i.book_name_id), sale_price = i.qt_price,
                        book_quantity = i.quantity, session_key = session_key 
                    ) 
                    models.AddToCart.objects.filter(session_key = session_key, book_name_id = i.book_name.id).delete()
                 
            else:  
                models.SalesOrder.objects.create(
                    order_number = order_number, customer_name_id = chk_customer.id, 
                    delivery_per_name = del_per_name, customer_mobile = customer_mobile, customer_email = customer_email, shipping_address = shipping_address,  
                    optional_number = optional_number, district_id = int(request.POST.get('district_name')), upozilla_id = upozilla_id, postal_code_id = int(request.POST.get('postal_code')),
                    total_amount = total_amount, vat_amount = 0, discount_amount = 0, less_amount = 0, due_amount = 0, shipping_charge = shipping_charge,  
                    service_charge = 0, payment_method = payment_method, payment_status = 1, order_status = 1, session_key = session_key
                ) 
                for i in checkout_item:   
                    models.SalesDetails.objects.create(
                        order_number = order_number, book_name_id = int(i.book_name_id), book_price = i.book_price, sale_price = i.qt_price, book_quantity = i.quantity,
                    ) 
                    models.AddToCart.objects.filter(session_key = session_key, book_name_id = i.book_name.id).delete()
                
                if chk_customer:
                    request.session['userid'] = chk_customer.id
                    request.session['usermobile'] = chk_customer.mobile
                    request.session['customername'] = chk_customer.customer_name 
 
        else: 
            exit_customer = models.CustomarAccount.objects.filter(id = int(request.session.get('userid'))).first()
            if exit_customer:
                request.session['userid'] = exit_customer.id
                request.session['usermobile'] = exit_customer.mobile
                request.session['customername'] = exit_customer.customer_name  

            models.SalesOrder.objects.create(
                order_number = order_number, customer_name_id = int(request.session.get('userid')),district_id = request.POST.get('district_name'),
                upozilla_id = upozilla_id, postal_code_id = request.POST.get('postal_code'),
                delivery_per_name = del_per_name, customer_mobile = customer_mobile, customer_email = customer_email, shipping_address = shipping_address, 
                optional_number = optional_number, total_amount = total_amount, vat_amount = 0, discount_amount = 0, less_amount = 0, due_amount = 0, 
                shipping_charge = shipping_charge, service_charge = 0, payment_method = payment_method, payment_status = 1, order_status = 1, session_key = session_key
            )  
            for i in checkout_item: 
                models.SalesDetails.objects.create(
                    order_number = order_number, book_name_id = int(i.book_name_id), book_price = i.book_price, sale_price = i.qt_price, book_quantity = i.quantity,
                ) 
                models.AddToCart.objects.filter(session_key = session_key, book_name_id = i.book_name.id).delete()
        request.session['redirect_session'] = order_number
        return redirect('/myorder/order-list/', order_number = order_number)   
        # context = {
        #     'order_number':order_number,
        #     'customer_info':customer_info, 
        # }  
        # return render(request, 'publisher_app/customer_panel/my_account.html', context)

    context = {
        'count' : models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
        'district' : district,
        'cart_list' : cart_list,
        'checkout_item' : checkout_item,
        'customer_info' : customer_info,
        'sutotalamount' : sutotalamount,
        'shipping_charge' : shipping_charge,
        'grand_total' : grand_total,
    }
    return render(request, 'publisher_app/checkout.html', context)


def checkout_order_now(request, id, qty):   
    year = str(timezone.now().year) 
    sm_year = year[-2:]  
    customer_info = ""
    session_key = request.session.get("abcd")  
    if request.session.get('userid'):   
        customer_info = models.CustomarAccount.objects.filter(id = request.session.get('userid'), status = True).first()
     
    district = models.DistrictEntry.objects.filter(status = True)
    checkout_item = models.BookList.objects.get(id = id)
    or_book_quantity = qty
    or_book_price = checkout_item.sale_price 
    sutotalamount = 0
    if checkout_item:
        sutotalamount = int(or_book_quantity) * int(or_book_price)
      
    shipping_charge = 50
    if sutotalamount > 1499:
        shipping_charge = 0

    grand_total = sutotalamount + shipping_charge
   
    if request.method == "POST": 
        get_id = models.SalesOrder.objects.last()
        if get_id:
            last_id = get_id.id
            last_prefix = int(last_id)+1  
            if len(str(last_prefix))<2:
                last_prefix = '0'+str(last_prefix) 
        else:
            last_prefix = '01'

        slo_no = str(sm_year)+str(last_prefix)  
        order_number   = slo_no 
        customer_id    = int(request.POST['customer_name'])
        del_per_name   =  request.POST['del_per_name'] 
        customer_mobile = request.POST.get('mobile_number')
        optional_number = request.POST.get('optional_number')
 
        customer_email  = request.POST.get('customer_email') 
        total_amount    = grand_total 
        payment_method  = request.POST.get('payment_type')
        payment_number_b  = request.POST.get('accounts_number_b')
        pay_amount_b      = request.POST.get('pay_amount_b')
        payment_number_r  = request.POST.get('accounts_number_r')
        pay_amount_r      = request.POST.get('pay_amount_r')
        payment_number_n  = request.POST.get('accounts_number_n')
        pay_amount_n      = request.POST.get('pay_amount_n')
        shipping_address = request.POST.get('delivery_address')
        upozilla_id = request.POST.get('upozilla_name')
         
        payment_number = ""
        pay_amount = ""
        if payment_number_b and pay_amount_b:
            payment_number = payment_number_b
            pay_amount = pay_amount_b
        elif payment_number_r and pay_amount_r:
            payment_number = payment_number_r
            pay_amount = pay_amount_r
        elif payment_number_n and pay_amount_n:
            payment_number = payment_number_n
            pay_amount = pay_amount_n

        # today           = datetime.now()
        request.session['redirect_session'] = None 
        if not request.session.get('userid'):
            chk_customer = models.CustomarAccount.objects.filter(mobile = customer_mobile, status = True).first()
            if not chk_customer: 
                customer_id = models.CustomarAccount.objects.create(
                    customer_name = del_per_name, mobile = customer_mobile, email = customer_email,
                    password = customer_mobile, is_guest = 1
                ) 
                if customer_id:
                    request.session['userid'] = customer_id.id
                    request.session['usermobile'] = customer_id.mobile
                    request.session['customername'] = customer_id.customer_name 
  
                sales_order_id = models.SalesOrder.objects.create(
                    order_number = order_number, customer_name_id = customer_id.id, 
                    delivery_per_name = del_per_name, customer_mobile = customer_mobile, customer_email = customer_email,  
                    shipping_address = shipping_address, optional_number = optional_number, district_id = request.POST.get('district_name'),
                    upozilla_id = upozilla_id, postal_code_id = request.POST.get('postal_code'),shipping_charge = shipping_charge, 
                    total_amount = total_amount, vat_amount = 0, discount_amount = 0, less_amount = 0, due_amount = 0, 
                    service_charge = 0, payment_method = payment_method,payment_status = 1, order_status = 1, session_key = session_key
                )     
                models.SalesDetails.objects.create(
                    order_number = order_number, book_name_id = int(checkout_item.id), sale_price = checkout_item.sale_price,
                    book_quantity = or_book_quantity, session_key = session_key 
                )
                models.SalesOrderPaymentDetails.objects.create(
                    sales_order_id = sales_order_id, order_number = order_number, payment_method = payment_method,
                    account_number = payment_number, payment_amount = pay_amount
                ) 
            else:  
                models.SalesOrder.objects.create(
                    order_number = order_number, customer_name_id = chk_customer.id, 
                    delivery_per_name = del_per_name, customer_mobile = customer_mobile, customer_email = customer_email, shipping_address = shipping_address,  
                    optional_number = optional_number, district_id = int(request.POST.get('district_name')), upozilla_id = upozilla_id, postal_code_id = int(request.POST.get('postal_code')),
                    total_amount = total_amount, vat_amount = 0, discount_amount = 0, less_amount = 0, due_amount = 0, shipping_charge = shipping_charge,  
                    service_charge = 0, payment_method = payment_method, payment_status = 1, order_status = 1, session_key = session_key
                )    
                models.SalesDetails.objects.create(
                    order_number = order_number, book_name_id = int(checkout_item.id), sale_price = checkout_item.sale_price,
                    book_quantity = or_book_quantity, session_key = session_key 
                )  
                if chk_customer:
                    request.session['userid'] = chk_customer.id
                    request.session['usermobile'] = chk_customer.mobile
                    request.session['customername'] = chk_customer.customer_name 
 
        else: 
            exit_customer = models.CustomarAccount.objects.filter(id = int(request.session.get('userid'))).first()
            if exit_customer:
                request.session['userid'] = exit_customer.id
                request.session['usermobile'] = exit_customer.mobile
                request.session['customername'] = exit_customer.customer_name  

            models.SalesOrder.objects.create(
                order_number = order_number, customer_name_id = int(request.session.get('userid')),district_id = request.POST.get('district_name'),
                upozilla_id = upozilla_id, postal_code_id = request.POST.get('postal_code'),
                delivery_per_name = del_per_name, customer_mobile = customer_mobile, customer_email = customer_email, shipping_address = shipping_address, 
                optional_number = optional_number, total_amount = total_amount, vat_amount = 0, discount_amount = 0, less_amount = 0, due_amount = 0, 
                shipping_charge = shipping_charge, service_charge = 0, payment_method = payment_method, payment_status = 1, order_status = 1, session_key = session_key
            )  
            models.SalesDetails.objects.create(
                order_number = order_number, book_name_id = int(checkout_item.id), sale_price = checkout_item.sale_price,
                book_quantity = or_book_quantity, session_key = session_key 
            )
        request.session['redirect_session'] = order_number
        return redirect('/myorder/order-list/', order_number = order_number)    
    
    else:
        context = {
            'count' : models.AddToCart.objects.filter(session_key = request.session["abcd"]).count(),
            'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
            'district' : district, 
            'checkout_item' : checkout_item,
            'customer_info' : customer_info,
            'sutotalamount' : sutotalamount,
            'shipping_charge' : shipping_charge,
            'grand_total' : grand_total,
        }  
        return render(request, 'publisher_app/order_now.html', context)
     

def customer_order_success(request):
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)

    order_number = request.POST.get('order_number')
    context = {
        'order_number':order_number,
        'count' : models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
    }
    return render(request,'publisher_app/order_success.html', context)


def bind_upozilla_wise_postoffice(request):
    upozilla_name   = int(request.GET.get('upozilla_name', None))
    upozilla_wise_post = models.PostOfficeInfo.objects.filter(upozilla_name_id = upozilla_name)
    
    context = {
        'upozilla_wise_post': upozilla_wise_post,
    }
    return render(request, 'publisher_app/bind_post_office.html', context)


def all_book_category_list(request):
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)

    context = {
        'count' : models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
    }

    return render(request,'publisher_app/all_book_category_list.html', context)


def all_book_writter_list(request):
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)

    context = {
        'count' : models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
    }

    return render(request,'publisher_app/all_book_writter_list.html', context)


def all_book_publisher_list(request):
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)

    context = {
        'count' : models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
    }

    return render(request,'publisher_app/all_book_publisher_list.html', context)



def bind_book_search(request):
    if request.is_ajax():
        src_data = request.GET['src_data'].strip() 
        src_data_txt = str("%")+src_data+str("%")
        
        book_list = models.BookList.objects.raw("""
            SELECT bk.id as book_id, bk.book_name_bangla, bk.book_name_english, wwb.book_name_id, wwb.writter_name_id, bw.id, bk.book_image, bk.slug as book_url, 
            bw.writter_name_bangla, bw.writter_name_english, bp.publisher_name_bangla, bp.publisher_name_english, bk.book_price, bk.sale_price, bk.discount as book_sale_discount FROM book_list bk 
            left join writter_wise_book wwb ON bk.id = wwb.book_name_id 
            left join book_publisher_list bp ON bk.publisher_id = bp.id
            LEFT JOIN book_writter_list bw ON wwb.writter_name_id = bw.id
            WHERE bk.status <> 0 and (bk.book_name_bangla like %s OR bk.book_name_english like %s OR bp.publisher_name_bangla like %s OR bp.publisher_name_english like %s OR bw.writter_name_bangla like %s OR bw.writter_name_english like %s ) GROUP BY wwb.book_name_id limit 15
        """,[src_data_txt, src_data_txt, src_data_txt, src_data_txt, src_data_txt, src_data_txt])
        
        results = [] 
 
        for data in book_list: 
            place_json = {
                'book_id':str(data.book_id),
                'book_url':str(data.book_url),
                'book_name_english':str(data.book_name_english),
                'book_name_bangla':str(data.book_name_bangla),
                'publisher_name_bangla':str(data.publisher_name_bangla),
                'publisher_name_english':str(data.publisher_name_english),
                'writter_name_bangla':str(data.writter_name_bangla),
                'writter_name_english':str(data.writter_name_english),
                'book_price':str(data.book_price),
                'sale_price':str(data.sale_price),
                'book_discount':str(data.book_sale_discount),
                'book_image':str(data.book_image),
            } 
            results.append(place_json) 
        return JsonResponse(results, safe=False)


def bind_writter_search(request):
    if request.is_ajax():
        src_data = request.GET['src_data']
        writter_list = models.BookWritter.objects.values('id', 'writter_name_bangla', 'writter_name_english', 'menu_url', 'writter_images').filter( Q(writter_name_bangla__icontains = src_data) | Q(writter_name_english__icontains = src_data) )
        if writter_list:
            return JsonResponse(list(writter_list), safe = False, content_type='application/json; charset=utf8')

        else:
            data = "Writter Not Found"
            return HttpResponse(data, content_type="application/json") 
    else:
        return HttpResponse("", content_type="application/json") 

def bind_category_search(request):
    if request.is_ajax():
        src_data = request.GET['src_data']
        category_list = models.BookCategory.objects.values('id', 'cat_name_bangla', 'cat_name_english', 'menu_url').filter( Q(cat_name_bangla__icontains = src_data) | Q(cat_name_english__icontains = src_data) )
        if category_list:
            return JsonResponse(list(category_list), safe = False, content_type='application/json; charset=utf8')
        else:
            data = "Category Not Found"
            return HttpResponse(data, content_type="application/json") 
    else:
        return HttpResponse("", content_type="application/json") 

def bind_publisher_search(request):
    if request.is_ajax():
        src_data = request.GET['src_data']
        publisher_list = models.Publisher.objects.values('id', 'publisher_name_bangla', 'publisher_name_english', 'menu_url').filter( Q(publisher_name_bangla__icontains = src_data) | Q(publisher_name_english__icontains = src_data) )
        if publisher_list:
            return JsonResponse(list(publisher_list), safe = False, content_type='application/json; charset=utf8')
        else:
            data = "Publisher Not Found"
            return HttpResponse(data, content_type="application/json") 
    else:
        return HttpResponse("", content_type="application/json") 
 

	
def ahsan_blog(request): 
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)
       
    blog_list = models.BlogMaster.objects.filter(status = True).order_by('-id') 
    category_list = models.BlogMaster.objects.raw("SELECT bm.id, bc.cat_name_bangla, bm.category_id,bc.id, bm.blog_title, bc.status, count(bm.category_id) as total_blog FROM blog_list bm LEFT JOIN book_category_list bc ON bm.category_id = bc.id GROUP BY category_id") 
     
    context = {
        'count' : models.AddToCart.objects.filter(session_key = request.session["abcd"]).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
        'blog_list':blog_list,
        'category_list':category_list, 
    }
    return render(request, 'publisher_app/blog.html', context)
	
def ahsan_blog_details(request, id, blog_url): 
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)

    if request.method=="GET":  
        get_blog = models.BlogMaster.objects.get(id = id)
        comments_list = models.BlogComment.objects.filter(blog_id = id)
        category_list = models.BlogMaster.objects.raw("SELECT bm.id, bc.cat_name_bangla, bm.category_id,bc.id, bm.blog_title, bc.status, count(bm.category_id) as total_blog FROM blog_list bm LEFT JOIN book_category_list bc ON bm.category_id = bc.id GROUP BY category_id") 

        context = {
            'count' : models.AddToCart.objects.filter(session_key = request.session["abcd"]).count(),
            'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
            'get_blog':get_blog, 
            'category_list':category_list,  
            'comments_list':comments_list,  
        }
        return render(request, 'publisher_app/blog_details.html', context)

    else:
        get_blog = models.BlogMaster.objects.get(id = id)
        comments_list = models.BlogComment.objects.filter(blog_id = id)
        category_list = models.BlogMaster.objects.raw("SELECT bm.id, bc.cat_name_bangla, bm.category_id,bc.id, bm.blog_title, bc.status, count(bm.category_id) as total_blog FROM blog_list bm LEFT JOIN book_category_list bc ON bm.category_id = bc.id GROUP BY category_id") 
 
        comments_text = request.POST.get('comments_text')
        user_name = request.POST.get('user_name')
        user_mobile = request.POST.get('user_mobile')
        user_email = request.POST.get('user_email')
        chk_comments = models.BlogComment.objects.filter(blog_id = id, user_mobile = user_mobile, user_email = user_email).first()
        if not chk_comments:
            comment_id = models.BlogComment.objects.create(
                blog_id = id, user_name = user_name, user_mobile = user_mobile, user_email = user_email,
                user_comments = comments_text
            ).id 
            if comment_id:
                models.BlogMaster.objects.filter(id = id).update( total_comments = F('total_comments')+1)
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                pass
        else:
            pass

        context = {
            'count' : models.AddToCart.objects.filter(session_key = request.session["abcd"]).count(),  
            'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
            'get_blog':get_blog, 
            'category_list':category_list, 
            'comments_list':comments_list, 
        }
        return render(request, 'publisher_app/blog_details.html', context)

	
def BlogPostViewByAjax(request): 
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)
  
    if request.is_ajax():
        blog_id = request.GET.get('blog_id')  
        models.BlogMaster.objects.filter(id = blog_id).update(total_view = F('total_view')+1) 
        data = "success"
        return JsonResponse(data, safe=False)
	
def CategoryWiseBlogList(request, category_id, menu_url): 
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)
  
    category_list = models.BlogMaster.objects.raw("SELECT bm.id, bc.cat_name_bangla, bm.category_id,bc.id, bm.blog_title, bc.status, count(bm.category_id) as total_blog FROM blog_list bm LEFT JOIN book_category_list bc ON bm.category_id = bc.id GROUP BY category_id") 
    blog_list = models.BlogMaster.objects.filter(category_id = category_id)
    category_name = blog_list[0].category

    context = {
        'blog_list':blog_list,
        'category_name':category_name,
        'category_list':category_list,
    } 
    return render(request, 'publisher_app/blog/category_wise_blog_lsit.html', context)

 
def author_pages(request, id, menu_url):  
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)

    session_key = request.session.get("abcd")
    # recent_book_list = models.AddToRecentView.objects.filter(session_key = request.session.get("abcd")).order_by('-id')

    cart_item = models.AddToCart.objects.filter(session_key = request.session.get("abcd"))
    total_price =  cart_item.aggregate(Sum('qt_price'))['qt_price__sum']
    author_info = models.BookWritter.objects.get(id = id)
    author_id = author_info.id
    book_lit = models.BookList.objects.raw("SELECT *, wl.book_name_id as wl_id FROM book_list bk LEFT JOIN writter_wise_book wwb ON bk.id = wwb.book_name_id LEFT JOIN translator_wise_book twb ON bk.id = twb.book_name_id LEFT JOIN add_to_wishlist wl ON wl.book_name_id = bk.id LEFT JOIN editor_wise_book ewb ON bk.id = ewb.book_name_id WHERE wwb.writter_name_id = %s or twb.translator_name_id = %s or ewb.editor_name_id = %s GROUP by wwb.book_name_id order by bk.id desc", [author_id, author_id, author_id])
    wish_list = models.AddToWishlist.objects.filter(session_key = request.session.get("abcd"))
    if request.is_ajax():
        book_name_id = request.GET.get('book_id')
        cart_items_list = models.AddToCart.objects.filter( book_name_id = book_name_id,session_key = request.session.get("abcd")).first()
        if not cart_items_list:
            models.AddToCart.objects.create(
                book_name_id = request.GET.get('book_id'),
                qt_price = request.GET.get('sale_price'),
                book_price = request.GET.get('book_price'),
                discount = request.GET.get('discount'),
                session_key = request.session.get("abcd")
            )
            data = "success"
            return JsonResponse(data, safe=False) 
        else:
            data = "Book Already Exsit"
            return JsonResponse(data, safe=False) 
         
    context = {
        'author_info':author_info,
        'book_lit':book_lit,
        'wish_list':wish_list,
        'author_info':author_info,
        'count' : models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
        'total_price' : total_price,
        # 'recent_book_list' : recent_book_list, 
    }
    return render(request, 'publisher_app/authors.html', context)

######## Category wise book list ####################
def category_book_list(request, id, menu_url): 
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)
 
    cat_info = models.BookCategory.objects.get(id = id) 
    today_date = datetime.date.today() 
    one_month_ago = today_date - datetime.timedelta(days=230)  
     
    # New Published book list
    cat_book_list = models.BookList.objects.raw('''
        SELECT *, wl.book_name_id as wl_id FROM book_list INNER JOIN category_wise_book cwb ON book_list.id = cwb.book_name_id 
        LEFT JOIN add_to_wishlist wl ON wl.book_name_id = book_list.id
        INNER JOIN book_category_list bc ON cwb.category_name_id=bc.id  INNER JOIN writter_wise_book wwb ON book_list.id  = wwb.book_name_id
        INNER JOIN book_writter_list au ON wwb.writter_name_id = au.id WHERE book_list.status = 1 and cwb.category_name_id = %s 
        and (book_list.add_date >= %s and book_list.add_date <= %s) GROUP by wwb.book_name_id order by book_list.id desc limit 12 ''', 
        [id, one_month_ago, today_date]
    )
     
    # Best sales book list 
    best_sales_book = models.BookList.objects.raw('''
        SELECT *, wl.book_name_id as wl_id FROM book_list INNER JOIN category_wise_book cwb ON book_list.id = cwb.book_name_id 
        LEFT JOIN add_to_wishlist wl ON wl.book_name_id = book_list.id
        INNER JOIN book_category_list bc ON cwb.category_name_id=bc.id  INNER JOIN writter_wise_book wwb ON book_list.id  = wwb.book_name_id
        INNER JOIN book_writter_list au ON wwb.writter_name_id = au.id WHERE book_list.status = 1 and cwb.category_name_id = %s
        and book_list.total_sale >= 0 GROUP by wwb.book_name_id order by book_list.total_sale desc limit 12 ''', [id])
     
     
    # Last Week Top Sales book list 
    last_week_top_sals = models.BookList.objects.raw('''
        SELECT *, wl.book_name_id as wl_id FROM book_list INNER JOIN category_wise_book cwb ON book_list.id = cwb.book_name_id 
        LEFT JOIN add_to_wishlist wl ON wl.book_name_id = book_list.id
        INNER JOIN book_category_list bc ON cwb.category_name_id=bc.id  INNER JOIN writter_wise_book wwb ON book_list.id  = wwb.book_name_id
        INNER JOIN book_writter_list au ON wwb.writter_name_id = au.id WHERE book_list.status = 1 and cwb.category_name_id = %s
        and book_list.total_sale >= 0 GROUP by wwb.book_name_id order by book_list.total_sale desc limit 12 ''', [id]) 
 
    wish_list = models.AddToWishlist.objects.filter(session_key = request.session.get("abcd"))
    if request.is_ajax():
        book_name_id = request.GET.get('book_id')
        cart_items_list = models.AddToCart.objects.filter( book_name_id = book_name_id,session_key = request.session.get("abcd")).first()
        if not cart_items_list:
            models.AddToCart.objects.create(
                book_name_id = request.GET.get('book_id'), qt_price = request.GET.get('sale_price'),
                book_price = request.GET.get('book_price'), discount = request.GET.get('discount'),
                session_key = request.session.get("abcd")
            )
            data = "success"
            return JsonResponse(data, safe=False) 
        else:
            data = "Book Already Exsit"
            return JsonResponse(data, safe=False) 


    page_number = request.GET.get('page')
    if request.method == "POST":
        btnvalue = request.POST.get('btnPage')
        page_number = btnvalue
    index_count = 0
    if page_number and int(page_number) > 1:
        index_count = 16 * (int(page_number)-1)

    paginator = Paginator(cat_book_list, 16)
    pagination = paginator.get_page(page_number)
    if page_number is None:
        page_number = 1
        
    cat_book_list =  cat_book_list[index_count:16 * int(page_number)] 
  
    context = {
        'cat_info': cat_info, 
        'wish_list': wish_list, 
        'cat_book_list': cat_book_list, 
        'best_sales_book': best_sales_book, 
        'last_week_top_sals': last_week_top_sals, 
        "index_count": index_count,
        "page_number": pagination, 
        "current_page_no": page_number,  
        'count' : models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
    }
    return render(request, 'publisher_app/category_book_list.html', context)

# category_wise_new_publication 
def category_wise_new_publication(request, id):
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)

    session_key = request.session.get("abcd") 
    cat_info = models.BookCategory.objects.get(id = id) 
    new_publication_book_list = ""
    today_date = datetime.date.today() 
    one_month_ago = today_date - datetime.timedelta(days=120)  
     
    # New Published book list
    new_publication_book_list = models.BookList.objects.raw('''
        SELECT *, wl.book_name_id as wl_id FROM book_list INNER JOIN category_wise_book cwb ON book_list.id = cwb.book_name_id 
        LEFT JOIN add_to_wishlist wl ON wl.book_name_id = book_list.id
        INNER JOIN book_category_list bc ON cwb.category_name_id=bc.id  INNER JOIN writter_wise_book wwb ON book_list.id  = wwb.book_name_id
        INNER JOIN book_writter_list au ON wwb.writter_name_id = au.id WHERE book_list.status = 1 and cwb.category_name_id = %s 
        and (book_list.add_date >= %s and book_list.add_date <= %s) GROUP by wwb.book_name_id order by book_list.id desc''', 
        [id, one_month_ago, today_date])
    
    wish_list = models.AddToWishlist.objects.filter(session_key = request.session.get("abcd"))

    if request.is_ajax():
        book_name_id = request.GET.get('book_id')
        cart_items_list = models.AddToCart.objects.filter( book_name_id = book_name_id,session_key = request.session.get("abcd")).first()
        if not cart_items_list:
            models.AddToCart.objects.create(
                book_name_id = request.GET.get('book_id'), qt_price = request.GET.get('sale_price'),
                book_price = request.GET.get('book_price'), discount = request.GET.get('discount'),
                session_key = request.session.get("abcd")
            )
            data = "success"
            return JsonResponse(data, safe=False) 
        else:
            data = "Book Already Exsit"
            return JsonResponse(data, safe=False) 


    page_number = request.GET.get('page')
    if request.method == "POST":
        btnvalue = request.POST.get('btnPage')
        page_number = btnvalue
    index_count = 0
    if page_number and int(page_number) > 1:
        index_count = 16 * (int(page_number)-1)

    paginator = Paginator(new_publication_book_list, 16)
    pagination = paginator.get_page(page_number)
    if page_number is None:
        page_number = 1
        
    new_publication_book_list =  new_publication_book_list[index_count:16 * int(page_number)] 
  
    context = {
        'cat_info': cat_info, 
        'wish_list': wish_list, 
        'new_publication_book_list': new_publication_book_list, 
        "index_count": index_count,
        "page_number": pagination, 
        "current_page_no": page_number,  
        'count' : models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
    }
    return render(request, 'publisher_app/new_publication_book_list.html', context)
 

# category_wise_best_saller_book_list 
def category_wise_best_saller_book_list(request, id):
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)

     
    cat_info = models.BookCategory.objects.get(id = id)   
  
    # Best Saller book list
    best_saller_book_list = models.BookList.objects.raw('''
        SELECT *, wl.book_name_id as wl_id FROM book_list INNER JOIN category_wise_book cwb ON book_list.id = cwb.book_name_id 
        LEFT JOIN add_to_wishlist wl ON wl.book_name_id = book_list.id
        INNER JOIN book_category_list bc ON cwb.category_name_id=bc.id  INNER JOIN writter_wise_book wwb ON book_list.id  = wwb.book_name_id
        INNER JOIN book_writter_list au ON wwb.writter_name_id = au.id WHERE book_list.status = 1 and cwb.category_name_id = %s 
        and book_list.total_sale >= 4  GROUP by wwb.book_name_id order by book_list.id desc''', [id])
    
    wish_list = models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")) 
    if request.is_ajax():
        book_name_id = request.GET.get('book_id')
        cart_items_list = models.AddToCart.objects.filter( book_name_id = book_name_id,session_key = request.session.get("abcd")).first()
        if not cart_items_list:
            models.AddToCart.objects.create(
                book_name_id = request.GET.get('book_id'), qt_price = request.GET.get('sale_price'),
                book_price = request.GET.get('book_price'), discount = request.GET.get('discount'),
                session_key = request.session.get("abcd")
            )
            data = "success"
            return JsonResponse(data, safe=False) 
        else:
            data = "Book Already Exsit"
            return JsonResponse(data, safe=False) 


    page_number = request.GET.get('page')
    if request.method == "POST":
        btnvalue = request.POST.get('btnPage')
        page_number = btnvalue
    index_count = 0
    if page_number and int(page_number) > 1:
        index_count = 16 * (int(page_number)-1)

    paginator = Paginator(best_saller_book_list, 16)
    pagination = paginator.get_page(page_number)
    if page_number is None:
        page_number = 1
        
    best_saller_book_list =  best_saller_book_list[index_count:16 * int(page_number)] 
  
    context = {
        'cat_info': cat_info,  
        'wish_list': wish_list,  
        'best_saller_book_list': best_saller_book_list,  
        "index_count": index_count,
        "page_number": pagination, 
        "current_page_no": page_number,  
        'count' : models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
    }
    return render(request, 'publisher_app/category_wise_best_saller_book_list.html', context)
 
  
# category_wise_last_week_best_writter_book 
def category_wise_last_week_best_writter_book(request, id):
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)
 
    cat_info = models.BookCategory.objects.get(id = id)    
    # Best Saller book list
    last_week_best_writter_book = models.BookList.objects.raw('''
        SELECT *, wl.book_name_id as wl_id FROM book_list INNER JOIN category_wise_book cwb ON book_list.id = cwb.book_name_id 
        LEFT JOIN add_to_wishlist wl ON wl.book_name_id = book_list.id 
        INNER JOIN book_category_list bc ON cwb.category_name_id=bc.id  INNER JOIN writter_wise_book wwb ON book_list.id  = wwb.book_name_id
        INNER JOIN book_writter_list au ON wwb.writter_name_id = au.id WHERE book_list.status = 1 and cwb.category_name_id = %s 
        and book_list.total_sale >= 4  GROUP by wwb.book_name_id order by book_list.id desc''', [id])

    wish_list = models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")) 
    if request.is_ajax():
        book_name_id = request.GET.get('book_id')
        cart_items_list = models.AddToCart.objects.filter( book_name_id = book_name_id,session_key = request.session.get("abcd")).first()
        if not cart_items_list:
            models.AddToCart.objects.create(
                book_name_id = request.GET.get('book_id'), qt_price = request.GET.get('sale_price'),
                book_price = request.GET.get('book_price'), discount = request.GET.get('discount'),
                session_key = request.session.get("abcd")
            )
            data = "success"
            return JsonResponse(data, safe=False) 
        else:
            data = "Book Already Exsit"
            return JsonResponse(data, safe=False) 


    page_number = request.GET.get('page')
    if request.method == "POST":
        btnvalue = request.POST.get('btnPage')
        page_number = btnvalue
    index_count = 0
    if page_number and int(page_number) > 1:
        index_count = 16 * (int(page_number)-1)

    paginator = Paginator(last_week_best_writter_book, 16)
    pagination = paginator.get_page(page_number)
    if page_number is None:
        page_number = 1
        
    last_week_best_writter_book =  last_week_best_writter_book[index_count:16 * int(page_number)] 
  
    context = {
        'cat_info': cat_info,  
        'wish_list': wish_list,  
        'last_week_best_writter_book': last_week_best_writter_book,  
        "index_count": index_count,
        "page_number": pagination, 
        "current_page_no": page_number,  
        'count' : models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
    }
    return render(request, 'publisher_app/last_week_best_writter_book.html', context)
 

def publisher_wise_page(request, id, menu_url ):
    
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)
    
    session_key = request.session.get("abcd") 
    publisher_info = models.Publisher.objects.get(id = id) 
    pub_book_list = models.BookList.objects.raw('''
        SELECT *, wl.book_name_id as wl_id FROM book_list INNER JOIN category_wise_book cwb ON book_list.id = cwb.book_name_id 
        LEFT JOIN add_to_wishlist wl ON wl.book_name_id = book_list.id
        INNER JOIN book_category_list bc ON cwb.category_name_id=bc.id  INNER JOIN writter_wise_book wwb ON book_list.id  = wwb.book_name_id
        INNER JOIN book_writter_list au ON wwb.writter_name_id = au.id WHERE book_list.status = 1 and book_list.publisher_id = %s GROUP by wwb.book_name_id order by book_list.id desc ''', [publisher_info.id]
    )
    wish_list = models.AddToWishlist.objects.filter(session_key = request.session.get("abcd"))
    if request.is_ajax():
        book_name_id = request.GET.get('book_id')
        cart_items_list = models.AddToCart.objects.filter( book_name_id = book_name_id,session_key = request.session.get("abcd")).first()
        if not cart_items_list:
            models.AddToCart.objects.create(
                book_name_id = request.GET.get('book_id'),
                qt_price = request.GET.get('sale_price'),
                book_price = request.GET.get('book_price'),
                discount = request.GET.get('discount'),
                session_key = request.session.get("abcd")
            )
            data = "success"
            return JsonResponse(data, safe=False) 
        else:
            data = "Book Already Added."
            return JsonResponse(data, safe=False) 
         

    context = {
        'publisher_info': publisher_info, 
        'wish_list': wish_list, 
        'pub_book_list': pub_book_list,
        'count' : models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
    }
    return render(request, 'publisher_app/publisher.html', context)

def customer_login(request): 
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)
 
    cart_item = models.AddToCart.objects.filter(session_key = request.session.get("abcd"))
    total_price =  cart_item.aggregate(Sum('qt_price'))['qt_price__sum']

    if request.is_ajax():
        your_mobile = request.GET.get('your_mobile')
        password = request.GET.get('password')
       
        data = models.CustomarAccount.objects.filter( mobile = your_mobile, password = password, is_guest = 1, status = True)
        if data:
            request.session['userid'] = data[0].id
            request.session['usermobile'] = data[0].mobile
            request.session['customername'] = data[0].customer_name
            request.session['user_type'] = "valid_user" 
            request.session['is_guest'] = "not_guest"
            request.session['customer_photo'] = str(data[0].profile_images)  
               
            data = "Login Successful"
            return JsonResponse(data, safe=False)
        else: 
            login_error = 'Login Failed!'
            return JsonResponse(login_error, safe=False)
    else:
        context = {
            'count' : models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count(),
            'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
            'total_price' : total_price, 
        }
        return render(request, 'publisher_app/customer_login.html', context)
 

############### Customer Registration #################
def customer_registration(request): 
    session_key = request.session.get("abcd")
    if request.is_ajax():
        mobile_number = request.GET.get('mobile_number')
        userEmail = request.GET.get('userEmail')
        user_full_name = request.GET.get('user_full_name')
        confirm_password = request.GET.get('confirm_password')

        chk_cust = models.CustomarAccount.objects.filter(mobile = mobile_number).first()
        if not chk_cust:  
            data = models.CustomarAccount.objects.create(
                customer_name = user_full_name, mobile = mobile_number, 
                email = userEmail, password = confirm_password, is_guest = 1
            )
            if data:  
                request.session['userid'] = data.id
                request.session['usermobile'] = data.mobile
                request.session['customername'] = data.customer_name
                request.session['user_type'] = "valid_user" 
                data = "Registration Successful"
                return JsonResponse(data, safe=False)
        else:  
            data = models.CustomarAccount.objects.filter(
                mobile = chk_cust.mobile, password = chk_cust.password, is_guest = 1
            ).first()
            if data:  
                request.session['userid'] = data.id
                request.session['usermobile'] = data.mobile
                request.session['customername'] = data.customer_name
                request.session['user_type'] = "valid_user" 
                data = "Registration Successful"
                return JsonResponse(data, safe=False) 
             
             
    context = {
        'count' : models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(), 
    } 
    return render(request, 'publisher_app/new_registration.html', context)
 

def user_logout(request): 
    request.session['userid'] = False  
    request.session['customer_photo'] = False  
    request.session['is_guest'] = "guest"

    return redirect('/customer/login/')




def login_for_review(request):  
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)
 
    if request.is_ajax():
        your_mobile = request.GET.get('your_mobile')
        password    = request.GET.get('password') 
        data = models.CustomarAccount.objects.filter( mobile = your_mobile, password = password, status = True)
        if data:
            request.session['userid'] = data[0].id
            request.session['usermobile'] = data[0].mobile
            request.session['customername'] = data[0].customer_name
            request.session['user_type'] = "valid_user" 
            request.session['is_guest'] = "not_guest"
            request.session['customer_photo'] = str(data[0].profile_images)  
               
            data = "Login Successful"
            return JsonResponse(data, safe=False)
        else: 
            login_error = 'Login Failed!'
            return JsonResponse(login_error, safe=False)
 
def client_review_message(request): 
    if request.is_ajax(): 
        review_book_id = int(request.GET.get('review_book_id'))
        review_message = request.GET.get('review_message')
        review_clients_id = int(request.GET.get('review_clients_id'))
        rating_point = request.GET.get('rating_point')
         
        chk_review = models.ClientReview.objects.filter( book_name_id = review_book_id, client_name_id = review_clients_id).first()
        if not chk_review:
            models.ClientReview.objects.create(
                book_name_id = review_book_id, client_name_id = review_clients_id,
                message = review_message, rating_count = rating_point, 
            )
            data = "success"
            return JsonResponse(data, safe=False) 
        else:
            models.ClientReview.objects.filter(book_name_id = review_book_id, client_name_id = review_clients_id).update(
                message = review_message, 
                rating_count = rating_point, 
            )
            data = "Exsit"
            return JsonResponse(data, safe=False) 


 

def wishList_cart_item(request):  
    mysession = random.random()
    if "abcd" not in request.session:
        request.session["abcd"] = str(mysession)

    session_key = request.session.get("abcd")
    print(session_key)
    wishlist_item = models.AddToWishlist.objects.raw("""
        SELECT bk.id, bk.book_name_bangla, bk.slug, bk.book_image, bk.book_price, bk.sale_price, IF(bk.cover_type = 1, 'পেপারব্যাক', 'হার্ডকভার') as cover_type,
        bp.publisher_name_bangla, bw.writter_name_bangla, bk.discount FROM add_to_wishlist wl 
        INNER JOIN book_list bk ON wl.book_name_id = bk.id INNER JOIN book_publisher_list bp ON bk.publisher_id = bp.id
        INNER JOIN writter_wise_book wwb ON wwb.book_name_id = bk.id INNER JOIN book_writter_list bw ON bw.id = wwb.writter_name_id
        where wl.session_key = %s and bk.status = 1 order by wl.id desc""", [session_key])
    
         
    if request.is_ajax():
        book_name_id = request.GET.get('book_id')
        cart_items_list = models.AddToCart.objects.filter( book_name_id = book_name_id,session_key = request.session.get("abcd")).first()
        if not cart_items_list:
            models.AddToCart.objects.create(
                book_name_id = request.GET.get('book_id'),
                qt_price = request.GET.get('sale_price'),
                book_price = request.GET.get('book_price'),
                discount = request.GET.get('discount'),
                session_key = request.session.get("abcd")
            )
            data = "success"
            return JsonResponse(data, safe=False) 
        else:
            data = "Book Already Added."
            return JsonResponse(data, safe=False) 

    context = {
        'wishlist_item': wishlist_item,
        'count' : models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(), 
    } 
    return render(request, 'publisher_app/wishlist_item.html', context)














































################ Dashboard Views ##########################


def admin_dashboard(request):  
    chk_permission   = check_user_permission(request,'/admin-dashboard')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action:

        return render(request, 'publisher_app/admin_dashboard/index.html')

    else:
        return redirect('/accessDeny')

        

def admin_login(request): 
    if request.method == "POST":
        data = models.UserRegistration.objects.filter(email = request.POST['user_email'], password = request.POST['user_pass']).first()
        if data:
            request.session['user_id'] = data.id
            request.session['user_name'] = data.full_name
            return redirect('/admin-dashboard')
        else:
            return redirect('/adminlogin') 
     
    return render(request, 'publisher_app/admin_dashboard/login.html')

def admin_logout(request):  
    request.session['user_id'] = False
    return redirect('/adminlogin')
 


def accessDeny(request):   
    return render(request, 'publisher_app/admin_dashboard/accessDeny.html')

@employeeLogin
def dashboard_active_book_list(request, id): 
    models.BookList.objects.filter(id = id).update(status = 0) 
    return redirect('/products/book-list/')

@employeeLogin
def dashboard_in_active_book_list(request, id):  
    models.BookList.objects.filter(id = id).update(status = 1) 
    return redirect('/products/book-list/')


@employeeLogin
def book_category_add(request): 
    chk_permission   = check_user_permission(request,'/book-category-entry/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 
        if request.method =="POST":
            menu_url4  = request.POST['category_name_english']
            loletterr = menu_url4.lower()
            usehipen = (loletterr.replace(" ", "-"))
            menu_url = usehipen
            models.BookCategory.objects.create(
                cat_name_bangla  = request.POST['category_name_bangla'],
                cat_name_english = request.POST['category_name_english'],
                menu_url = menu_url,
                Is_homepage     = True if request.POST.get('is_homepage') else False,
                Is_mainmenu     = True if request.POST.get('is_mainmenu') else False,
            )
            messages.success(request, "Category Entry Success.")
            return redirect("/book-category-list/")
        else:
            return render(request, 'publisher_app/admin_dashboard/settings/category_entry.html') 
    else:
        return redirect('/accessDeny')

        

@employeeLogin
def NewBookCategoryEntry(request): 
    chk_permission   = check_user_permission(request,'/products/add-new-book/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 
        if request.is_ajax():
            menu_url4  = request.GET.get('category_name_english')
            loletterr = menu_url4.lower()
            usehipen = (loletterr.replace(" ", "-"))
            menu_url = usehipen
            models.BookCategory.objects.create(
                cat_name_bangla  = request.GET.get('category_name_bangla'),
                cat_name_english = request.GET.get('category_name_english'),
                menu_url = menu_url
            )
            data = "success"
            return JsonResponse(data, safe=False)
        else:
            pass 
    else:
        return redirect('/accessDeny')

@employeeLogin
def NewBookWriterEntry(request): 
    chk_permission   = check_user_permission(request,'/products/add-new-book/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 
        if request.method =="POST":
            menu_url4 = request.POST['author_name_english']
            loletterr = menu_url4.lower()
            usehipen = (loletterr.replace(" ", "-"))
            menu_url = usehipen
            
            #  = "" 
            document_path = "" 
            if bool(request.FILES.get('author_photo', False)) == True:
                file = request.FILES['author_photo']   
                if not os.path.exists('publisher_app/static/publisher_app/media/images/writter/'):
                    os.mkdir('publisher_app/static/publisher_app/media/images/writter/')
 
                document_path = default_storage.save("writter/"+file.name, ContentFile(file.read()))
                if document_path:
                    document_path = str("writter/")+str(document_path).split("/")[-1]  
    
            models.BookWritter.objects.create(
                writter_name_bangla = request.POST['author_name_bangla'], writter_name_english = request.POST['author_name_english'],
                menu_url = menu_url, email = request.POST['author_email'], mobile = request.POST['author_mobile'], writter_images = document_path,
            )
            messages.success(request, "Book Writter Save Successful.")
            return redirect('/products/add-new-book/')
        else:
            pass 
    else:
        return redirect('/accessDeny')



@employeeLogin
def book_category_update(request, id): 
    chk_permission   = check_user_permission(request,'/book-category-entry/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 
        get_category = models.BookCategory.objects.get(id = id)
        if request.method =="POST":
            menu_url4  = request.POST['category_name_english']
            loletterr = menu_url4.lower()
            usehipen = (loletterr.replace(" ", "-"))
            menu_url = usehipen
            models.BookCategory.objects.filter(id=id).update(
                cat_name_bangla  = request.POST['category_name_bangla'],
                cat_name_english = request.POST['category_name_english'],
                detail = request.POST['category_details'],
                menu_url = menu_url, 
                Is_homepage     = True if request.POST.get('is_homepage') else False,
                Is_mainmenu     = True if request.POST.get('is_mainmenu') else False,
            )
            messages.success(request, "Category Update Successful")
            return redirect("/book-category-list/")
    
        context = {
            'get_category':get_category,
        }
        return render(request, 'publisher_app/admin_dashboard/settings/edit_category.html', context)
    else:
        return redirect('/accessDeny')

@employeeLogin
def book_category_list(request): 
    chk_permission   = check_user_permission(request,'/book-category-list/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 
    
        dash_cat_list = models.BookCategory.objects.filter(status = True).order_by('-id')
        context = {
            'dash_cat_list':dash_cat_list,
        }
        return render(request, 'publisher_app/admin_dashboard/settings/category_list.html', context)
    else:
        return redirect('/accessDeny')

@employeeLogin
def book_author_add(request): 
    chk_permission   = check_user_permission(request,'/book-category-list/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 
        if request.method=="POST":
            prod = models.BookWritter()
            menu_url4 = request.POST['author_name_english']
            loletterr = menu_url4.lower()
            usehipen = (loletterr.replace(" ", "-"))
            menu_url = usehipen
            
            #  = "" 
            document_path = "" 
            if bool(request.FILES.get('author_photo', False)) == True:
                file = request.FILES['author_photo']   
                if not os.path.exists('publisher_app/static/publisher_app/media/images/writter/'):
                    os.mkdir('publisher_app/static/publisher_app/media/images/writter/')
 
                document_path = default_storage.save("writter/"+file.name, ContentFile(file.read()))
                if document_path:
                    document_path = str("writter/")+str(document_path).split("/")[-1]  
     
            models.BookWritter.objects.create(
                writter_name_bangla = request.POST['author_name_bangla'], writter_name_english = request.POST['author_name_english'],
                menu_url = menu_url, email = request.POST['author_email'], mobile = request.POST['author_mobile'], qualification = request.POST['qualification'], 
                personal_details = request.POST['personal_details'], address = request.POST['author_address'], writter_images = document_path,
            )
 
            messages.success(request, "Book Writter Entry Save Successful.")
            return redirect('/book-author-list/')
        else:        
            return render(request, 'publisher_app/admin_dashboard/settings/author_entry.html')
    else:
        return redirect('/accessDeny')

  
@employeeLogin
def book_author_update(request, id):  
    chk_permission   = check_user_permission(request,'/book-category-list/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 
        get_auth = models.BookWritter.objects.get(id = id)
        if request.method=="POST":
            menu_url4 = request.POST['author_name_english']
            loletterr = menu_url4.lower()
            usehipen = (loletterr.replace(" ", "-"))
            menu_url = usehipen 

            writter_images = str(get_auth.writter_images) if get_auth.writter_images else ""
            if bool(request.FILES.get('writter_images', False)) == True: 
                if os.path.exists(str(writter_images)):
                    os.remove(str(get_auth.writter_images))

                file = request.FILES['writter_images']
                writter_images = "writter/"+file.name 
                if not os.path.exists('publisher_app/static/publisher_app/media/images/writter/'):
                    os.mkdir('publisher_app/static/publisher_app/media/images/writter/') 
                writter_images = default_storage.save("writter/"+file.name, ContentFile(file.read())) 
                if writter_images:
                    writter_images = str("writter/")+str(writter_images).split("/")[-1] 
            
            models.BookWritter.objects.filter(id=id).update(
                writter_name_bangla = request.POST['author_name_bangla'], writter_name_english = request.POST['author_name_english'],
                menu_url = menu_url, email = request.POST['author_email'], mobile = request.POST['author_mobile'], qualification = request.POST['qualification'], 
                personal_details = request.POST['personal_details'], address = request.POST['author_address'], writter_images = writter_images,
            )
            messages.success(request, "Book Writter Update Successful.")
            return redirect('/book-author-list/')

        context = {
            'get_auth':get_auth,
        }
        return render(request, 'publisher_app/admin_dashboard/settings/author_edit.html', context) 
    else:
        return redirect('/accessDeny')

@employeeLogin
def book_author_list(request):  
    chk_permission   = check_user_permission(request,'/book-category-list/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 
    
        dash_author_list = models.BookWritter.objects.filter(status = True).order_by('-id')
        context = {
            'dash_author_list':dash_author_list,
        }
        return render(request, 'publisher_app/admin_dashboard/settings/author_list.html', context)
    else:
        return redirect('/accessDeny')

@employeeLogin
def book_publisher_add(request):  
    chk_permission   = check_user_permission(request,'/book-category-list/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 

        if request.method=="POST":
            menu_url4 = request.POST['publisher_name_english']
            loletterr = menu_url4.lower()
            usehipen = (loletterr.replace(" ", "-"))
            menu_url = usehipen

            publisher_logo = "" 
            if bool(request.FILES.get('publisher_logo', False)) == True:
                file = request.FILES['publisher_logo']   
                if not os.path.exists('publisher_app/static/publisher_app/media/images/publisher_logo/'):
                    os.mkdir('publisher_app/static/publisher_app/media/images/publisher_logo/')

                document_path = default_storage.save("publisher_logo/"+file.name, ContentFile(file.read()))
                if document_path:
                    publisher_logo = str("publisher_logo/")+str(document_path).split("/")[-1] 
                      
            publisher_cover = "" 
            if bool(request.FILES.get('publisher_cover', False)) == True:
                file = request.FILES['publisher_cover']   
                if not os.path.exists('publisher_app/static/publisher_app/media/images/publisher_logo/'):
                    os.mkdir('publisher_app/static/publisher_app/media/images/publisher_logo/')

                cover_path = default_storage.save("publisher_logo/"+file.name, ContentFile(file.read()))
                if cover_path:
                    publisher_cover = str("publisher_logo/")+str(cover_path).split("/")[-1] 
    

            models.Publisher.objects.create(
                publisher_name_bangla = request.POST['publisher_name_bangla'], publisher_name_english = request.POST['publisher_name_english'],
                menu_url = menu_url, authorize_person = request.POST['authorize_person'], publisher_code = request.POST['publisher_code'], email = request.POST['publisher_email'], mobile = request.POST['publisher_mobile'],
                mobile_optional = request.POST['publisher_mobile2'], password = request.POST['password'],
                publisher_address = request.POST['publisher_address'], discount_persent = request.POST['discount_persent'],
                web_address = request.POST['web_address'], facebook_link = request.POST['facebook_link'], publisher_logo = publisher_logo, publisher_cover = publisher_cover,
            )
            messages.success(request, "Publisher Entry Save Successful.")
            return redirect('/book-publisher-list/') 

        else: 
            return render(request, 'publisher_app/admin_dashboard/settings/publisher_entry.html')
    else:
        return redirect('/accessDeny')

@employeeLogin
def book_publisher_list(request):  
    chk_permission   = check_user_permission(request,'/book-category-list/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 

        dash_pub_list = models.Publisher.objects.filter(status = True).order_by('-id') 
        context = {
            'dash_pub_list':dash_pub_list,
        } 
        return render(request, 'publisher_app/admin_dashboard/settings/publisher_list.html', context)
    else:
        return redirect('/accessDeny')

@employeeLogin
def book_publisher_update(request, id):  
    chk_permission   = check_user_permission(request,'/book-category-list/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 

        get_pub = models.Publisher.objects.get(id = id)
        if request.method=="POST":
            menu_url4 = request.POST['publisher_name_english']
            loletterr = menu_url4.lower()
            usehipen = (loletterr.replace(" ", "-"))
            menu_url = usehipen

            document_path = str(get_pub.publisher_logo) if get_pub.publisher_logo else ""
            if bool(request.FILES.get('publisher_logo', False)) == True:
                if os.path.exists(str(document_path)):
                    os.remove(str(get_pub.document_path))

                file = request.FILES['publisher_logo']
                document_path = "publisher_logo/"+file.name
                if not os.path.exists("publisher_logo/"):
                    os.mkdir("publisher_logo/")
                document_path = default_storage.save("publisher_logo/"+file.name, ContentFile(file.read()))
                if document_path:
                    document_path = str("publisher_logo/")+str(document_path).split("/")[-1]
            
            publisher_cover = str(get_pub.publisher_cover) if get_pub.publisher_cover else ""
            if bool(request.FILES.get('publisher_cover', False)) == True:
                if os.path.exists(str(publisher_cover)):
                    os.remove(str(get_pub.publisher_cover))

                file = request.FILES['publisher_cover']
                publisher_cover = "publisher_logo/"+file.name
                if not os.path.exists("publisher_logo/"):
                    os.mkdir("publisher_logo/")
                publisher_cover = default_storage.save("publisher_logo/"+file.name, ContentFile(file.read()))
                if publisher_cover:
                    publisher_cover = str("publisher_logo/")+str(publisher_cover).split("/")[-1]

            models.Publisher.objects.filter(id=id).update(
                publisher_name_bangla = request.POST['publisher_name_bangla'], publisher_name_english = request.POST['publisher_name_english'],
                menu_url = menu_url, authorize_person = request.POST['authorize_person'], publisher_code = request.POST['publisher_code'], 
                email = request.POST['publisher_email'], mobile = request.POST['publisher_mobile'],
                mobile_optional = request.POST['publisher_mobile2'], publisher_logo = document_path, publisher_cover = publisher_cover,
                publisher_address = request.POST['publisher_address'], discount_persent = request.POST['discount_persent'],
                web_address = request.POST['web_address'], facebook_link = request.POST['facebook_link'], sales_discount = request.POST['sales_discount'],
            ) 
            messages.success(request, "Publisher Update Successful.")
            return redirect('/book-publisher-list/')
        
        context = {
            'get_pub': get_pub,
        } 
        return render(request, 'publisher_app/admin_dashboard/settings/publisher_edit.html', context)
    else:
        return redirect('/accessDeny')


def add_new_book(request): 
    chk_permission   = check_user_permission(request,'/products/add-new-book/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 

        book_list  = models.BookList.objects.raw("SELECT bk.id, bk.book_price, bk.sale_price, bk.discount, bk.book_name_bangla, bwr.writter_name_bangla, pub.publisher_name_bangla FROM book_list bk left JOIN writter_wise_book wwb ON bk.id = wwb.book_name_id LEFT JOIN book_writter_list bwr ON wwb.writter_name_id = bwr.id LEFT JOIN book_publisher_list pub ON bk.publisher_id = pub.id")
        cate_list  = models.BookCategory.objects.filter(status = True)
        writter_list  = models.BookWritter.objects.filter(status = True)
        publisher  = models.Publisher.objects.filter(status = True)
        
        if request.method == "POST":
            book_idendity    = random.randint(1000, 1499149999)
            
            publisher_name = request.POST.get('publisher_name')
            book_name_bangla = request.POST.get('book_name_bangla')
            book_name_english = request.POST.get('book_name_english')
            book_origin = request.POST.get('book_origin')
            lowletter = book_name_english.lower()
            usehipen = (lowletter.replace(" ", "-"))
            book_name_wo_space = (lowletter.replace(" ", ""))
            book_url = usehipen

            book_language = request.POST.get('book_language')
            edition = request.POST.get('book_edition') 
            isbn_code = request.POST.get('isbn_code')
            cover_type = request.POST['cover_type'] 
            stock_info = request.POST['stock_info']
            quantity = 0
            number_of_page = request.POST.get('number_of_page')
            country = request.POST.get('country')
            book_price = request.POST.get('book_price')
            discount_offer = request.POST.get('discount_offer')
            purchase_discount = request.POST.get('purchase_discount')
            unit_price = request.POST.get('unit_price')
            sale_price = request.POST.get('sale_price')
            book_weight = request.POST.get('book_weight')
            book_details = request.POST.get('book_details')
 
            video_link_book_details = request.POST.get('video_link_book_details') 
            book_id_list = request.POST.getlist('book_name')  
            category_list = request.POST.getlist('category_name') 
            writter_lst = request.POST.getlist('writter_name') 
            translator_list = request.POST.getlist('book_translator') 
            editor_list = request.POST.getlist('editor_name') 
 
  
            if bool(request.FILES.get('book_image', False)) == True:
                file = request.FILES['book_image']   
                if not os.path.exists("book_image/"):
                    os.mkdir("book_image/")

                document_path = default_storage.save("book_image/"+file.name, ContentFile(file.read()))
                if document_path:
                    document_path = str("book_image/")+str(document_path).split("/")[-1] 
                 
            is_pre_image = 0
            preview_pdf = request.FILES.get('prev_file') 
            if preview_pdf:
                is_pre_image = 1
                if bool(request.FILES.get('prev_file', False)) == True:
                    file = request.FILES['prev_file']   
                    if not os.path.exists("preview_pdf/"):
                        os.mkdir("preview_pdf/")

                    pdf_path = default_storage.save("preview_pdf/"+file.name, ContentFile(file.read()))
                    if pdf_path:
                        pdf_path = str("preview_pdf/")+str(pdf_path).split("/")[-1]
                 
                     
            book_name_id = models.BookList.objects.create(
                publisher_id = publisher_name, is_pre_image = is_pre_image, slug = book_url,
                book_name_bangla = book_name_bangla, book_name_english = book_name_english, origin = book_origin, stock_info = stock_info, quantity = quantity,
                book_idendity = book_idendity, video_link = video_link_book_details,  purchase_discount = purchase_discount, unit_price = unit_price,
                country = country, number_of_page = number_of_page, cover_type = cover_type, ISBN = isbn_code, book_price = book_price, discount = discount_offer, 
                sale_price = sale_price, language = book_language, edition = edition, book_image = document_path, detail = book_details, weight = book_weight,
            ).id

            if preview_pdf:
                models.PreviewPdfFile.objects.create(book_name_id = book_name_id, pdf_file = pdf_path )
 
            for bk in book_id_list: 
                models.BookPackageDetails.objects.create(
                    package_name = book_name_bangla,
                    booklist_master_id = book_name_id, book_name_id = int(bk),
                    package_price = sale_price, package_discount = discount_offer
                )
            
            for cat in category_list: 
                models.CategoryWiseBook.objects.create(book_name_id = book_name_id, category_name_id = int(cat))
            
            for wri in writter_lst: 
                models.WritterWiseBook.objects.create(book_name_id = book_name_id, writter_name_id = int(wri))
            
            for tra in translator_list:
                models.TranslatorWiseBook.objects.create(book_name_id = book_name_id, translator_name_id = int(tra))

            for edit in editor_list:
                models.EditorWiseBook.objects.create(book_name_id = book_name_id, editor_name_id = int(edit))
  
            messages.success(request, "Book Entry Success.")
            return redirect("/products/book-list/")

        context = {
            'cate_list':cate_list,
            'writter_list':writter_list,
            'publisher':publisher,
            'book_list':book_list,
        }
        return render(request, 'publisher_app/admin_dashboard/products/add_new_book.html', context) 

    else:
        return redirect('/accessDeny')


def bookWisePreviewImageClear(request): 
    if request.is_ajax():
        book_id = request.GET.get('book_id')  
        get_pre_img = models.PreviewImages.objects.filter(book_name_id = book_id)
        for data in get_pre_img: 
            if data.images: 
                data.images.delete() 
        get_pre_img.delete()
        models.BookList.objects.filter(id = book_id).update(is_pre_image = 0) 
        data = "success"
        return JsonResponse(data, safe=False)

@employeeLogin
def book_list(request):  
    chk_permission   = check_user_permission(request,'/products/book-list/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 
        if request.method == "GET":
            book_list_total = models.BookList.objects.raw('''
                SELECT * FROM book_list bk LEFT JOIN category_wise_book bwc ON bk.id = bwc.book_name_id LEFT JOIN book_category_list bc ON bwc.category_name_id = bc.id 
                LEFT JOIN writter_wise_book wwb ON bk.id = wwb.book_name_id LEFT JOIN book_writter_list bw ON wwb.writter_name_id = bw.id
                LEFT JOIN book_publisher_list pub ON bk.publisher_id = pub.id GROUP BY bwc.book_name_id ORDER BY bk.id desc
            ''')
            page_number = request.GET.get('page')
            if request.method == "POST":
                btnvalue = request.POST.get('btnPage')
                page_number = btnvalue
            index_count = 0
            if page_number and int(page_number) > 1:
                index_count = 21 * (int(page_number)-1)

            paginator = Paginator(book_list_total, 21)
            pagination = paginator.get_page(page_number)
            if page_number is None:
                page_number = 1
                
            book_list =  book_list_total[index_count:21 * int(page_number)] 
        
            context = { 
                'book_list':book_list, 
                'total_book':len(list(book_list_total)),
                "index_count": index_count,
                "page_number": pagination, 
                "current_page_no": page_number,  
            }
            return render(request, 'publisher_app/admin_dashboard/products/book_list.html', context)
        
        else:   
            book_txt = request.POST.get("book_content_search").strip() 
            src_data_txt = str("%")+book_txt+str("%")
           
            book_list_total = models.BookList.objects.raw('''
                SELECT * FROM book_list bk LEFT JOIN category_wise_book bwc ON bk.id = bwc.book_name_id 
                LEFT JOIN book_category_list bc ON bwc.category_name_id = bc.id LEFT JOIN writter_wise_book wwb ON bk.id = wwb.book_name_id
                LEFT JOIN book_writter_list bw ON wwb.writter_name_id = bw.id LEFT JOIN book_publisher_list pub ON bk.publisher_id = pub.id
                where(bk.id LIKE %s OR bk.origin LIKE %s OR bk.book_price LIKE %s OR bk.sale_price LIKE %s OR bk.book_name_bangla LIKE %s OR bk.book_name_english LIKE %s OR bc.cat_name_bangla LIKE %s 
                OR bw.writter_name_bangla LIKE %s OR bw.writter_name_english LIKE %s OR pub.publisher_name_bangla LIKE %s 
                OR pub.publisher_name_english LIKE %s) GROUP BY bwc.book_name_id ORDER BY bk.id desc
            ''', [src_data_txt, src_data_txt, src_data_txt, src_data_txt, src_data_txt, src_data_txt, src_data_txt, src_data_txt, src_data_txt, src_data_txt, src_data_txt])
              
            to_entry = models.BookList.objects.raw("SELECT id, COUNT(id) as total_entry FROM `book_list`") 
            
            page_number = request.GET.get('page')
            if request.method == "POST":
                btnvalue = request.POST.get('btnPage')
                page_number = btnvalue
            index_count = 0
            if page_number and int(page_number) > 1:
                index_count = 21 * (int(page_number)-1)

            paginator = Paginator(book_list_total, 21)
            pagination = paginator.get_page(page_number)
            if page_number is None:
                page_number = 1
                
            book_list =  book_list_total[index_count:21 * int(page_number)]  

            context = { 
                'book_list':book_list, 
                'total_book':len(book_list_total),
                "index_count": index_count,
                'book_txt':book_txt,
                "page_number": pagination, 
                "current_page_no": page_number,     
            }
            return render(request, 'publisher_app/admin_dashboard/products/book_list.html', context)

    else:
        return redirect('/accessDeny')

 
@employeeLogin
def dashboard_update_book_item(request, id):
    chk_permission   = check_user_permission(request,'/products/add-new-book/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action:

        get_book = models.BookList.objects.get(id = id) 
        preview_file = models.PreviewPdfFile.objects.filter(book_name_id = id).first()
        cate_list  = models.BookCategory.objects.filter(status = True)
        book_wise_cate    = models.CategoryWiseBook.objects.filter(book_name_id = id)
        
        book_list  = models.BookList.objects.raw("SELECT bk.id, bk.book_price, bk.sale_price, bk.discount, bk.book_name_bangla, bwr.writter_name_bangla, pub.publisher_name_bangla FROM `book_list` bk left JOIN writter_wise_book wwb ON bk.id = wwb.book_name_id LEFT JOIN book_writter_list bwr ON wwb.writter_name_id = bwr.id LEFT JOIN book_publisher_list pub ON bk.publisher_id = pub.id")
        package_book_list  = models.BookPackageDetails.objects.raw("SELECT * FROM `book_package_list` WHERE booklist_master_id = %s",[id])
        writter_list      = models.BookWritter.objects.filter(status = True)
        book_wise_writ    = models.WritterWiseBook.objects.filter(book_name_id = id)
        book_wise_trans   = models.TranslatorWiseBook.objects.filter(book_name_id = id)
        book_wise_editor  = models.EditorWiseBook.objects.filter(book_name_id = id)
        publisher         = models.Publisher.objects.filter(status = True)
    
        if request.method=="POST":  
            publisher_name = int(request.POST.get('publisher_name'))
            book_name_bangla = request.POST.get('book_name_bangla')
            book_name_english = request.POST.get('book_name_english')
            book_origin = request.POST.get('book_origin')
            
            lowletter = book_name_english.lower()
            usehipen = (lowletter.replace(" ", "-"))
            book_name_wo_space = (lowletter.replace(" ", ""))
            book_url = usehipen

            book_language = request.POST.get('book_language')
            edition = request.POST.get('edition')
            isbn_code = request.POST.get('isbn_code')
            cover_type = request.POST.get('book_cover_type')
            number_of_page = request.POST.get('number_of_page')
            country = request.POST.get('country') 
            book_price = request.POST.get('book_price')
            discount_offer = request.POST.get('discount_offer') 
            sale_price = request.POST.get('sale_price')
            purchase_discount = request.POST.get('purchase_discount')
            unit_price = request.POST.get('unit_price')
            stock_info = request.POST.get('stock_info') 
            coupon_price = request.POST.get('coupon_price')
            
            book_weight = request.POST.get('book_weight') 
            book_details = request.POST.get('book_details')
            video_link_book_details = request.POST.get('video_link_book_details')

            category_list = request.POST.getlist('categoryName') 
            writter_id = request.POST.getlist('writter_name')  
            translator_id = request.POST.getlist('translator_name')  
            editor_name = request.POST.getlist('editor_name')  
 
            preview_pdf = request.FILES.get('prev_file')  
            
            if preview_pdf:
                is_pre_image = 1 
            else:
                if preview_file:
                    is_pre_image = 1
                else:
                    is_pre_image = 0   
            
            document_path = str(get_book.book_image) if get_book.book_image else "" 
            if bool(request.FILES.get('book_image', False)) == True:
                if os.path.exists(str(document_path)):
                    os.remove(str(get_book.document_path))

                file = request.FILES['book_image']
                document_path = "book_image/"+file.name
                print("This is check file Name : ", file.name)
                if not os.path.exists("book_image/"):
                    os.mkdir("book_image/")
                document_path = default_storage.save("book_image/"+file.name, ContentFile(file.read()))
                if document_path:
                    document_path = str("book_image/")+str(document_path).split("/")[-1]
 
            if preview_pdf: 
                if preview_file: 
                    pdf_path = str(preview_file.pdf_file) if preview_file.pdf_file else "" 
                if bool(request.FILES.get('prev_file', False)) == True:
                    file = request.FILES['prev_file']   
                    if not os.path.exists("preview_pdf/"):
                        os.mkdir("preview_pdf/")

                    pdf_path = default_storage.save("preview_pdf/"+file.name, ContentFile(file.read()))
                    if pdf_path:
                        pdf_path = str("preview_pdf/")+str(pdf_path).split("/")[-1]

                    models.PreviewPdfFile.objects.create(book_name_id = id, pdf_file = pdf_path )

                # Code for Thumbnail Image Convert 
                # if not os.path.exists('publisher_app/static/publisher_app/media/images/thumbnail/'):
                #     os.mkdir('publisher_app/static/publisher_app/media/images/thumbnail/')
                # size = 130,190
                # im = Image.open(file)
                # im.thumbnail(size, Image.ANTIALIAS)
                # im.save(settings.MEDIA_ROOT+"images/thumbnail/"+str(book_name_wo_space)+str("_")+str(file), format="JPEG", quality=80)
                # thumbnail = "images/thumbnail/"+str(file)
                # if thumbnail:
                #     thumbnail = str("images/thumbnail/")+str(book_name_wo_space)+str("_")+str(thumbnail).split("/")[-1]
            
            models.BookList.objects.filter(id=id).update(
                publisher_id = publisher_name, book_name_bangla = book_name_bangla, book_name_english = book_name_english, 
                slug = book_url,video_link = video_link_book_details, country = country, is_pre_image = is_pre_image, origin = book_origin,
                number_of_page = number_of_page, cover_type = cover_type, ISBN = isbn_code, stock_info = stock_info,
                book_price = book_price, discount = discount_offer, sale_price = sale_price, language = book_language, 
                edition = edition, book_image = document_path, detail = book_details, weight = book_weight,
                coupon_price = coupon_price, purchase_discount = purchase_discount, unit_price = unit_price,
            )  
            models.WritterWiseBook.objects.filter(book_name_id =  id).delete()
            for wri in writter_id:   
                models.WritterWiseBook.objects.create(book_name_id = get_book.id, writter_name_id = int(wri),)
            
            models.CategoryWiseBook.objects.filter(book_name_id =  id).delete()
            for cat in category_list:   
                models.CategoryWiseBook.objects.create(book_name_id = get_book.id, category_name_id = int(cat),)
                
            models.TranslatorWiseBook.objects.filter(book_name_id = id).delete()
            for ts in translator_id:   
                models.TranslatorWiseBook.objects.create(book_name_id = get_book.id, translator_name_id = int(ts),)     
            
            models.EditorWiseBook.objects.filter(book_name_id =  id).delete()
            for ed in editor_name:   
                models.EditorWiseBook.objects.create(book_name_id = get_book.id, editor_name_id = int(ed),)
   
            return redirect('/products/book-list/')
        
        context = {
            'get_book':get_book,
            'cate_list':cate_list,
            'writter_list':writter_list,
            'publisher':publisher,
            'book_wise_cate':book_wise_cate,
            'book_wise_writ':book_wise_writ,
            'book_wise_trans':book_wise_trans,
            'book_wise_editor':book_wise_editor,
            'book_list':book_list,
            'package_book_list':package_book_list,
            'preview_file':preview_file,
        }
        return render(request, 'publisher_app/admin_dashboard/products/update_book_list.html', context)

    else:
        return redirect('/accessDeny')


@employeeLogin
def settings_dashboard(request):
    chk_permission   = check_user_permission(request,'/settings-dashboard/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 
 

        return render(request, 'publisher_app/admin_dashboard/settings/settings_dashboard.html')
    else:
        return redirect('/accessDeny')

@employeeLogin
def user_access_control(request):
    chk_permission   = check_user_permission(request,'/user-access-control/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 
        menu_list = models.MenuList.objects.filter(status = True)
 
        context = {
            'menu_list':menu_list,
        } 
        return render(request, 'publisher_app/admin_dashboard/settings/user_access_control.html', context)
    else:
        return redirect('/accessDeny')



@employeeLogin
def dashboard_district_add(request): 
    chk_permission   = check_user_permission(request,'/settings/district-add/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 

        # district_list = requests.get("https://www.durbarshop.com/api/districtList?accessToken=ib71caf71ca9c263d1bec89b2850120f1").json()
        # count = 1

        # for data in district_list["results"]: 
        #     print(data["id"]) 
        #     count+=1
 
        if request.method =="POST":
            models.DistrictEntry.objects.create(
                district_name_bangla = request.POST['district_name_bangla'],
                district_name_english = request.POST['district_name_english'],
                status = True if request.POST.get('checkbox_status') else False,
            )
            messages.success(request, "District Add Successful.")
            return redirect('/settings/district-list/')
        else:    
            return render(request, 'publisher_app/admin_dashboard/settings/district_add.html')
    else:
        return redirect('/accessDeny')

@employeeLogin
def dashboard_district_list(request): 
    chk_permission   = check_user_permission(request,'/settings/district-list/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 

        distr_list = models.DistrictEntry.objects.all().order_by('ordering')
        context = {
            'distr_list':distr_list,
        }
        return render(request, 'publisher_app/admin_dashboard/settings/district_list.html', context)
    else:
        return redirect('/accessDeny')


@employeeLogin
def dashboard_upozilla_add(request):
    chk_permission   = check_user_permission(request,'/settings/upozilla-add/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 
        
        show_dist_list = models.DistrictEntry.objects.all()
        if request.method =="POST":
            models.UpozillaEntry.objects.create(
                district_name_id      = int(request.POST['district_name']),
                upozilla_name_bangla  = request.POST['upozilla_name_bangla'],
                upozilla_name_english = request.POST['upozilla_name_english'],
                status = True if request.POST.get('checkbox_status') else False, 
            )
            messages.success(request, "Upozilla Add Successful")
            return redirect('/settings/upozilla-list/')
            
        context = {
            'show_dist_list':show_dist_list,
        }
        return render(request, 'publisher_app/admin_dashboard/settings/upozilla_add.html', context)
    else:
        return redirect('/accessDeny')

@employeeLogin
def dashboard_upozilla_list(request):
    chk_permission   = check_user_permission(request,'/settings/upozilla-list/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action:  

        upozi_list = models.UpozillaEntry.objects.all().order_by('-id')
        context = {
            'upozi_list':upozi_list,
        }
        return render(request, 'publisher_app/admin_dashboard/settings/upozilla_list.html', context)
    else:
        return redirect('/accessDeny')

@employeeLogin
def dashboard_post_office_add(request): 
    chk_permission   = check_user_permission(request,'/settings/post-office-add/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 

        show_dist_list = models.DistrictEntry.objects.all()
        show_upozi_list = models.UpozillaEntry.objects.all()

        if request.method =="POST":
            upozilla_id =  int(request.POST['upozilla_id'])
            post_office_bangla = request.POST['post_office_name_bangla']
            post_office_english = request.POST['post_office_name_english']
            post_code   = request.POST['post_office_code'] 

            models.PostOfficeInfo.objects.create(
                upozilla_name_id = upozilla_id,
                post_office_bangla = post_office_bangla,
                post_office_english = post_office_english,
                post_code = post_code, 
            )
            messages.success(request, "Post Code Add Successful.")
            return redirect('/settings/post-office-add/')

        context = {
            'show_dist_list':show_dist_list,
            'show_upozi_list':show_upozi_list,
        }
        return render(request, 'publisher_app/admin_dashboard/settings/post_office_add.html', context)
    else:
        return redirect('/accessDeny')
    
@employeeLogin
def dashboard_post_office_list(request):
    chk_permission   = check_user_permission(request,'/settings/post-office-list/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 

        post_office_list = models.PostOfficeInfo.objects.filter(status = True).order_by('-id')
        context = {
            'post_office_list': post_office_list,
        }
        return render(request, 'publisher_app/admin_dashboard/settings/post_office_list.html', context)
    else:
        return redirect('/accessDeny')

    
def dashboard_bind_district_wise_upozilla(request): 
    district_name   = int(request.GET.get('district_name', None))  
    district_wise_upozilla = models.UpozillaEntry.objects.filter(district_name_id = district_name)  
    context = {
        'district_wise_upozilla': district_wise_upozilla,  
    }
    return render(request, 'publisher_app/admin_dashboard/settings/bind_district_wise_upo.html', context)

     
@employeeLogin
def menu_add(request):
    chk_permission   = check_user_permission(request,'/settings/menu-add/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 

        if request.method == "POST":
            menu_name = request.POST['menu_name']
            menu_url = request.POST['menu_url']
            menu_module = request.POST['menu_module']

            models.MenuList.objects.create(
                menu_name = menu_name, menu_url = menu_url, module_name = menu_module, created_by_id = int(request.session['user_id'])
            )
            messages.success(request, "Menu Add Successful.")
            return redirect('/settings/menu-list/')

        return render(request, 'publisher_app/admin_dashboard/settings/menu_add.html')
    else:
        return redirect('/accessDeny')
     
@employeeLogin
def menu_list(request):
    chk_permission   = check_user_permission(request,'/settings/menu-list/')
    if chk_permission and chk_permission.view_action and chk_permission.insert_action: 

        menu_list = models.MenuList.objects.filter(status = True)
        context = {
            'menu_list': menu_list,
        }
        return render(request, 'publisher_app/admin_dashboard/settings/menu_list.html', context)
    else:
        return redirect('/accessDeny')

def bookListApi(request):
    if request.GET.get("accessToken") == "ib71caf71ca9c263d1bec89b2850120f1": 
        if request.method == "GET":   
            book_list = models.BookList.objects.filter(status=1)            
            if book_list:  
                results = [] 
                for data in book_list: 
                    data = {
                        "id": int(data.id),   
                        "book_name_english": str(data.book_name_english), 
                        "book_price": str(data.book_price), 
                        "sale_price": str(data.sale_price),  
                        "publisher_name": str(data.publisher.publisher_name_english),   
                        "status": str(data.status),   
                    } 
                    results.append(data) 
            return JsonResponse({"results": results}, safe=False, status=200) 
        else:
            return JsonResponse({"message": "Method not allowed"}, safe=False, status=400) 
 