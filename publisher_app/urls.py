from unicodedata import name
from django.urls import path
from . import views
from . import customer_views
from . import order_views

urlpatterns = [ 
    path('', views.index_page, name="index_page"),
    path('contact-us/', views.contact_page, name="contact_page"),
    path('about-us/', views.about_us, name="about_us"),
    path('complain/', views.complain_page, name="complain_page"),
    path('refund-policy/', views.refund_policy, name="refund_policy"),
    path('terms-of-service/', views.terms_and_service, name="terms_and_service"),
    path('book/<int:id>/<str:slug>/', views.book_details, name="book_details"),
    path('my-cart/', views.add_to_cart_page),
    path('cart/delete-item/', views.delete_to_cart),
    path('quick-login/', views.quick_login),
    path('checkout/', views.checkout_order),  
    path('checkout-order-now/<int:id>/<str:qty>/', views.checkout_order_now),
    path('order-success/', views.customer_order_success), 
    path('bind-upozilla-wise-post-office/', views.bind_upozilla_wise_postoffice), 
    path('category-wise-subcategory/', views.category_wise_subcategory), 
    path('book/categories/', views.all_book_category_list),
    path('book/writter-list/', views.all_book_writter_list),
    path('book/pulisher-list/', views.all_book_publisher_list),
    path('book-search/', views.bind_book_search), 
    path('writter-search/', views.bind_writter_search), 
    path('category-search/', views.bind_category_search), 
    path('publisher-search/', views.bind_publisher_search),
    path('book/author/<int:id>/<str:menu_url>/',views.author_pages),  
    path('book/category/<int:id>/<str:menu_url>/', views.category_book_list), 
    path('book/subcategory/<int:id>/<str:menu_url>/', views.subcategoryWiseBookList), 
    path('book/newPpublishedBook/<int:id>/', views.category_wise_new_publication), 
    path('book/bestSallerBook/<int:id>/', views.category_wise_best_saller_book_list), 
    path('book/LastWeekBestWritter/<int:id>/', views.category_wise_last_week_best_writter_book), 
    path('book/publisher/<int:id>/<str:menu_url>/', views.publisher_wise_page),
    path('customer/login/off/', views.customer_login),
    path('customer/login/', views.customer_login2),
    path('customer/forgot-password/', views.customer_forgot_password),
    path('customer/reset-password/', views.customer_reset_password),
    path('customer/registration/', views.customer_registration),
    path('logout/', views.user_logout),  
    path('login_for_review/', views.login_for_review), 
    path('cusotmer/client-review/', views.client_review_message), 
    path('loadPublisherWiseBook/', views.loadPublisherWiseBook), 
    path('loadCartItemByAjax/', views.loadCartItemByAjax, name="loadCartItemByAjax"), 
    path('deleteCartItemByAjax/', views.deleteCartItemByAjax, name="deleteCartItemByAjax"), 
    path('bookSearch/', views.AdvanceBookSearch, name="AdvanceBookSearch"), 
    path('addToWishList/', views.addToWishList, name="addToWishList"), 
    path('wishlist-item/', views.wishList_cart_item, name="wishList_cart_item"), 
    path('category/<int:category_id>/all-subcategory/', views.category_wise_all_subcategory, name="category_wise_all_subcategory"), 
     
    path('ajaxQuantityUpDown/', views.ajaxQuantityUpDown, name="ajaxQuantityUpDown"), 
    path('confirm-otp/', views.confirm_otp, name="confirm_otp"),   
    path('get-load-publisher-list/', views.get_load_publisher_list, name="get_load_publisher_list"),   


    # Bkash API Payment 
    # path('ajaxQuantityUpDown/', views.ajaxQuantityUpDown, name="ajaxQuantityUpDown"), 


    # Customer Panel
    path('my-account/', customer_views.my_account),
    path('cart-items/', customer_views.my_cart_items),
    path('my-wishlist/', customer_views.my_wishlist_items),
    path('wishlist/<int:book_name>/delete/', customer_views.my_wishlist_items_delete),
    path('myorder/order-list/', customer_views.my_order_list),
    path('myorder/<int:order_number>/view/', customer_views.my_order_view),
    path('cl/profile/<int:id>/update/', customer_views.customer_profile_update),
  

    #####################  Dashboard Url ##############################
    path('admin-dashboard', views.admin_dashboard, name="admin_dashboard"),
    path('adminlogin/', views.admin_login, name="admin_login"),
    path('adminlogout', views.admin_logout, name="admin_logout"),
    path('accessDeny', views.accessDeny, name="accessDeny"),
    
    path('dashboard/bookWisePreviewImageClear/', views.bookWisePreviewImageClear), 
    # path('dashboard/bookWisePreviewImageClear/', views.book_search_page), 

    #####  Settings Url ###
    path('settings-dashboard/', views.settings_dashboard, name="settings_dashboard"),
    path('user-access-control/', views.user_access_control, name="user_access_control"),
    path('book-category-entry/', views.book_category_add, name="Book_category_add"),
    path('NewBookCategoryEntry/', views.NewBookCategoryEntry, name="NewBookCategoryEntry"),
    path('book-category-update/<int:id>/', views.book_category_update, name="book_category_update"),
    path('book-category-list/', views.book_category_list, name="book_category_list"),

    path('book-author-entry/', views.book_author_add, name="book_author_add"),
    path('NewBookWriterEntry/', views.NewBookWriterEntry, name="NewBookWriterEntry"),
    path('book-author-update/<int:id>/', views.book_author_update, name="book_author_update"),
    path('book-author-delete/<int:id>/', views.book_author_delete, name="book_author_update"),
    path('book-author-list/', views.book_author_list, name="book_author_list"),
    # path('book-category-list/', views.book_category_list, name="book_category_list"),

    path('book-publisher-entry/', views.book_publisher_add, name="book_publisher_add"),
    path('book-publisher-update/<int:id>/', views.book_publisher_update, name="book_publisher_update"),
    path('book-publisher-list/', views.book_publisher_list, name="book_publisher_list"),
    path('products/book/<int:id>/active/', views.dashboard_active_book_list),
    path('products/book/<int:id>/in-active/', views.dashboard_in_active_book_list),

    path('settings/district-add/', views.dashboard_district_add),
    path('settings/upozilla-add/', views.dashboard_upozilla_add),
    path('settings/upozilla-list/', views.dashboard_upozilla_list),
    path('settings/district-list/', views.dashboard_district_list),
    path('settings/post-office-add/', views.dashboard_post_office_add),
    path('settings/post-office-list/', views.dashboard_post_office_list), 
    path('bind-district-upozilla/', views.dashboard_bind_district_wise_upozilla), 
    path('settings/menu-add/', views.menu_add, name="menu_add"), 
    path('settings/menu-list/', views.menu_list, name="menu_list"), 
    path('settings/sliderAdd/', views.sliderAdd, name="sliderAdd"), 
    path('settings/sliderList/', views.sliderList, name="sliderList"), 
    path('settings/<int:id>/sliderEdit/', views.sliderEdit, name="sliderEdit"), 
    

    ########  Product Urls ###########
    path('products/add-new-book/', views.add_new_book, name="add_new_book"),
    path('products/add-new-product/', views.add_new_product, name="add_new_product"),
    path('products/product-list/', views.product_list, name="product_list"),
    path('products/add-package-book/', views.add_package_book, name="add_package_book"),
    path('products/book-list/', views.book_list, name="book_list"),
    path('products/book/<int:id>/update-book/', views.dashboard_update_book_item),


    path('api/bookListApi', views.bookListApi, name="bookListApi"), 

    ############### Order Dashboard Urls ############### 
    path('dashboard/orders/all-order/', order_views.all_order_dashboard),
    path('dashboard/orders/pending-orders/', order_views.pending_order_list),
    path('dashboard/orders/confirmed-orders/', order_views.dashboard_confirm_order_list),
    path('dashboard/orders/packed-orders/', order_views.dashboard_packed_order_list),
    path('dashboard/orders/shipping-orders/', order_views.dashboard_shipping_order_list),
    path('dashboard/orders/delivery-orders/', order_views.dashboard_delivery_order_list),
    path('dashboard/orders/returned-orders/', order_views.dashboard_returned_order_list),
    path('dashboard/orders/canceled-orders/', order_views.dashboard_canceled_order_list),
    path('dashboard/orders/hold-orders/', order_views.dashboard_hold_order_list), 
    path('dashboard-orders-details/<str:order_number>/', order_views.dashboard_order_items_views), 
    path('dashboard/orderWiseView/<str:order_number>/', order_views.orderWiseView), 
    path('dashboardOrderPrint', order_views.dashboardOrderPrint), 
    path('dashboard/order/customize/', order_views.dashboard_customize_order_add),
    path('dashboard/UpdateOrder/', order_views.UpdateOrder), 
    path('dashboard/order/edit/', order_views.dashboard_update_order, name="dashboard_update_order"),

    path('dashboard/bind-district-upozilla/', order_views.dashboard_bind_district_wise_upozilla),  
    path('dashboard/bind-upozilla-wise-post-office/', order_views.dashboard_bind_upozilla_wise_post),  
    path('dashboard/orders/<int:id>/delete/', order_views.dashboard_customize_order_delete), 
    path('dashboard/incrementDecrementQuantity/', order_views.incrementDecrementQuantity), 

    # Sales Reports 
    path('dashboard/sales/sales-history/', order_views.dashboard_sales_history), 
    path('dashboard/customerList/', order_views.dashboardCustomerList), 
    path('dashboard/ExportSalesList/', order_views.ExportSalesList), 
    
    #blog POSt List
    path('ahsan-blog/', views.ahsan_blog),
    path('ahsan-blog/<int:id>/<str:blog_url>/', views.ahsan_blog_details),
    path('BlogPostViewByAjax/', views.BlogPostViewByAjax),
    path('CategoryWiseBlogList/<int:category_id>/<str:menu_url>/', views.CategoryWiseBlogList),

    path('dashboard/blog/add-new-blog/', order_views.dashboard_add_new_blog),
    path('dashboard/blog/blog-list/', order_views.dashboard_blog_list),
    path('dashboard/blog/<int:id>/update/', order_views.dashboard_blog_update),
    path('dashboard/blog/<int:id>/blog-delete/', order_views.dashboard_blog_delete),

    path('master-category-list/', order_views.master_category_list),
    path('master-category-add/', order_views.master_category_add),
    path('master-category/<int:id>/edit/', order_views.master_category_update),
    path('master-subcategory-list/', order_views.master_subcategory_list),
    path('master-subcategory-add/', order_views.master_subcategory_add), 
    path('master-subcategory/<int:id>/edit/', order_views.master_subcategory_update), 
    path('master-subcategory/<int:id>/delete/', order_views.master_subcategory_delete), 
    path('payment-success/<str:order_number>/<str:session_key>/', order_views.payment_success), 
    path('payment-cancel/<str:order_number>/<str:session_key>/', order_views.payment_cancel), 
    path('payment-failed/<str:order_number>/<str:session_key>/', order_views.payment_failed), 
    path('importSubcategory/', order_views.importSubcategory), 
    path('importcategorywisebook/', order_views.importcategorywisebook), 
    path('importsubcategorywisebook/', order_views.importsubcategorywisebook), 
    
]
