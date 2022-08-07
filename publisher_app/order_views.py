from unicodedata import category
from django.shortcuts import render, redirect
#from grpc import Status
from . import models
from publisher_app.utils import render_to_pdf
from django.http import HttpResponse
from django.http import HttpRequest   
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
from django.utils import timezone
from datetime import datetime, timedelta, tzinfo, date  
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
# import urllib.parse
from urllib.parse import urlparse 
from publisher_app.decorators import employeeLogin
val = None
value = None
import datetime
import time 
import random
from django.views.decorators.csrf import csrf_exempt
import io, os, xlsxwriter
import pandas as pd

@employeeLogin
def dashboard_bind_district_wise_upozilla(request): 
    district_name   = int(request.GET.get('district_name', None))  
    district_wise_upozilla = models.UpozillaEntry.objects.filter(district_name_id = district_name) 
    get_upozilla_id = val() 
    context = {
        'district_wise_upozilla': district_wise_upozilla, 
        'get_upozilla_id': get_upozilla_id, 
    }
    return render(request, 'publisher_app/admin_dashboard/bind_district_wise_upo.html', context)

@employeeLogin
def dashboard_bind_upozilla_wise_post(request): 
    upozilla_name   = int(request.GET.get('upozilla_name', None))    
    upozila_wise_post = models.PostOfficeInfo.objects.filter(upozilla_name_id = upozilla_name)
    postal_code_id = value()  
    context = {
        'upozila_wise_post': upozila_wise_post, 
        'postal_code_id': postal_code_id, 
    }
    return render(request, 'publisher_app/admin_dashboard/bind_post_office.html', context)
 

@employeeLogin
def all_order_dashboard(request, *args, **kwargs): 
    if request.method == "GET": 
        custom_id = request.session.get('user_id')  
        all_order = models.SalesOrder.objects.filter(status = True).order_by('-order_number')
            
        context = {
            'all_order':all_order, 
        }
        return render(request, 'publisher_app/admin_dashboard/orders/all_order.html', context)
    else: 
        search_txt = str(request.POST.get('SearchOrder')).strip() 
        all_order = models.SalesOrder.objects.raw("select * from sales_order where (delivery_per_name like %s OR order_number = %s OR customer_mobile = %s OR optional_number = %s) and status = 1", [search_txt, search_txt, search_txt, search_txt])
          
        context = {
            'all_order':all_order, 
            'search_txt':search_txt,  
        }
        return render(request, 'publisher_app/admin_dashboard/orders/all_order.html', context)
    
@employeeLogin
def pending_order_list(request):  
    if request.method == "GET":    
        pending_order = models.SalesOrder.objects.filter(order_status = 1, status = True).order_by('-order_number')
            
        context = {
            'pending_order':pending_order, 
        }
        return render(request, 'publisher_app/admin_dashboard/orders/pending_order.html', context)
    else: 
        search_txt = str(request.POST.get('SearchOrder')).strip() 
        pending_order = models.SalesOrder.objects.raw("select * from sales_order where order_status = 1 and (delivery_per_name like %s OR order_number = %s OR customer_mobile = %s OR optional_number = %s) and status = 1", [search_txt, search_txt, search_txt, search_txt])
          
        context = {
            'pending_order':pending_order, 
            'search_txt':search_txt,  
        } 
        return render(request, 'publisher_app/admin_dashboard/orders/pending_order.html', context)

@employeeLogin
def dashboard_confirm_order_list(request):  
    if request.method == "GET":    
        confirm_order = models.SalesOrder.objects.filter(order_status = 2, status = True).order_by('-order_number')
            
        context = {
            'confirm_order':confirm_order, 
        }
        return render(request, 'publisher_app/admin_dashboard/orders/confirm_order.html', context)
    else: 
        search_txt = str(request.POST.get('SearchOrder')).strip() 
        confirm_order = models.SalesOrder.objects.raw("select * from sales_order where order_status = 2 and (delivery_per_name like %s OR order_number = %s OR customer_mobile = %s OR optional_number = %s) and status = 1", [search_txt, search_txt, search_txt, search_txt])
         
        context = {
            'confirm_order':confirm_order, 
            'search_txt':search_txt,  
        }  
        return render(request, 'publisher_app/admin_dashboard/orders/confirm_order.html', context)

@employeeLogin
def dashboard_packed_order_list(request):  
    if request.method == "GET":    
        packed_order_list = models.SalesOrder.objects.filter(order_status = 3, status = True).order_by('-order_number')
            
        context = {
            'packed_order_list':packed_order_list, 
        }
        return render(request, 'publisher_app/admin_dashboard/orders/packed_order_list.html', context)
    else: 
        search_txt = str(request.POST.get('SearchOrder')).strip() 
        packed_order_list = models.SalesOrder.objects.raw("select * from sales_order where order_status = 3 and (delivery_per_name like %s OR order_number = %s OR customer_mobile = %s OR optional_number = %s) and status = 1", [search_txt, search_txt, search_txt, search_txt])
         
        context = {
            'packed_order_list':packed_order_list, 
            'search_txt':search_txt,  
        }  
        return render(request, 'publisher_app/admin_dashboard/orders/packed_order_list.html', context)

