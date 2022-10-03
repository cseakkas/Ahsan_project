from csv import writer
import os
from socket import create_connection
from unicodedata import category
from django.db import models
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField
import datetime
from django.conf import settings
import re
from django.utils.timezone import get_fixed_timezone, utc
from django.contrib.auth.models import User
# from grpc import Status


class PublisherProfile(models.Model):
    publisher_name     = models.CharField(max_length=100, blank=True)
    slugan       = models.CharField(max_length=100, blank=True)
    page_title   = models.CharField(max_length=100, blank=True)
    email1       = models.EmailField(max_length=100, blank=True)
    email2       = models.EmailField(max_length=100, blank=True)
    mobile1      = models.CharField(max_length=15,  blank=True)
    mobile2      = models.CharField(max_length=15,  blank=True)
    address      = models.TextField(blank=True)
    pro_details  = RichTextField(blank=True)
    logo           = models.ImageField(upload_to='images/logo')
    favicon_logo   = models.ImageField(upload_to='images/logo')
    about_content  = RichTextField(blank=True)
    about_content  = RichTextField(blank=True)
    about_images   = models.ImageField(upload_to='images/about_images')
    why_buy        = models.TextField(blank=True) 
    shipping_policy  = RichTextField(blank=True)
    terms_condition  = RichTextField(blank=True) 
    map_locationo  = models.TextField(blank=True)
    facebook_link  = models.TextField(blank=True)
    instagram_link  = models.TextField(blank=True)
    youtube_link  = models.TextField(blank=True)
    linkedin_link  = models.TextField(blank=True)
    staring_year  = models.IntegerField()
    copy_right    = models.CharField(max_length=50, blank=True)
    status       = models.BooleanField(default=True)

    def __str__(self):
        return self.publisher_name
    class Meta:
        db_table = 'shop_profile'
        verbose_name = 'Publisher Profile'
        verbose_name_plural = 'Publisher Profile Information'


class SliderInfo(models.Model):
    slider_name   = models.CharField(max_length=100, blank=True)
    title1        = models.CharField(max_length=200, blank=True)
    title2        = models.CharField(max_length=200, blank=True)
    slider_images = models.ImageField(upload_to='images/slider')
    slider_link   = models.TextField(blank=True)
    upload_date   = models.DateTimeField(auto_now_add=True)
    slider_order  = models.IntegerField()
    status        = models.BooleanField(default=True)

    class Meta:
        db_table = 'slider_list'
        verbose_name = 'Slider Image'
        verbose_name_plural = 'Slider Images'

    def url(self):
        return os.path.join('/static/publisher_app/media/images/slider/', os.path.basename(str(self.slider_images)))

    def photo(self):
        return mark_safe('<img src = "{}" width="80"/>'.format(self.url()))

    def __str__(self):
        return self.slider_name
 
class MastarCategorySetup(models.Model):  
    cat_name_bangla  = models.CharField(max_length=150)
    cat_name_english = models.CharField(max_length=150, blank=True)
    detail        = models.TextField(blank=True)
    Is_homepage   = models.BooleanField(default=False)
    Is_mainmenu   = models.BooleanField(default=False)
    Is_book       = models.BooleanField(default=False)
    Is_top_category   = models.BooleanField(default=False)
    menu_url      = models.CharField(max_length=450,blank = True)
    category_cover = models.ImageField(upload_to='images/category_cover', blank = True)
    ordering       = models.IntegerField(default = 1000)
    status        = models.BooleanField(default=True)

    def __str__(self):
        return str(self.cat_name_bangla)

    class Meta:
        db_table = 'master_category' 


class BookCategory(models.Model):
    master_category     = models.ForeignKey(MastarCategorySetup, on_delete=models.DO_NOTHING, null=True, blank=True) 
    cat_name_bangla     = models.CharField(max_length=150)
    cat_name_english    = models.CharField(max_length=150, blank=True)
    detail              = models.TextField(blank=True)
    Is_homepage         = models.BooleanField(default=False)
    Is_mainmenu         = models.BooleanField(default=False)
    Is_top_category     = models.BooleanField(default=False)
    menu_url            = models.CharField(max_length=450,blank = True)
    category_cover      = models.ImageField(upload_to='images/category_cover', blank = True)
    ordering            = models.IntegerField(default = 1000)
    status              = models.BooleanField(default=True)

    def __str__(self):
        return self.cat_name_bangla

    class Meta:
        db_table = 'book_category_list'
        verbose_name = 'Book Category'
        verbose_name_plural = 'Add Book Category'

