from django import template
from publisher_app import models

register = template.Library()

@register.filter(name='shop_profile')
def shop_profile_load(request):
    profile = models.PublisherProfile.objects.filter(status=True)
    if profile:
        return profile
 
@register.filter(name='topmenu')
def topmenu_load(request):
    website_menu = models.MastarSubCategory.objects.filter(status = True).order_by('master_category', 'regular_category')
    if website_menu:
        return website_menu

# @register.filter(name='topmenu')
# def topmenu_load(request):
#     top_menu = models.BookCategory.objects.filter(Is_mainmenu=True)
#     if top_menu:
#         return top_menu
 
@register.filter(name='book_category2')
def category_load2(request):
    book_catagory = models.BookCategory.objects.filter(status=True, Is_top_category=1, Is_homepage = False).order_by('Is_top_category')[:20]
    if book_catagory:
        return book_catagory


@register.filter(name='total_book_category2')
def total_category_load2(request):
    total_category = models.BookCategory.objects.filter(status=True).order_by('id') 
    if total_category:
        total_category = len(list(total_category))
        return total_category


@register.filter(name='total_book_list')
def total_book_load(request):
    total_book = models.BookList.objects.filter(status=True)
    if total_book:
        total_book = len(list(total_book))
        return total_book



@register.filter(name='book_category')
def category_load(request):
    book_cat = models.BookCategory.objects.filter(status=True)
    if book_cat:
        return book_cat


@register.filter(name='book_writter')
def writter_load(request):
    writter = models.BookWritter.objects.filter(status=True)
    if writter:
        return writter

@register.filter(name='total_book_writter')
def total_writter_load(request):
    total_writter = models.BookWritter.objects.filter(status=True)
    if total_writter:
        total_writter = len(list(total_writter))
        return total_writter


@register.filter(name='book_publisher')
def publisher_load(request):
    publisher = models.Publisher.objects.filter(status=True)
    if publisher:
        return publisher

@register.filter(name='total_book_publisher')
def total_publisher_load(request):
    total_publisher = models.Publisher.objects.filter(status=True)
    if total_publisher:
        total_publisher = len(list(total_publisher))
        return total_publisher

@register.filter(name='book_list')
def all_book_load(request):
    all_book =  book_list = models.BookList.objects.raw('''
        SELECT bk.id, bk.book_name_bangla, bk.book_name_english, bk.sale_price, bk.book_price, bk.discount, bc.cat_name_bangla, cwb.category_name_id, bc.menu_url, bw.writter_name_bangla FROM `durbar_shop_booklist` bk LEFT JOIN durbar_shop_categorywisebook cwb ON bk.id = cwb.book_name_id
        LEFT JOIN durbar_shop_bookcategory bc ON cwb.category_name_id = bc.id  LEFT JOIN durbar_shop_writterwisebook wwb ON bk.id = wwb.book_name_id
        LEFT JOIN durbar_shop_bookwritter bw ON  wwb.writter_name_id = bw.id  WHERE bc.Is_homepage = 1 ORDER BY bc.ordering asc
    ''')
    if all_book:
        return all_book
 
 
@register.filter(name='total_all_order')
def load_all_order(request):
    all_order = models.CustomarOrderList.objects.raw("SELECT clo.id , cl.id, clo.customer_name_id, sum(clo.book_price) as book_price, cl.shipping_charge, cl.less_amount, ((sum(clo.book_price)+cl.shipping_charge)-cl.less_amount) as total_price, clo.order_date FROM `durbar_shop_customarorderlist` clo INNER JOIN durbar_shop_customarlist cl ON clo.order_number = cl.order_number GROUP BY clo.order_number order BY clo.order_number desc, clo.order_date")
    total_all_order = 0
    if all_order:
        total_all_order = len(list(all_order))
        return total_all_order
 
 
@register.filter(name='total_pending_order')
def load_pending_order(request):
    pending_list = models.CustomarOrderList.objects.raw("SELECT clo.id, clo.customer_name_id, cl.customer_mobile, cl.order_number, sum(clo.book_price) as book_price, cl.shipping_charge, (sum(clo.book_price)+cl.shipping_charge) as total_price, clo.order_date, clo.order_status FROM `durbar_shop_customarorderlist` clo INNER JOIN durbar_shop_customarlist cl ON clo.order_number = cl.order_number WHERE clo.order_status = 1 GROUP BY clo.order_number order BY cl.id asc")

    total_pending = 0
    if pending_list:
        total_pending = len(list(pending_list))
        return total_pending
 