@employeeLogin
def dashboard_shipping_order_list(request):  
    if request.method == "GET":    
        shipping_order = models.SalesOrder.objects.filter(order_status = 4, status = True).order_by('-order_number')
            
        context = {
            'shipping_order':shipping_order, 
        }
        return render(request, 'publisher_app/admin_dashboard/orders/shipping_order.html', context)
    else: 
        search_txt = str(request.POST.get('SearchOrder')).strip() 
        shipping_order = models.SalesOrder.objects.raw("select * from sales_order where order_status = 4 and (delivery_per_name like %s OR order_number = %s OR customer_mobile = %s OR optional_number = %s) and status = 1", [search_txt, search_txt, search_txt, search_txt])
         
        context = {
            'shipping_order':shipping_order, 
            'search_txt':search_txt,  
        }
        return render(request, 'publisher_app/admin_dashboard/orders/shipping_order.html', context)

@employeeLogin
def incrementDecrementQuantity(request):  
    if request.is_ajax():
        status = request.GET.get('status')
        OrderNumber = request.GET.get('OrderNumber')
        booknameid = request.GET.get('booknameid') 
        customer_book_id = request.GET.get('customer_book_id') 
        exitbook_price = models.BookList.objects.get(id = booknameid)
        book_mrp_price = int(exitbook_price.book_price) 
        book_sale_price = int(exitbook_price.sale_price) 
        get_OrderNumber = models.SalesOrder.objects.get(order_number = OrderNumber)
        exit_OrderPrice = get_OrderNumber.total_amount
        new_price = int(exit_OrderPrice) - int(book_sale_price) 
        
        if status == "plus":
            models.SalesDetails.objects.filter(id = customer_book_id).update(
                book_quantity = F('book_quantity')+1,
                book_price = F('book_price')+book_mrp_price,
                sale_price = F('sale_price')+book_sale_price,
            )
            models.SalesOrder.objects.filter(order_number = OrderNumber).update(
                total_amount = F('total_amount')+book_sale_price,
            )
        else:
            models.SalesDetails.objects.filter(id = customer_book_id).update(
                book_quantity = F('book_quantity')-1,
                book_price = F('book_price') - book_mrp_price,
                sale_price = F('sale_price') - book_sale_price,
            )
            models.SalesOrder.objects.filter(order_number = OrderNumber).update(
                total_amount = F('total_amount') - book_sale_price,
            )
        data = "Quantity Change Successful"    
        return JsonResponse(data, safe=False)
 

@employeeLogin
def dashboard_delivery_order_list(request):  
    if request.method == "GET":    
        delivery_order_list = models.SalesOrder.objects.filter(order_status = 5, status = True).order_by('-order_number')
            
        context = {
            'delivery_order_list':delivery_order_list, 
        }
        return render(request, 'publisher_app/admin_dashboard/orders/delivery_order_list.html', context)
    else: 
        search_txt = str(request.POST.get('SearchOrder')).strip() 
        delivery_order_list = models.SalesOrder.objects.raw("select * from sales_order where order_status = 5 and (delivery_per_name like %s OR order_number = %s OR customer_mobile = %s OR optional_number = %s) and status = 1", [search_txt, search_txt, search_txt, search_txt])
         
        context = {
            'delivery_order_list':delivery_order_list, 
            'search_txt':search_txt,  
        }
        return render(request, 'publisher_app/admin_dashboard/orders/delivery_order_list.html', context)

@employeeLogin
def dashboard_returned_order_list(request): 
    request.session['previous_url_get'] = None
    
    returned_order_list = models.SalesOrder.objects.filter(order_status = 6, status = True).order_by('-order_number')
        
    context = {
        'returned_order_list':returned_order_list, 
    }
    return render(request, 'publisher_app/admin_dashboard/orders/returned_order_list.html', context)

@employeeLogin
def dashboard_canceled_order_list(request): 
    request.session['previous_url_get'] = None 

    canceled_order_list = models.SalesOrder.objects.filter(order_status = 7, status = True).order_by('-order_number')
        
    context = {
        'canceled_order_list':canceled_order_list, 
    }
    return render(request, 'publisher_app/admin_dashboard/orders/canceled_order_list.html', context)


@employeeLogin
def dashboard_hold_order_list(request):  
    request.session['previous_url_get'] = None  

    hold_order_list = models.SalesOrder.objects.filter(order_status = 8, status = True).order_by('-order_number')
        
    context = {
        'hold_order_list':hold_order_list, 
    }
    return render(request, 'publisher_app/admin_dashboard/orders/hold_order_list.html', context)
 