class BookWritter(models.Model):
    writter_name_bangla    = models.CharField(max_length=150)
    writter_name_english   = models.CharField(max_length=150, blank=True)
    menu_url        = models.CharField(max_length=450,blank = True)
    email           = models.EmailField(max_length=150, blank = True)
    mobile          = models.CharField(max_length=15, blank = True)
    qualification   = models.CharField(max_length=15, blank = True)
    designation     = models.CharField(max_length=15, blank = True)
    specialist      = models.CharField(max_length=15, blank = True)
    date_of_birth   = models.CharField(max_length=15, blank = True)
    address         = models.TextField( blank = True)
    personal_details = RichTextField(blank = True)
    writter_images   = models.CharField(max_length=450,blank = True)
    is_writer        = models.BooleanField(default=1)
    is_translator    = models.BooleanField(default=0)
    is_editor        = models.BooleanField(default=0) 
    status           = models.BooleanField(default=1)
    
    def __str__(self):
        return self.writter_name_bangla

    class Meta:
        db_table = 'book_writter_list'
        verbose_name = 'Book Writter'
        verbose_name_plural = 'Book Writter Entry'

class Publisher(models.Model):
    publisher_name_bangla  = models.CharField(max_length=150)
    publisher_name_english  = models.CharField(max_length=150, blank=True)
    menu_url                = models.CharField(max_length=450,blank = True)
    authorize_person        = models.CharField(max_length=150, blank = True)
    email           = models.EmailField(max_length=150, blank = True)
    publisher_code  = models.CharField(max_length=150, blank = True)
    password        = models.CharField(max_length=150, blank = True)
    mobile          = models.CharField(max_length=15, blank = True)
    mobile_optional     = models.CharField(max_length=15, blank = True)
    publisher_address   = models.TextField( blank = True)
    discount_persent = models.IntegerField(default=0)
    sales_discount   = models.IntegerField(default=0)
    publisher_logo  = models.ImageField(upload_to='images/publisher_logo', blank = True)
    publisher_cover  = models.ImageField(upload_to='images/publisher_logo', blank = True)
    web_address       = models.CharField(max_length=150, blank = True)
    facebook_link    = models.TextField( blank = True)
    status          = models.BooleanField(default=1)

    def __str__(self):
        return self.publisher_name_bangla

    class Meta:
        db_table = 'book_publisher_list'
        verbose_name = 'Book Publisher'
        verbose_name_plural = 'Publisher Entry'


class MastarSubCategory(models.Model):  
    master_category      = models.ForeignKey(MastarCategorySetup, on_delete=models.DO_NOTHING, null=True, blank=True) 
    regular_category     = models.ForeignKey(BookCategory, on_delete=models.DO_NOTHING, null=True, blank=True) 
    sub_category_bangla  = models.CharField(max_length=60, blank=True, null=True)
    sub_category_english = models.CharField(max_length=60, blank=True, null=True)
    created              = models.DateTimeField(auto_now_add=True)  
    menu_url             = models.CharField(max_length=450,blank = True) 
    Is_homepage          = models.BooleanField(default=False)
    Is_mainmenu          = models.BooleanField(default=False) 
    ordering             = models.IntegerField(default = 1000)
    status               = models.BooleanField(default=True)

    def __str__(self):
        return str(self.sub_category_bangla)

    class Meta:
        db_table = 'master_sub_category' 


class ProductBrand(models.Model):  
    brand_name          = models.CharField(max_length=60, blank=True, null=True) 
    details             = models.TextField(blank=True, null=True)
    ordering            = models.IntegerField(default=0) 
    created             = models.DateTimeField(auto_now_add=True)   
    status              = models.BooleanField(default=True)

    def __str__(self):
        return str(self.brand_name)

    class Meta:
        db_table = 'product_brand_list' 

class ProductSize(models.Model):  
    size_name           = models.CharField(max_length=60, blank=True, null=True) 
    ordering            = models.IntegerField(default=0) 
    created             = models.DateTimeField(auto_now_add=True)   
    status              = models.BooleanField(default=True)

    def __str__(self):
        return str(self.size_name)

    class Meta:
        db_table = 'product_size_list' 
 
