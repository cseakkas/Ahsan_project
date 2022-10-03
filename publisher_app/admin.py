
from django.contrib import admin
from . import models

class PublisherProfileAdmin(admin.ModelAdmin):
    list_display = ('publisher_name', 'email1', 'mobile1', 'address', 'status')
    list_filter = ('publisher_name', 'email1', 'status')
    search_fields = ('publisher_name', 'email1','mobile1')

class SliderImgAdmin(admin.ModelAdmin):
    list_display = ('slider_name','title1','upload_date','slider_order','photo','status')
    list_filter = ['status']


class BookCategoryAdmin(admin.ModelAdmin):
    list_display    = ('cat_name_bangla', 'Is_homepage', 'Is_mainmenu', 'ordering', 'status',)
    search_fields   = ('cat_name_bangla','status',)
    list_per_page = 25

class BookWritterAdmin(admin.ModelAdmin):
    list_display    = ('writter_name_bangla', 'email', 'mobile', 'status',)
    search_fields   = ('writter_name_bangla', 'email', 'mobile', 'status',)
    list_per_page = 25

class PublisherAdmin(admin.ModelAdmin):
    list_display    = ('publisher_name_bangla', 'email', 'mobile', 'discount_persent','publisher_address', 'status')
    search_fields   = ('publisher_name_bangla', 'email', 'mobile', 'status',)
    list_per_page = 25


class BookListAdmin(admin.ModelAdmin):
    list_display    = ('book_name_bangla', 'book_price', 'publisher', 'quantity', 'language', 'photo', 'status',)
    search_fields   = ('book_name_bangla', 'book_price', 'publisher', 'quantity', 'language',)
    list_per_page = 25
    date_hierarchy = 'add_date'
    ordering = ('add_date',)
   
class DistrictEntryAdmin(admin.ModelAdmin):
    list_display  = ['district_name_bangla', 'district_name_english', 'ordering', 'add_date', 'status']
    list_filter  = ['district_name_bangla', 'district_name_english', 'ordering', 'add_date', 'status']
    search_fields = ['district_name_bangla', 'add_date',]
    
    
class UpozillaEntryAdmin(admin.ModelAdmin):
    list_filter  = ['upozilla_name_bangla', 'upozilla_name_english', 'district_name', 'add_date', 'status']
    list_display  = ['upozilla_name_bangla', 'upozilla_name_english', 'district_name', 'add_date', 'status']
    search_fields = ['upozilla_name_bangla', 'district_name', 'add_date',]


class PostOfficeInfoAdmin(admin.ModelAdmin):
    list_filter  = ['post_office_bangla', 'post_office_english', 'post_code', 'upozilla_name', 'add_date', 'status']
    list_display  = ['post_office_bangla', 'post_code', 'upozilla_name', 'add_date', 'status']
    search_fields = ['post_office_bangla', 'upozilla_name', 'add_date',]
    
     
class UserRegistrationAdmin(admin.ModelAdmin):
    list_display  = ['full_name', 'user_type', 'email', 'mobile', 'designation', 'username', 'password', 'status']
    search_fields = ['full_name', 'email',]
     
     
class MenuListAdmin(admin.ModelAdmin):
    list_display  = ['menu_name', 'menu_url',  'module_order', 'status']
    search_fields = ['menu_name', 'module_types',]
     
class UserAccessControlAdmin(admin.ModelAdmin):
    list_display  = ['menu', 'user', 'view_action', 'insert_action', 'update_action', 'delete_action', 'status']
    search_fields = ['menu', 'user',]
     
class CourierServiceAdmin(admin.ModelAdmin):
    list_display  = ['courier_name', 'ordering', 'status']
    search_fields = ['courier_name', 'ordering',]

# class MastarCategorySetupAdmin(admin.ModelAdmin):
#     list_display  = ['category_name', 'category_ordering', 'created', 'status']
#     search_fields = ['category_name', 'category_ordering',]
     
# class MastarSubCategoryAdmin(admin.ModelAdmin):
#     list_display  = ['sub_category', 'category_name', 'created', 'status']
#     search_fields = ['sub_category', 'category_name',]

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display  = ['category_name', 'create_date', 'status']
    search_fields = ['category_name', 'create_date',]

class ProductSubCategoryAdmin(admin.ModelAdmin):
    list_display  = ['sub_category_name','category', 'create_date', 'status']
    search_fields = ['sub_category_name','category', 'create_date',]
     
    
admin.site.register(models.PublisherProfile, PublisherProfileAdmin)
admin.site.register(models.SliderInfo,SliderImgAdmin)
admin.site.register(models.BookCategory,BookCategoryAdmin)
admin.site.register(models.BookWritter,BookWritterAdmin)
admin.site.register(models.Publisher,PublisherAdmin)
admin.site.register(models.BookList,BookListAdmin)  
admin.site.register(models.DistrictEntry, DistrictEntryAdmin)
admin.site.register(models.UpozillaEntry, UpozillaEntryAdmin)
admin.site.register(models.PostOfficeInfo, PostOfficeInfoAdmin) 
admin.site.register(models.UserRegistration, UserRegistrationAdmin) 
admin.site.register(models.MenuList, MenuListAdmin) 
admin.site.register(models.UserAccessControl, UserAccessControlAdmin) 
# admin.site.register(models.MastarCategorySetup, MastarCategorySetupAdmin) 
# admin.site.register(models.MastarSubCategory, MastarSubCategoryAdmin) 
admin.site.register(models.CourierService, CourierServiceAdmin) 
admin.site.register(models.ProductCategory, ProductCategoryAdmin) 
admin.site.register(models.ProductSubCategory, ProductSubCategoryAdmin) 