@employeeLogin
def dashboard_order_items_views(request, order_number):  
    request.session['previous_url_get'] = None  
    get_order_info = models.SalesOrder.objects.filter(order_number = order_number).first()
    district = models.DistrictEntry.objects.filter(status = True)
    upozilla = models.UpozillaEntry.objects.filter(status = True)
    postoffice = models.PostOfficeInfo.objects.filter(status = True)
    courier_list = models.CourierService.objects.filter(status = True).order_by('ordering')
    book_list = models.BookList.objects.raw("""SELECT bk.id, bk.book_name_bangla, bwr.writter_name_bangla, pub.publisher_name_bangla 
        FROM `book_list` bk left JOIN writter_wise_book wwb ON bk.id = wwb.book_name_id 
        LEFT JOIN book_writter_list bwr ON wwb.writter_name_id = bwr.id 
        LEFT JOIN book_publisher_list pub ON bk.publisher_id = pub.id"""
    )
    order_wise_product = models.SalesDetails.objects.raw(
        """ SELECT sd.id, bk.book_name_bangla,bw.writter_name_bangla, bp.publisher_name_bangla, sd.order_number, sd.book_price, sd.sale_price, (sd.sale_price*sd.book_quantity) as total_price, 
        sd.book_quantity, sd.order_date FROM `sales_details` sd LEFT JOIN book_list bk ON sd.book_name_id = bk.id 
        LEFT JOIN writter_wise_book wwb ON bk.id = wwb.book_name_id LEFT JOIN book_writter_list bw ON wwb.writter_name_id = bw.id 
        LEFT JOIN book_publisher_list bp ON bk.publisher_id = bp.id 
        WHERE sd.order_number = %s and sd.status = 1 order by sd.id asc """, [order_number]
    )

    total_order_price, grand_total,total_payable = 0,0,0
    
    for price in order_wise_product:
        total_order_price += price.total_price 

    grand_total =  total_order_price + get_order_info.shipping_charge + get_order_info.vat_amount
    total_payable = grand_total - get_order_info.less_amount

    global val
    def val(): 
        return get_order_info.upozilla_id

    global value
    def value(): 
        return get_order_info.postal_code_id
 

    context = {
        'get_order_info':get_order_info, 
        'district':district, 
        'upozilla':upozilla, 
        'postoffice':postoffice, 
        'book_list':book_list, 
        'upozila_id':get_order_info.upozilla_id,
        'postal_code_id':get_order_info.postal_code_id,
        'order_wise_product':order_wise_product,
        'total_order_price':total_order_price,
        'grand_total':grand_total,
        'total_payable':total_payable,
        'courier_list':courier_list,
    }
     
    return render(request, 'publisher_app/admin_dashboard/orders/view_order.html', context)


@employeeLogin
def orderWiseView(request, order_number):  
    request.session['previous_url_get'] = None  
    get_order_info = models.SalesOrder.objects.filter(order_number = order_number).first()
    district = models.DistrictEntry.objects.filter(status = True)
    upozilla = models.UpozillaEntry.objects.filter(status = True)
    postoffice = models.PostOfficeInfo.objects.filter(status = True)
    courier_list = models.CourierService.objects.filter(status = True).order_by('ordering')
    book_list = models.BookList.objects.raw("""SELECT bk.id, bk.book_name_bangla, bwr.writter_name_bangla, pub.publisher_name_bangla 
        FROM `book_list` bk left JOIN writter_wise_book wwb ON bk.id = wwb.book_name_id 
        LEFT JOIN book_writter_list bwr ON wwb.writter_name_id = bwr.id 
        LEFT JOIN book_publisher_list pub ON bk.publisher_id = pub.id"""
    )
    order_wise_product = models.SalesDetails.objects.raw(
        """ SELECT sd.id, bk.book_name_bangla,bw.writter_name_bangla, bp.publisher_name_bangla, sd.order_number, sd.book_price, sd.sale_price, (sd.sale_price*sd.book_quantity) as total_price, 
        sd.book_quantity, sd.order_date FROM `sales_details` sd LEFT JOIN book_list bk ON sd.book_name_id = bk.id 
        LEFT JOIN writter_wise_book wwb ON bk.id = wwb.book_name_id LEFT JOIN book_writter_list bw ON wwb.writter_name_id = bw.id 
        LEFT JOIN book_publisher_list bp ON bk.publisher_id = bp.id 
        WHERE sd.order_number = %s and sd.status = 1 order by sd.id asc """, [order_number]
    )

    total_order_price, grand_total,total_payable = 0,0,0
    
    for price in order_wise_product:
        total_order_price += price.total_price 

    grand_total =  total_order_price + get_order_info.shipping_charge + get_order_info.vat_amount
    total_payable = grand_total - get_order_info.less_amount
  
    context = {
        'get_order_info':get_order_info, 
        'district':district, 
        'upozilla':upozilla, 
        'postoffice':postoffice, 
        'book_list':book_list, 
        'upozila_id':get_order_info.upozilla_id,
        'postal_code_id':get_order_info.postal_code_id,
        'order_wise_product':order_wise_product,
        'total_order_price':total_order_price,
        'grand_total':grand_total,
        'total_payable':total_payable,
        'courier_list':courier_list,
    }
     
    return render(request, 'publisher_app/admin_dashboard/orders/orderWiseView.html', context)