class BookList(models.Model):    
    master_category         = models.ForeignKey(MastarCategorySetup, on_delete=models.DO_NOTHING, null=True, blank=True)
    # For Book Items
    publisher         = models.ForeignKey(Publisher, on_delete=models.DO_NOTHING, null=True, blank=True)
    book_name_bangla  = models.CharField(max_length=250, null = True)
    book_name_english = models.CharField(max_length=250, blank=True, null = True)
    slug              = models.CharField(max_length=250, blank=True, null = True)
    book_image        = models.CharField(max_length=300, blank=True, null = True) 
    country           = models.CharField(max_length=50,blank=True, null = True)
    number_of_page    = models.CharField(max_length=50,blank=True, null = True)
    cover_t = (
        ('1', 'পেপারব্যাক'),
        ('2', 'হার্ডকভার'),    
        ('3', 'NANE'),  
    )
    cover_type     = models.CharField(max_length=10, choices=cover_t, default=1)
    ISBN           = models.CharField(max_length=80,blank=True, null = True)
    edition        = models.CharField(max_length=50,blank=True, null = True)
    language       = models.CharField(max_length=100, blank=True, null = True)
    unit_price     = models.IntegerField(default=0) 
    purchase_discount   = models.CharField(max_length=15, blank=True, null = True)
    book_price     = models.CharField(max_length=15, blank=True, null = True) 
    sale_price     = models.CharField(max_length=15, blank=True, null = True)
    coupon_price   = models.IntegerField(default = 0, blank=True, null = True)
    discount       = models.CharField(max_length=15, default=0)
    total_sale     = models.IntegerField(default=0)
    quantity       = models.IntegerField(default=0)
    weight         = models.CharField(max_length=15, default=0, null = True)
    origin         = models.CharField(max_length=100, blank=True,null=True)
    external_link  = models.CharField(max_length=600, blank=True,null=True)
    pre_order_msg  = models.CharField(max_length=200, blank=True, null = True)
    book_idendity  = models.CharField(max_length=15, default=0)
    stock = (
        ('1', 'In Publisher'),
        ('2', 'In Stock'),
        ('3', 'Out of Stock'),
        ('4', 'Pre Order'),
    )
    stock_info     = models.CharField(max_length=10, choices=stock)
    add_date       = models.DateField(auto_now_add=True)
    sales_date     = models.DateField(auto_now_add=False)
    detail         = RichTextField(blank=True, null = True)
    video_link     = models.TextField(blank=True, null = True)
    is_pre_image   = models.BooleanField(default=0)
    is_package     = models.BooleanField(default=0) # is_package = 1 means Package else single book is_package = 0
    status         = models.BooleanField(default=1)
 

    def url(self):
        return os.path.join('/static/publisher_app/media/images/book_image/', os.path.basename(str(self.book_image)))
 
    def photo(self):
        return mark_safe('<img src = "{}" width="50" height = "55"/>'.format(self.url()))
  
    def __str__(self):
        return self.book_name_bangla

    class Meta:
        db_table = 'book_list'
        verbose_name = 'All Book'
        verbose_name_plural = 'Books List'


class CategoryWiseBook(models.Model):
    book_name        = models.ForeignKey(BookList, on_delete=models.DO_NOTHING, null=True )
    category_name    = models.ForeignKey(BookCategory, on_delete=models.DO_NOTHING, blank = True, null=True)
    status           = models.BooleanField(default=True)

    def __int__(self):
        return self.category_name

    class Meta:
        db_table = 'category_wise_book'
        verbose_name = 'Category Wise Book'
        verbose_name_plural = 'Category Wise Books'
 
class SubCategoryWiseBook(models.Model):
    book_name        = models.ForeignKey(BookList, on_delete=models.DO_NOTHING, null=True ) 
    subcategory_name = models.ForeignKey(MastarSubCategory, on_delete=models.DO_NOTHING, blank = True, null=True)
    status           = models.BooleanField(default=True)

    def __int__(self):
        return self.subcategory_name

    class Meta:
        db_table = 'sub_category_wise_book'
        verbose_name = 'Sub Category Wise Book'
        verbose_name_plural = 'Sub Category Wise Books'

class WritterWiseBook(models.Model):
    book_name        = models.ForeignKey(BookList, on_delete=models.DO_NOTHING, null=True)
    writter_name     = models.ForeignKey(BookWritter, on_delete=models.DO_NOTHING, blank = True, null=True)
    status           = models.BooleanField(default=True)

    
    
    class Meta:
        db_table = 'writter_wise_book'
        verbose_name = 'Writter Wise Book'
        verbose_name_plural = 'Writter Wise Books'

class TranslatorWiseBook(models.Model):
    book_name        = models.ForeignKey(BookList, on_delete=models.DO_NOTHING, null=True)
    translator_name  = models.ForeignKey(BookWritter, on_delete=models.DO_NOTHING, null=True)
    status           = models.BooleanField(default=True)
    
    def __int__(self):
        return self.translator_name
    
    class Meta:
        db_table = 'translator_wise_book'
        verbose_name = 'Translator Wise Book'
        verbose_name_plural = 'Translator Wise Books'