@register.filter(name='total_confirm_order')
def load_confirm_order(request):
    confirm_list = models.CustomarOrderList.objects.raw("SELECT clo.id, clo.customer_name_id, cl.customer_mobile, cl.order_number, sum(clo.book_price) as book_price, cl.shipping_charge, (sum(clo.book_price)+cl.shipping_charge) as total_price, clo.order_date, clo.order_status FROM `durbar_shop_customarorderlist` clo INNER JOIN durbar_shop_customarlist cl ON clo.order_number = cl.order_number WHERE clo.order_status = 2 GROUP BY clo.order_number order BY cl.id asc")
    total_confirm = 0
    if confirm_list:
        total_confirm = len(list(confirm_list))
        return total_confirm


@register.filter(name='total_packet_order')
def load_packet_order(request):
    packed_order_list = models.CustomarOrderList.objects.raw("SELECT clo.id, clo.customer_name_id, cl.customer_mobile, cl.order_number, sum(clo.book_price) as book_price, cl.shipping_charge, (sum(clo.book_price)+cl.shipping_charge) as total_price, clo.order_date, clo.order_status FROM `durbar_shop_customarorderlist` clo INNER JOIN durbar_shop_customarlist cl ON clo.order_number = cl.order_number WHERE clo.order_status = 3 GROUP BY clo.order_number order BY cl.id asc")
    
    total_packed = 0
    if packed_order_list:
        total_packed = len(list(packed_order_list))
        return total_packed

@register.filter(name='total_shipping_order')
def load_shipping_order(request):
    packed_shipping_list = models.CustomarOrderList.objects.raw("SELECT clo.id, clo.customer_name_id, cl.customer_mobile, cl.order_number, sum(clo.book_price) as book_price, cl.shipping_charge, (sum(clo.book_price)+cl.shipping_charge) as total_price, clo.order_date, clo.order_status FROM `durbar_shop_customarorderlist` clo INNER JOIN durbar_shop_customarlist cl ON clo.order_number = cl.order_number WHERE clo.order_status = 4 GROUP BY clo.order_number order BY cl.id asc")

    total_shipping = 0
    if packed_shipping_list:
        total_shipping = len(list(packed_shipping_list))
        return total_shipping

@register.filter(name='total_delivery_order')
def load_delivery_order(request):
    delivery_order_list = models.CustomarOrderList.objects.raw("SELECT clo.id, clo.customer_name_id, cl.customer_mobile, cl.order_number, sum(clo.book_price) as book_price, cl.shipping_charge, (sum(clo.book_price)+cl.shipping_charge) as total_price, clo.order_date, clo.order_status FROM `durbar_shop_customarorderlist` clo INNER JOIN durbar_shop_customarlist cl ON clo.order_number = cl.order_number WHERE clo.order_status = 5 GROUP BY clo.order_number order BY cl.id desc")

    total_delivery = 0
    if delivery_order_list:
        total_delivery = len(list(delivery_order_list))
        return total_delivery


@register.filter(name='total_returned_order')
def load_returned_order(request):
    returned_order_list = models.CustomarOrderList.objects.raw("SELECT clo.id, clo.customer_name_id, cl.customer_mobile, cl.order_number, sum(clo.book_price) as book_price, cl.shipping_charge, (sum(clo.book_price)+cl.shipping_charge) as total_price, clo.order_date, clo.order_status FROM `durbar_shop_customarorderlist` clo INNER JOIN durbar_shop_customarlist cl ON clo.order_number = cl.order_number WHERE clo.order_status = 6 GROUP BY clo.order_number order BY cl.id desc" )

    total_returned = 0
    if returned_order_list:
        total_returned = len(list(returned_order_list))
        return total_returned


@register.filter(name='total_canceled_order')
def load_canceled_order(request):
    canceled_order_list = models.CustomarOrderList.objects.raw("SELECT clo.id, clo.customer_name_id, cl.customer_mobile, cl.order_number, sum(clo.book_price) as book_price, cl.shipping_charge, (sum(clo.book_price)+cl.shipping_charge) as total_price, clo.order_date, clo.order_status FROM `durbar_shop_customarorderlist` clo INNER JOIN durbar_shop_customarlist cl ON clo.order_number = cl.order_number WHERE clo.order_status = 7 GROUP BY clo.order_number order BY cl.id desc" )
    
    total_canceled = 0
    if canceled_order_list:
        total_canceled = len(list(canceled_order_list))
        return total_canceled



@register.filter(name='total_hold_order')
def load_hold_order(request):
    hold_order_list = models.CustomarOrderList.objects.raw("SELECT clo.id, clo.customer_name_id, cl.customer_mobile, cl.order_number, sum(clo.book_price) as book_price, cl.shipping_charge, (sum(clo.book_price)+cl.shipping_charge) as total_price, clo.order_date, clo.order_status FROM `durbar_shop_customarorderlist` clo INNER JOIN durbar_shop_customarlist cl ON clo.order_number = cl.order_number WHERE clo.order_status = 8 GROUP BY clo.order_number order BY cl.id asc")
    
    total_hold = 0
    if hold_order_list:
        total_hold = len(list(hold_order_list)) 
        return total_hold