@employeeLogin
def dashboardOrderPrint(request):
    if request.method == "POST":
        order_number = request.POST.get('order_number')
        get_order_info = models.SalesOrder.objects.filter(order_number = order_number).first()

        order_wise_product = models.SalesDetails.objects.raw(
            """ SELECT sd.id, bk.book_name_bangla,bw.writter_name_bangla, bp.publisher_name_bangla, sd.order_number, sd.book_price, sd.sale_price, (sd.sale_price*sd.book_quantity) as total_price, 
            sd.book_quantity, sd.order_date FROM `sales_details` sd LEFT JOIN book_list bk ON sd.book_name_id = bk.id 
            LEFT JOIN writter_wise_book wwb ON bk.id = wwb.book_name_id LEFT JOIN book_writter_list bw ON wwb.writter_name_id = bw.id 
            LEFT JOIN book_publisher_list bp ON bk.publisher_id = bp.id 
            WHERE sd.order_number = %s and sd.status = 1 order by sd.id asc """, [order_number]
        )

        total_order_price, grand_total,total_payable = 0,0,0
        
        for price in order_wise_product:
            total_order_price += price.total_price 

        grand_total =  total_order_price + get_order_info.shipping_charge + get_order_info.vat_amount
        total_payable = grand_total - get_order_info.less_amount
     
        context = {
            'get_order_info':get_order_info, 
            'upozila_id':get_order_info.upozilla_id,
            'postal_code_id':get_order_info.postal_code_id,
            'order_wise_product':order_wise_product,
            'total_order_price':total_order_price,
            'grand_total':grand_total,
            'total_payable':total_payable,
        }
    
        return render(request, 'publisher_app/admin_dashboard/orders/OrderPrint.html', context)
    else:
        pass

@employeeLogin
def dashboard_customize_order_add(request):   
    if request.is_ajax(): 
        order_number = request.GET.get('OrderNumber')
        book_name_id = request.GET.get('book_name_id')
        book_quantity = request.GET.get('book_quantity')  
        find_order_number = models.SalesOrder.objects.filter(order_number = order_number)
        customer_id = find_order_number[0].customer_name_id  
        get_book_id = models.BookList.objects.get(id = book_name_id) 
        new_price = int(get_book_id.sale_price) * int(book_quantity)
        
        get_exit_book = models.SalesDetails.objects.filter(order_number = order_number, book_name_id = book_name_id)
        
        if not get_exit_book: 
            exit_price = models.SalesOrder.objects.get(order_number = order_number)
            new_book_price = int(exit_price.total_amount) + new_price
            models.SalesDetails.objects.create( 
                order_number = order_number, 
                book_name_id = book_name_id, 
                book_quantity = book_quantity, 
                book_price = get_book_id.book_price, 
                sale_price = get_book_id.sale_price,
                order_date = find_order_number[0].order_date
            )
            models.SalesOrder.objects.filter(order_number = order_number, customer_name_id = customer_id).update(
                total_amount = new_book_price, update_date = datetime.datetime.now(), 
            )
            data = "Successful"
            return JsonResponse(data, safe=False) 
        else:
            data = "Book Already Added"
            return JsonResponse(data, safe=False) 
       
         
    data = "New Book Add Successful"
    return JsonResponse(data, safe=False)

@employeeLogin   
def UpdateOrder(request):   
    if request.is_ajax():
        less_amount = request.GET.get('less_amount')
        OrderNumber = request.GET.get('OrderNumber')
        shipping_charge = request.GET.get('shipping_charge')  

        models.SalesOrder.objects.filter(order_number = OrderNumber).update(
            less_amount = less_amount, shipping_charge = shipping_charge,
        )
     
        data = "Order Update Successful"    
        return JsonResponse(data, safe=False)
 
 
@employeeLogin
def dashboard_customize_order_delete(request, id):  
    getBook = models.SalesDetails.objects.filter(id = id).first()
    order_num = str(getBook.order_number) 
    delete_price = int(getBook.sale_price)  
    models.SalesOrder.objects.filter(order_number = order_num).update(
       total_amount = F('total_amount') - delete_price, 
    )
    getBook.delete() 
    return redirect('/dashboard-orders-details/'+order_num+'/')