class EditorWiseBook(models.Model):
    book_name        = models.ForeignKey(BookList, on_delete=models.DO_NOTHING, null=True)
    editor_name      = models.ForeignKey(BookWritter, on_delete=models.DO_NOTHING, null=True)
    status           = models.BooleanField(default=True)
    
    def __int__(self):
        return self.editor_name
    
    class Meta:
        db_table = 'editor_wise_book'
        verbose_name = 'Editor Wise Book'
        verbose_name_plural = 'Editor Wise Books'

class AddToCart(models.Model):
    book_name   = models.ForeignKey(BookList, on_delete=models.DO_NOTHING, null=True)
    qt_price    = models.IntegerField(default = 0)
    book_price  = models.IntegerField(default = 0)
    total_price  = models.IntegerField(default = 0)
    discount    = models.IntegerField(default = 0)
    quantity    = models.IntegerField(default = 1)
    add_date    = models.DateTimeField(auto_now_add = True)
    session_key = models.CharField(max_length=230) 

    def __str__(self):
        return str(self.book_name)
    
    class Meta:
        db_table = 'add_to_cart'
        verbose_name = 'AddTo Cart'
        verbose_name_plural = 'AddToCart List'


class AddToWishlist(models.Model):
    book_name   = models.ForeignKey(BookList, on_delete=models.DO_NOTHING, null=True)
    qt_price    = models.IntegerField(default = 0)
    book_price  = models.IntegerField(default = 0)
    total_price  = models.IntegerField(default = 0)
    discount    = models.IntegerField(default = 0)
    quantity    = models.IntegerField(default = 1)
    add_date    = models.DateTimeField(auto_now_add = True)
    session_key = models.CharField(max_length=230)
    def __str__(self):
        return str(self.book_name)
    
    class Meta:
        db_table = 'add_to_wishlist'
        verbose_name = 'AddTo Wishlist'
        verbose_name_plural = 'Add Wish List'
 
class PreviewImages(models.Model):
    book_name_id  = models.IntegerField(default=0)
    ISBN          = models.CharField(max_length=30)
    images        = models.FileField(upload_to='images/preview_images', blank = True)
    
    def url(self):
        return os.path.join('/static/publisher_app/media/images/preview_images/', os.path.basename(str(self.images)))

    def picture(self):
        return mark_safe('<img src = "{}" width="50" height = "55"/>'.format(self.url()))

    def __int__(self):
        return self.book_name

    class Meta: 
        db_table = 'preview_images'

class PreviewPdfFile(models.Model):
    book_name       = models.ForeignKey(BookList, on_delete=models.DO_NOTHING, null=True) 
    pdf_file        = models.CharField(max_length=260, blank = True, null=True)
    created         = models.DateTimeField(auto_now_add = True, blank = True, null=True)
 
    def __int__(self):
        return self.book_name

    class Meta: 
        db_table = 'preview_pdf_file'
 
class DistrictEntry(models.Model):
    district_name_bangla  = models.CharField(max_length=230)
    district_name_english  = models.CharField(max_length=230)
    ordering       = models.IntegerField(default=0)
    add_date    = models.DateTimeField(auto_now_add = True)
    status         = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.district_name_bangla)

    class Meta:
        db_table = 'district_list'

class UpozillaEntry(models.Model):
    district_name  = models.ForeignKey(DistrictEntry, on_delete=models.DO_NOTHING, null=True)
    upozilla_name_bangla   = models.CharField(max_length=230)
    upozilla_name_english  = models.CharField(max_length=230)
    add_date       = models.DateTimeField(auto_now_add = True)
    status         = models.BooleanField(default=1)

    def __str__(self):
        return str(self.upozilla_name_bangla)
        
    class Meta:
        db_table = 'upozilla_list'

class PostOfficeInfo(models.Model):
    upozilla_name  = models.ForeignKey(UpozillaEntry, on_delete=models.DO_NOTHING, null=True)
    post_office_bangla    = models.CharField(max_length=230)
    post_office_english    = models.CharField(max_length=230)
    post_code      = models.CharField(max_length=230)
    add_date       = models.DateTimeField(auto_now_add = True)
    status         = models.BooleanField(default=1)

    def __str__(self):
        return str(self.post_office_bangla)
        
    class Meta:
        db_table = 'post_office_list'
 
class UserRegistration(models.Model):
    first_name  = models.CharField(max_length=65, blank = True)
    last_name   = models.CharField(max_length=65, blank = True)
    full_name   = models.CharField(max_length=130, blank = True)
    email       = models.CharField(max_length=130, blank = True)
    mobile      = models.CharField(max_length=50, blank = True)
    mobile2     = models.CharField(max_length=50, blank = True)
    designation = models.CharField(max_length=60, blank = True)
    photo       = models.FileField(upload_to='images/user_progile', blank = True)    
    select_type = (
        ('1', 'Admin Dashboard'),
        ('2', 'Collector Dashboard'),
        ('3', 'Delivery Dashboard'),
    )
    user_type   = models.CharField(max_length=2, choices = select_type)
    username    = models.CharField(max_length=65 )
    password    = models.CharField(max_length=65 )
    create_date = models.DateTimeField(auto_now_add = True)
    status      = models.BooleanField(default=True)
    
    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'user_list'
        verbose_name = 'User Registration'
        verbose_name_plural = 'User Registration List'
 


class MenuList(models.Model):
    menu_name   = models.CharField(max_length=50)
    menu_url    = models.CharField(max_length=90)
    module_types = (
        ('HR', 'HR'),
        ('Attendance', 'Attendance'),
        ('Leave', 'Leave'),
        ('Payroll', 'Payroll'), 
        ('Ecommerce', 'Ecommerce'), 
    )
    module_name      = models.CharField(max_length=50, choices=module_types)
    module_order     = models.IntegerField(default=0)
    menu_order       = models.IntegerField(default=0)
    menu_icon        = models.CharField(max_length=50,blank=True)
    background_color = models.CharField(max_length=30,blank=True)
    font_color       = models.CharField(max_length=30,blank=True)
    is_dashboard     = models.BooleanField(default=False)
    created_by       = models.ForeignKey(UserRegistration, on_delete = models.DO_NOTHING, blank=True, null=True)
    modified_by      = models.IntegerField(blank=True, null=True)
    created          = models.DateTimeField(auto_now_add=True, null=True)
    modified         = models.DateTimeField(auto_now=True, null=True)
    status           = models.BooleanField(default=True)

    def __str__(self):
        return self.menu_name

    class Meta:
        db_table = 'menu_list'
        verbose_name = "Menu"
        verbose_name_plural = "Menu List"  


class UserAccessControl(models.Model):
    user            = models.ForeignKey(UserRegistration, on_delete = models.DO_NOTHING, null=True) 
    menu            = models.ForeignKey(MenuList, on_delete = models.DO_NOTHING, null=True)
    view_action     = models.BooleanField(default=0)      
    insert_action   = models.BooleanField(default=0)      
    update_action   = models.BooleanField(default=0)      
    delete_action   = models.BooleanField(default=0)   
    permission_date = models.DateTimeField(auto_now_add=True)
    permitted_by    = models.BigIntegerField(default=0)
    insert_date     = models.DateTimeField(auto_now_add=True)
    last_update     = models.DateTimeField(auto_now=True)
    insert_by       = models.IntegerField(default=0)
    update_by       = models.IntegerField(default=0) 
    status          = models.BooleanField(default=True)   
    
    def __str__(self):
        return str(self.user)   
        
    class Meta:
        db_table = 'user_access_control'
        verbose_name = "Access Control"
        verbose_name_plural = "User Access Control"                
 

class CustomarAccount(models.Model):
    customer_name = models.CharField(max_length=30)
    mobile        = models.CharField(max_length=15)
    optional_mobile = models.CharField(max_length=15, blank = True)
    email         = models.CharField(max_length=170, blank=True, null = True)
    user_name     = models.CharField(max_length=100, blank=True)
    password      = models.CharField(max_length=100)
    login_otp     = models.IntegerField(blank=True, null = True)
    reg_date      = models.DateTimeField(auto_now_add=True)
    address       = models.TextField(blank=True)
    profile_images  = models.ImageField(upload_to='images/customer_images', blank = True)  
    is_guest        = models.BooleanField(default=1)
    customer_level  = models.CharField(max_length=55, blank=True, null=True) 
    total_point     = models.DecimalField(max_digits=30, decimal_places=6, default=0)
    used_point      = models.DecimalField(max_digits=30, decimal_places=6, default=0)
    available_point = models.DecimalField(max_digits=30, decimal_places=6, default=0)
    created         = models.DateTimeField(auto_now_add=True, null=True)
    status          = models.BooleanField(default=1)

    def __str__(self):
        return self.customer_name

    class Meta:
        db_table = 'customer_list'
    