val = None
value = None
import datetime
import time 
import random

@employeeLogin
def dashboard_update_order(request):   
    if request.method=="POST":
        order_number = request.POST['order_number']
        order_status    = request.POST['order_status']
        delivery_method_id = int(request.POST.get('delivery_method')) 
        print(delivery_method_id)
         
        previous_url_get    = request.POST['previous_url_get']
        request.session['previous_url_get'] = previous_url_get
        
 
        customer_info = models.SalesOrder.objects.filter(order_number = order_number)
          
        models.SalesOrder.objects.filter(order_number = order_number).update(
            delivery_per_name    = request.POST['del_per_name'],
            customer_mobile = request.POST.get('customer_mobile'),
            optional_number = request.POST.get('optional_number'),
            customer_email  = request.POST.get('customer_email'), 
            delivery_method_id = delivery_method_id,
            order_status    = order_status,
            payment_status  = request.POST['payment_status'],
            service_code    = request.POST['service_code'],
            service_charge  = request.POST['service_charge'],
            payment_method  = request.POST['payment_method'], 
            shipping_address = request.POST['address'],
            district_id     = int(request.POST['district_name']),
            upozilla_id     = int(request.POST['upozilla_name']),
            postal_code_id  = request.POST['postal_code'], 
            order_remarks   = request.POST['customer_note'],
            shipping_charge = request.POST['shipping_charge'],
            less_amount     = request.POST['less_amount'],
            update_date     = datetime.datetime.now(), 
        ) 
 
        messages.success(request, "Order Info Update Successful")
        return redirect('/dashboard-orders-details/'+order_number)

    
 
# Sales Reports  
@employeeLogin
def dashboard_sales_history(request):   
    request.session['sales_list'] = None
    if request.method =="POST":
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        order_status = request.POST.get('order_status')

        arr = []
        query_str = ""
        sales_list = ""

        if from_date:
            arr.append(from_date+str(' 00:00:00'))
            query_str += " and order_date >= %s"

        if to_date:
            arr.append(to_date+str(' 23:59:59'))
            query_str += " and order_date <= %s"

        if order_status:
            arr.append(order_status)
            query_str += " and order_status = %s"
         
        sales_list = models.SalesOrder.objects.raw("SELECT * FROM sales_order where status = 1 "+query_str+" order by order_number desc", arr)
         
        
        if from_date and to_date:
            from_date2 = str("'")+from_date+str(" 00:00:00")+str("'")
            to_date2   = str("'")+to_date+str(" 23:59:59")+str("'")
            print("to_date2 :", to_date2)
            request.session['sales_list'] = str(sales_list.query).replace("order_date >= "+from_date+" 00:00:00 and order_date <= "+to_date+" 23:59:59", "order_date >= "+from_date2+" and order_date <= "+to_date2) 

        elif from_date and not to_date:
            from_date2 = str("'")+from_date+str(" 00:00:00")+str("'")
            request.session['sales_list'] = str(sales_list.query).replace("order_date >= "+from_date+" 00:00:00", "order_date >= "+from_date2)
        elif to_date and not from_date:
            to_date2 = str("'")+to_date+str(" 23:59:59")+str("'")
            request.session['sales_list'] = str(sales_list.query).replace("order_date <= "+to_date+" 23:59:59", "order_date <= "+to_date2)

        elif order_status:  
            request.session['sales_list'] = str(sales_list.query) 

        else: 
            request.session['sales_list'] = str(sales_list.query) 

        print("request session: ", request.session['sales_list']) 

        total_summary = 0
        for amount in  sales_list: 
            total_summary += amount.total_amount
        
        context = {
            'sales_list': sales_list,
            'total_summary': total_summary,
            'from_date': from_date,
            'to_date': to_date,
        }  
        return render(request, 'publisher_app/admin_dashboard/sales/sales_history.html', context)
    else:
        return render(request, 'publisher_app/admin_dashboard/sales/sales_history.html')

 