class GatewayePayment(models.Model):  
    customer        = models.ForeignKey(CustomarAccount, on_delete=models.DO_NOTHING, blank = True, null=True) 
    bank_id         = models.CharField(max_length=100,blank = True, null=True)    
    payment_type    = models.CharField(max_length=100,blank = True, null=True)    
    amount          = models.IntegerField(default=0)   
    transaction_id  = models.CharField(max_length=100,blank = True, null=True)
    created         = models.DateTimeField(auto_now_add=True, null=True)
    order_number    = models.IntegerField(default=0)
    status          = models.BooleanField(default=1)

    def __str__(self):
        return self.customer

    class Meta:
        db_table = 'gatewaye_payment_list'

 
class PackageList(models.Model): 
    bangla_name                = models.CharField(max_length=230) 
    english_name               = models.CharField(max_length=230) 
    product                    = models.ForeignKey(BookList, on_delete = models.DO_NOTHING, null=True)
    unit_price                 = models.IntegerField(default = 0)
    sale_price                 = models.IntegerField(default = 0)
    discount_percent           = models.IntegerField(default = 0)
    package_image              = models.CharField(max_length=300, blank=True, null = True)  
    cover_t = (
        ('1', 'পেপারব্যাক'),
        ('2', 'হার্ডকভার'),    
    )
    cover_type                 = models.CharField(max_length=10, choices=cover_t, default=1)
    details                    = RichTextField(blank=True, null=True)
    video_link                 = models.TextField(blank=True,null=True)
    total_sale                 = models.IntegerField(default = 0)  
    is_book_package            = models.BooleanField(default = 0)  
    status                     = models.BooleanField(default=1) 
    created                    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bangla_name

    class Meta:
        db_table = 'package_list'

class CourierService(models.Model): 
    courier_name    = models.CharField(max_length=60, blank=True, null = True)
    courier_address = models.TextField(blank=True, null = True)
    ordering        = models.IntegerField(default=0)
    status          = models.BooleanField(default=1) 

    def __str__(self):
        return self.courier_name

    class Meta:
        db_table = 'courier_service_list'

class SalesOrder(models.Model): 
    order_number     = models.IntegerField(default=0)
    customer_name    = models.ForeignKey(CustomarAccount, on_delete=models.DO_NOTHING, blank = True, null=True) 
    delivery_per_name    = models.CharField(max_length=180)
    customer_mobile = models.CharField(max_length=15)
    optional_number = models.CharField(max_length=15, blank = True)
    customer_email  = models.EmailField(max_length=150, blank = True)
    shipping_address  = models.CharField(max_length=20000) 
    total_amount     = models.IntegerField(default=0)
    vat_amount     = models.IntegerField(default=0)
    discount_amount     = models.IntegerField(default=0)
    less_amount      = models.IntegerField(default=0)
    due_amount      = models.IntegerField(default=0) 
    shipping_charge  = models.IntegerField(default=0)
    service_charge   = models.IntegerField(default=0)
    service_code   = models.IntegerField(default=0)
    grand_total      = models.IntegerField(default=0)
    payment_type_choose = (
        ('1', 'COD'),
        ('2', 'Bkash'),
        ('3', 'Rocket'),
        ('4', 'Nagad'),
        ('5', 'AamarPay'),
    )
    payment_method  = models.CharField(max_length=1, choices=payment_type_choose, default=1) 
    delivery_method = models.ForeignKey(CourierService, on_delete=models.DO_NOTHING, blank = True, null=True)
    payment_status_choose = (
        ('1', 'Pending'),
        ('2', 'Unpaid'),
        ('3', 'Paid'),
        ('4', 'Refund'),
    )
    payment_status  = models.CharField(max_length=1, choices=payment_status_choose, default=1)
    order_status_choose = (
        ('1', 'Pending'),
        ('2', 'Confirmed'),
        ('3', 'Packed'),
        ('4', 'Shipping'),
        ('5', 'Delivered'),
        ('6', 'Returned'),
        ('7', 'Canceled'),
        ('8', 'Hold'),
    )
    order_status  = models.CharField(max_length=1, choices=order_status_choose, default=1)
    district       = models.ForeignKey(DistrictEntry, on_delete=models.DO_NOTHING, null=True, blank=True)
    upozilla       = models.ForeignKey(UpozillaEntry, on_delete=models.DO_NOTHING, null=True, blank=True)
    postal_code    = models.ForeignKey(PostOfficeInfo, on_delete=models.DO_NOTHING, null=True, blank=True)
    session_key      = models.CharField(max_length=230)
    order_date       = models.DateTimeField(auto_now_add=True)
    update_date      = models.DateTimeField(auto_now_add=False, null = True)
    order_remarks    = models.TextField(blank=True,null=True)
    status           = models.BooleanField(default=1)

    def __int__(self):
        return self.order_number

    class Meta:
        db_table = 'sales_order'
        verbose_name = 'Sales Order'
        verbose_name_plural = 'Sales Orders'


class SalesDetails(models.Model):
    order_number    = models.IntegerField(default=0)  
    book_name       = models.ForeignKey(BookList, on_delete=models.DO_NOTHING, blank = True, null=True) 
    book_price      = models.IntegerField(default=0)
    sale_price      = models.IntegerField(default=0)
    book_quantity   = models.IntegerField(default=1)
    order_date      = models.DateTimeField(auto_now_add=True)
    update_date     = models.DateTimeField(auto_now_add=False, blank = True, null=True) 
    is_guest        = models.IntegerField(default=1)
    session_key     = models.CharField(max_length=230, blank = True, null=True) 
    remarks         = models.TextField(blank = True)
    status          = models.BooleanField(default=1) 
    def __int__(self):
        return self.order_number

    class Meta:
        db_table = 'sales_details'
        verbose_name = 'Sales Detail'
        verbose_name_plural = 'Sales Details'
 
 
class SalesOrderPaymentDetails(models.Model):
    sales_order       = models.ForeignKey(SalesOrder, on_delete=models.DO_NOTHING, null=True, blank=True)
    order_number      = models.IntegerField(default=0) 
    payment_type_choose = (
        ('1', 'COD'),
        ('2', 'Bkash'),
        ('3', 'Rocket'),
        ('4', 'Nagad'),
        ('5', 'AamarPay'),
    )
    payment_method  = models.CharField(max_length=1, choices=payment_type_choose, default=1)
    payment_status_choose= (
        ('1', 'Partial'),
        ('2', 'Full'),
        ('3', 'Due'),
        ('4', 'Free'),
    )
    payment_status  = models.CharField(max_length=1, choices=payment_status_choose, default=1)
    account_number      = models.IntegerField(default=0)
    payment_amount      = models.IntegerField(default=0)
    txt_number          = models.CharField(max_length=50,blank=True,null=True)
    create_date     = models.DateTimeField(auto_now_add = True)
    update_date     = models.DateTimeField(auto_now_add = True)
    status          = models.BooleanField(default=True)
    
    def __str__(self):
        return self.order_number

    class Meta:
        db_table = 'sales_order_payment_details'
        verbose_name = 'Sales Order Payment Detail'
        verbose_name_plural = 'Sales Order Payment Details'


class ProductOffer(models.Model):
    offer_title    = models.CharField(max_length=230)
    link           = models.TextField(blank=True)
    offer_details  = models.TextField(blank=True)
    create_date    = models.DateTimeField(auto_now_add = True)
    insert_by      = models.ForeignKey(CustomarAccount, on_delete=models.DO_NOTHING, null=True, blank=True)
    status         = models.BooleanField(default=False)
    
    def __str__(self):
        return self.offer_title

    class Meta:
        db_table = 'product_offers'
        verbose_name = 'Product Offer'
        verbose_name_plural = 'Product Offer List'
         
class ClientReview(models.Model):
    book_name       = models.ForeignKey(BookList, on_delete=models.DO_NOTHING, null=True, blank=True)
    client_name     = models.ForeignKey(CustomarAccount, on_delete=models.DO_NOTHING, null=True, blank=True)
    message         = models.TextField(blank = True)
    rating_count    = models.IntegerField(default = 0)
    total_like      = models.IntegerField(default = 0)
    total_dislike   = models.IntegerField(default = 0) 
    create_date     = models.DateTimeField(auto_now_add = True)
    status          = models.BooleanField(default=True)
    
    def __str__(self):
        return self.client_name

    class Meta:
        db_table = 'client_review_list'
        verbose_name = 'Client Review'
        verbose_name_plural = 'Client Review list'
   

#-------------- Blog Models --------------------#  
class BlogMaster(models.Model): 
    blog_title          = models.CharField(max_length=256, blank=True, null=True) 
    blog_title_english  = models.CharField(max_length=256, blank=True, null=True)
    blog_url            = models.CharField(max_length=256, blank=True, null=True)
    category            = models.ForeignKey(BookCategory, on_delete=models.DO_NOTHING, blank=True, null=True)
    blog_image          = models.ImageField(upload_to='images/blog_image', blank=True, null=True)
    blog_details        = RichTextField(blank = True, null=True)
    meta_keyword        = models.TextField(blank = True, null=True)
    meta_description    = models.TextField(blank = True, null=True)
    create_date         = models.DateTimeField(auto_now_add = True)
    created_by          = models.ForeignKey(UserRegistration, on_delete=models.DO_NOTHING, blank=True, null=True)
    total_like          = models.IntegerField(default=0) 
    total_view          = models.IntegerField(default=0) 
    total_comments      = models.IntegerField(default=0) 
    status              = models.BooleanField(default=True)  

    def __str__(self):
        return self.blog_title

    class Meta:
        db_table = 'blog_list'
        verbose_name = "Blog List"
        verbose_name_plural = "Blog Lists"