from django.http import  Http404
def download_excel_sheet(file_name):
    file_path = os.path.join(settings.MEDIA_ROOT+'/excel_templates/', file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404  


def ExportSalesList(request):  
    sales_order_list = models.SalesOrder.objects.raw(request.session["sales_list"]) 
    print(len(sales_order_list))    
    if sales_order_list: 
        if not os.path.exists(settings.MEDIA_ROOT+'/excel_templates/'):
            os.mkdir(settings.MEDIA_ROOT+'/excel_templates/')

        file_name = "sales_order_list.xlsx"
        file_path = os.path.join(settings.MEDIA_ROOT+'/excel_templates/',file_name)
        if os.path.isfile(settings.MEDIA_ROOT+'/excel_templates/'+file_name):
            os.remove(settings.MEDIA_ROOT+'/excel_templates/'+file_name)

        if not os.path.exists(file_path):
            workbook  = xlsxwriter.Workbook(settings.MEDIA_ROOT+'/excel_templates/'+file_name)
            worksheet = workbook.add_worksheet()

            worksheet.write('A1','Order Date') 
            worksheet.write('B1','Order Number') 
            worksheet.write('C1','Customer Name') 
            worksheet.write('D1','Mobile')    
            worksheet.write('E1','Payment Method')    
            worksheet.write('F1','Payment Status')    
            worksheet.write('G1','Order Status')    
            worksheet.write('H1','Total Amount')    

            worksheet.set_column('A:A', 15)
            worksheet.set_column('B:B', 15) 
            worksheet.set_column('C:C', 25) 
            worksheet.set_column('D:D', 15)  
            worksheet.set_column('E:E', 15)  
            worksheet.set_column('F:F', 15)  
            worksheet.set_column('G:G', 15)  
            worksheet.set_column('H:H', 15)  
                
            count = 2 
            for i in sales_order_list:   
                worksheet.write('A'+str(count), str(i.order_date))
                worksheet.write('B'+str(count), str(i.order_number))
                worksheet.write('C'+str(count), str(i.customer_name.customer_name)) 
                worksheet.write('D'+str(count), str(i.customer_name.mobile)) 
                worksheet.write('E'+str(count), str(i.get_payment_method_display())) 
                worksheet.write('F'+str(count), str(i.get_payment_status_display())) 
                worksheet.write('G'+str(count), str(i.get_order_status_display())) 
                worksheet.write('H'+str(count), str(i.total_amount))
                count +=1
         
            workbook.close()
            return download_excel_sheet(file_name)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        




    
#----------------- dashboard CustomerList  ---------------------------#   
@employeeLogin
def dashboardCustomerList(request):  
    customer_list = models.CustomarAccount.objects.filter(status = True).order_by('-id')
    context = {
        'customer_list':customer_list,  
    }
    return render(request, 'publisher_app/admin_dashboard/settings/customer_list.html', context)
    
#----------------- Blog List Code here ---------------------------#   
@employeeLogin
def dashboard_blog_list(request):  
    blog_list = models.BlogMaster.objects.filter(status = True).order_by('-id')
    context = {
        'blog_list':blog_list,  
    }
    return render(request, 'publisher_app/admin_dashboard/blog/blog_list.html', context)

#----------------- Delete Blog Code here ---------------------------#    
@employeeLogin
def dashboard_blog_delete(request, id):  
    models.BlogComment.objects.filter(blog_id=id).delete()
    get_blog = models.BlogMaster.objects.filter(id=id)
    if get_blog:
        get_blog[0].blog_image.delete()
    get_blog.delete() 
    return redirect("/dashboard/blog/blog-list/")


#----------------- New Blog add Code here ---------------------------#   
@employeeLogin       
def dashboard_add_new_blog(request):  
    category_list = models.BookCategory.objects.filter(status = True)
    if request.method =="POST":
        blog_category   = int(request.POST.get('blog_category'))
        blog_title      = request.POST.get('blog_title') 
        blog_details    = request.POST.get('blog_details')
        blog_title_english      = request.POST.get('blog_title_english')  
        lowletter = blog_title_english.lower()
        blog_url = (lowletter.replace(" ", "-")) 

        document_path = ""
        if bool(request.FILES.get('blog_image', False)) == True:
            file = request.FILES['blog_image']   
            if not os.path.exists("blog_image"):
                os.mkdir("blog_image")

            document_path = default_storage.save("blog_image/"+file.name, ContentFile(file.read()))
            if document_path:
                document_path = str("blog_image/")+str(document_path).split("/")[-1] 
             

        models.BlogMaster.objects.create(
            category_id = blog_category, blog_title = blog_title, blog_details = blog_details, blog_url = blog_url, blog_title_english = blog_title_english,
            blog_image = document_path, created_by_id = request.session.get('user_id')
        )
        return redirect("/dashboard/blog/blog-list/")
    
    context = {
        'category_list':category_list,
    }
    return render(request, 'publisher_app/admin_dashboard/blog/add_new_blog.html', context)


#----------------- Blog Update Code here ---------------------------#   
@employeeLogin  
def dashboard_blog_update(request, id): 
    get_comments = models.BlogMaster.objects.get(id = id)
    category_list = models.BookCategory.objects.filter(status = True)
    if request.method =="POST":
        blog_category       = int(request.POST.get('blog_category'))
        blog_title          = request.POST.get('blog_title')  
        blog_title_english  = request.POST.get('blog_title_english') 
        blog_details        = request.POST.get('blog_details') 
        lowletter           = blog_title_english.lower()
        blog_url            = (lowletter.replace(" ", "-")) 
 
        document_path = str(get_comments.blog_image) if get_comments.blog_image else "" 
        if bool(request.FILES.get('blog_image', False)) == True:
            file = request.FILES['blog_image']   
            if not os.path.exists("blog_image"):
                os.mkdir("blog_image")

            document_path = default_storage.save("blog_image/"+file.name, ContentFile(file.read()))
            if document_path:
                document_path = str("blog_image/")+str(document_path).split("/")[-1] 
              
        models.BlogMaster.objects.filter(id = id).update(
            category_id = blog_category, blog_title = blog_title, blog_details = blog_details, blog_url = blog_url, blog_title_english = blog_title_english,
            blog_image = document_path, created_by_id = request.session.get('user_id')
        )
        return redirect("/dashboard/blog/blog-list/")
    
    context = {
        'category_list':category_list,
        'get_comments':get_comments,
    }
    return render(request, 'publisher_app/admin_dashboard/blog/update_new_blog.html', context)


def master_category_list(request):
    category_list = models.MastarCategorySetup.objects.filter(status = True).order_by('-id')
 
    context = {
        'category_list': category_list
    }
    return render(request, 'publisher_app/admin_dashboard/settings/master_category_list.html', context)


def master_category_add(request):
    if request.method == "POST":
        category_bangla = request.POST.get('category_bangla')
        category_english = request.POST.get('category_english').strip()
        loletterr = category_english.lower()
        menu_url = (loletterr.replace(" ", "-")) 


        models.MastarCategorySetup.objects.create(
            cat_name_bangla = category_bangla, cat_name_english = category_english, menu_url = menu_url,
            Is_homepage     = True if request.POST.get('is_homepage') else False,
            Is_mainmenu     = True if request.POST.get('is_mainmenu') else False,
            Is_book         = True if request.POST.get('is_book') else False,
        )
        messages.success(request, "Master Category add successful.")
        return redirect('/master-category-list/')
    
    return render(request, 'publisher_app/admin_dashboard/settings/master_category_add.html')

def master_category_update(request, id):
    get_category = models.MastarCategorySetup.objects.get(id=id)
    if request.method == "POST":
        category_bangla = request.POST.get('category_bangla')
        category_english = request.POST.get('category_english').strip()
        loletterr = category_english.lower()
        menu_url = (loletterr.replace(" ", "-"))  

        models.MastarCategorySetup.objects.filter(id=id).update(
            cat_name_bangla = category_bangla, cat_name_english = category_english, menu_url = menu_url,
            Is_homepage     = True if request.POST.get('is_homepage') else False,
            Is_mainmenu     = True if request.POST.get('is_mainmenu') else False,
            Is_book         = True if request.POST.get('is_book') else False,
        )
        messages.success(request, "Master Category add successful.")
        return redirect('/master-category-list/')
    
    context = {
        'get_category': get_category,
    }
    return render(request, 'publisher_app/admin_dashboard/settings/master_category_edit.html', context)


def master_subcategory_list(request): 
    sub_category_list = models.MastarSubCategory.objects.filter(status = True).order_by('-id')
 
    context = { 
        'sub_category_list': sub_category_list,
    }
    return render(request, 'publisher_app/admin_dashboard/settings/master_subcategory_list.html', context)
     
def master_subcategory_add(request): 
    if request.method == "GET":
        category_list = models.BookCategory.objects.filter(status = True) 
        master_category_list = models.MastarCategorySetup.objects.filter(status = True) 
        
        context = {
            'category_list': category_list,
            'master_category_list': master_category_list
        }
        return render(request, 'publisher_app/admin_dashboard/settings/master_subcategory_add.html', context) 
        
    else: 
        master_category_id = int(request.POST.get('master_category_id'))
        regular_category_id = int(request.POST.get('regular_category_id'))
        sub_category_bangla = request.POST.get('sub_category_bangla')
        sub_category_english = request.POST.get('sub_category_english').strip()  
        loletterr = sub_category_english.lower()
        menu_url = (loletterr.replace(" ", "-")) 

        models.MastarSubCategory.objects.create(
            master_category_id = master_category_id, regular_category_id = regular_category_id,
            sub_category_bangla = sub_category_bangla,
            sub_category_english = sub_category_english, menu_url = menu_url,
            Is_homepage     = True if request.POST.get('is_homepage') else False,
            Is_mainmenu     = True if request.POST.get('is_mainmenu') else False,
        )
        
        messages.success(request, "Sub Category add successful.")
        return redirect('/master-subcategory-list/')
     
def master_subcategory_update(request, id): 
    get_data = models.MastarSubCategory.objects.get(id = id)
    category_list = models.BookCategory.objects.filter(status = True) 
    master_category_list = models.MastarCategorySetup.objects.filter(status = True) 
  
    if request.method == "POST":
        master_category_id = int(request.POST.get('master_category_id'))
        regular_category_id = int(request.POST.get('regular_category_id'))
        sub_category_bangla = request.POST.get('sub_category_bangla')
        sub_category_english = request.POST.get('sub_category_english').strip()  
        loletterr = sub_category_english.lower()
        menu_url = (loletterr.replace(" ", "-")) 

        models.MastarSubCategory.objects.filter(id=id).update(
            master_category_id = master_category_id, regular_category_id = regular_category_id,
            sub_category_bangla = sub_category_bangla,
            sub_category_english = sub_category_english, menu_url = menu_url,
            Is_homepage     = True if request.POST.get('is_homepage') else False,
            Is_mainmenu     = True if request.POST.get('is_mainmenu') else False,
        )
        
        messages.success(request, "Sub Category add successful.")
        return redirect('/master-subcategory-list/')

    context = {
        'get_data': get_data,
        'category_list': category_list,
        'master_category_list': master_category_list
    }
    return render(request, 'publisher_app/admin_dashboard/settings/master_subcategory_edit.html', context) 

def master_subcategory_delete(request, id):
    models.MastarSubCategory.objects.filter(id=id).delete()
    messages.success(request, "Sub Category delete successful.")
    return redirect('/master-subcategory-list/')
 
@csrf_exempt
def payment_success(request): 
    context = { 
        'count' : models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
        'website_menu': models.MastarSubCategory.objects.filter(status = True, regular_category__Is_top_category = True).order_by('master_category', 'regular_category'),
    } 
    return render(request, 'publisher_app/aamarpay/success.html', context) 

@csrf_exempt
def payment_cancel(request):
    context = { 
        'count' : models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
        'website_menu': models.MastarSubCategory.objects.filter(status = True, regular_category__Is_top_category = True).order_by('master_category', 'regular_category'),
    } 
    return render(request, 'publisher_app/aamarpay/cancel.html', context) 

@csrf_exempt
def payment_failed(request): 
    print(request.POST.__dict__)  
    context = { 
        'count' : models.AddToCart.objects.filter(session_key = request.session.get("abcd")).count(),
        'wishlist_count' : models.AddToWishlist.objects.filter(session_key = request.session.get("abcd")).count(),
        'website_menu': models.MastarSubCategory.objects.filter(status = True, regular_category__Is_top_category = True).order_by('master_category', 'regular_category'),
    } 
    return render(request, 'publisher_app/aamarpay/failed.html', context)  
 
def importSubcategory(request):
    if request.method == "POST":
        xl = pd.read_excel(request.FILES["import_file"], "Sheet1") 
        headers = list(xl.head(0))
        update_count, new_count = 1, 0 
        for i in range(1,len(xl)): 
            master_cate_id  = xl["Master id"][i]
            regular_cate_id = str(xl["Regular Category id"][i])
            sub_category_name = str(xl["Sub category"][i]) 
            loletterr = sub_category_name.lower()
            menu_url = (loletterr.replace(" ", "-"))  
 
            models.MastarSubCategory.objects.create(
                master_category_id = int(master_cate_id),
                regular_category_id = int(regular_cate_id),
                sub_category_bangla = sub_category_name,
                sub_category_english = sub_category_name,
                menu_url = menu_url, 
            ) 
            update_count += 1
        messages.success(request, "Sub Category Import successful.")
        return redirect('/master-subcategory-list/')
 
    else:
        pass


def importcategorywisebook(request):
    if request.method == "POST":
        xl = pd.read_excel(request.FILES["import_file"], "Sheet1")  
        update_count = 1
 
        for i in range(1,len(xl)): 
            book_id  = xl["Book Id"][i]
            cate_id = str(xl["Category Id"][i]) 
 
            models.CategoryWiseBook.objects.create(
                book_name_id = int(book_id),
                category_name_id = int(cate_id), 
            ) 
            update_count += 1
        messages.success(request, "Category Wise book Import successful.")
        return redirect('/master-subcategory-list/')
 
    else:
        pass

def importsubcategorywisebook(request):
    if request.method == "POST":
        xl = pd.read_excel(request.FILES["import_file"], "Sheet1")  
        update_count = 1
 
        for i in range(1,len(xl)): 
            book_id  = xl["Book ID"][i]
            cate_name = str(xl["Regular"][i]) 
            subcat_name = str(xl["Sub category"][i])  

            get_sub_cate = models.MastarSubCategory.objects.filter(regular_category__cat_name_bangla = cate_name, sub_category_bangla = subcat_name).first()
            
            models.SubCategoryWiseBook.objects.create(
                book_name_id = int(book_id),
                subcategory_name_id = int(get_sub_cate.id), 
            ) 
            update_count += 1
        messages.success(request, "Sub Category Wise book Import successful.")
        return redirect('/master-subcategory-list/')
 
    else:
        pass


		


    