class BlogComment(models.Model): 
    blog            = models.ForeignKey(BlogMaster, on_delete=models.DO_NOTHING, blank=True, null=True)  
    user_name       = models.CharField(max_length=60, blank=True, null = True)
    user_mobile     = models.CharField(max_length=60, blank=True, null = True)
    user_email      = models.EmailField(max_length=60, blank=True, null = True) 
    user_comments   = RichTextField(blank = True, null=True)
    create_date     = models.DateTimeField(auto_now_add = True) 
    status          = models.BooleanField(default=True) 

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = 'blog_wise_comments'
        verbose_name = "Blog Comment"
        verbose_name_plural = "Blog Comment List"

class ProductCategory(models.Model): 
    category_name       = models.CharField(max_length=100, blank=True, null = True) 
    create_date     = models.DateTimeField(auto_now_add = True) 
    status          = models.BooleanField(default=True) 

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = 'product_category_list'
        verbose_name = "Product Category"
        verbose_name_plural = "Product Category List"

class ProductSubCategory(models.Model): 
    sub_category_name   = models.CharField(max_length=100, blank=True, null = True) 
    category            = models.ForeignKey(ProductCategory, on_delete=models.DO_NOTHING, blank=True, null=True)  
    create_date         = models.DateTimeField(auto_now_add = True) 
    status              = models.BooleanField(default=True) 

    def __str__(self):
        return self.sub_category_name

    class Meta:
        db_table = 'product_sub_category_list'
        verbose_name = "Product Sub Category"
        verbose_name_plural = "Product Sub Category List"

class ProductList(models.Model): 
    p_type= (
        ('1', 'Book'),
        ('2', 'Other'), 
    )
    product_type            = models.CharField(max_length=1, choices=p_type, default=1)
    product_name_bangla     = models.CharField(max_length=256, blank=True, null = True)
    product_name_english    = models.CharField(max_length=256, blank=True, null = True) 
    origin                  = models.CharField(max_length=256, blank=True, null = True) 
    product_url             = models.CharField(max_length=256, blank=True, null = True) 
       
    book_name               = models.ForeignKey(BookList, on_delete=models.DO_NOTHING, blank=True, null=True)  
     
    mrp_price               = models.FloatField(default=0, blank=True, null = True) 
    unit_price              = models.FloatField(default=0, blank=True, null = True) 
    sale_price              = models.FloatField(default=0, blank=True, null = True) 
    qty                     = models.FloatField(default=0, blank=True, null = True) 
    purchase_discount       = models.FloatField(default=0, blank=True, null = True) 
    sale_discount           = models.FloatField(default=0, blank=True, null = True) 
    
    details         = RichTextField(blank = True, null=True)
    video_link      = models.TextField(blank=True,null=True)
    product_image   = models.CharField(max_length=256,blank = True, null=True)
    
    cover_t = (
        ('1', 'পেপারব্যাক'),
        ('2', 'হার্ডকভার'),    
        ('3', 'NANE'),  
    )
    cover_type      = models.CharField(max_length=10, choices=cover_t, null=True)
    stock_info      = models.CharField(max_length=56,blank = True, null=True) 
    edition         = models.CharField(max_length=56,blank = True, null=True)
    weight          = models.CharField(max_length=56,blank = True, null=True)
    language        = models.CharField(max_length=56,blank = True, null=True)
    number_of_page  = models.CharField(max_length=56,blank = True, null=True)
    country         = models.CharField(max_length=56,blank = True, null=True)
    ISBN            = models.CharField(max_length=56,blank = True, null=True)
    is_preview_img  = models.CharField(max_length=56,blank = True, null=True) 
    publisher       = models.ForeignKey(Publisher, on_delete=models.DO_NOTHING, blank=True, null=True)  
    
    category        = models.ForeignKey(ProductCategory, on_delete=models.DO_NOTHING, blank=True, null=True)  
    sub_category    = models.ForeignKey(ProductSubCategory, on_delete=models.DO_NOTHING, blank=True, null=True)  
 
    create_date     = models.DateTimeField(auto_now_add = True) 
    status          = models.BooleanField(default=True) 

    def __str__(self):
        return self.product_name_bangla

    class Meta:
        db_table = 'product_list'
        verbose_name = "Product List" 

 
