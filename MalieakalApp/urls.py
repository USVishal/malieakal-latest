from django.urls import re_path,path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    #############################################################<<<<<<<<< LANDING MODULE >>>>>>>>>>>>>>>>>
    path('', views.index, name='index'),
    path('user_type', views.user_type, name='user_type'),
    path('login_main',views.login_main, name='login_main'),
    path('forgotPassword/', views.forgotPassword,name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate,name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword,name='resetPassword'),
    path('logout/', views.logout,name='logout'),
    ############################################################ <<<<<<<<< admin MODULE >>>>>>>>>>>>>>>>>
      
    path('admin_home/',views.admin_home,name='admin_home'),
    path('admin_delete_item/<int:id>/', views.admin_delete_item, name='admin_delete_item'),

    path('admin_add_item',views.admin_add_item,name='admin_add_item'),
    path('admin_edit_item/<int:item_id>',views.admin_edit_item,name='admin_edit_item'),
    path('upload_images',views.upload_images,name='upload_images'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('admin_itemlist/',views.admin_itemlist,name='admin_itemlist'),
    path('stafflist/', views.staff_list_view, name='staff_list'),

    path('staffofferlist/', views.staffofferlist, name='staffofferlist'),
    path('edit_offer/<int:id>', views.edit_offer, name='edit_offer'),
    path('delete_offer/<int:id>', views.delete_offer, name='delete_offer'),


    path('admin_category/', views.admin_category, name='admin_category'),
    path('new_form/', views.new_form, name='new_form'),
    path('staff_management/', views.staff_management, name='staff_management'), 
    path('edit_staff/<int:id>', views.edit_staff, name='edit_staff'),
    path('delete_staff/<int:id>', views.delete_staff, name='delete_staff'),
    
    ############################################################ <<<<<<<<< Staff MODULE >>>>>>>>>>>>>>>>>
  
    path('staff_home/',views.staff_home,name='staff_home'),
    path('delete/<int:id>/', views.delete_item, name='delete_item'),
    path('profile_staff_creation/',views.profile_staff_creation,name='profile_staff_creation'),
    path('new_module',views.new_module,name='new_module'),
    path('new_module_edit/<int:item_id>',views.new_module_edit,name='new_module_edit'), 
    path('staff_upload_images',views.staff_upload_images,name='staff_upload_images'),
    path('staff_itemlist',views.staff_itemlist,name='staff_itemlist'),
    path('staff_category',views.staff_category,name='staff_category'),
    path('staff_new_offer/', views.staff_new_offer, name='staff_new_offer'),

    
    ############################################################ <<<<<<<<< User MODULE >>>>>>>>>>>>>>>>>

    path('user_registration/',views.user_registration,name='user_registration'),
    path('index_user_confirmation/<int:user_id>/',views.index_user_confirmation,name='index_user_confirmation'),
    path('profile_user_creation/',views.profile_user_creation,name='profile_user_creation'),
    path('user_home/',views.user_home,name='user_home'),
    path('all_items/',views.all_items,name='all_items'),
    path('all_items_add_cart/<int:id>/<int:category>',views.all_items_add_cart,name='all_items_add_cart'),

    path('index_user_confirmation/<int:user_id>/',views.index_user_confirmation,name='index_user_confirmation'),
    path('category_items/<int:categorys>',views.category_items,name='category_items'),#--- Category item view template 
    path('under_category_items_add_cart/<int:id>/<int:categorys>',views.under_category_items_add_cart,name='under_category_items_add_cart'),

    path('under_items/<str:category>',views.under_items,name='under_items'),
    path('add_cart_pr_view/<int:id>/<int:category>',views.add_cart_pr_view,name='add_cart_pr_view'),

    path('add_cart/<int:id>/<int:category>',views.add_cart,name='add_cart'),
    path('add_cart_pr_view/<int:id>/<int:category>',views.add_cart_pr_view,name='add_cart_pr_view'),
    path('cart_view',views.cart_view,name='cart_view'),
    path('home',views.home,name='home'),#-----------------------------Cart View Template
    path('cart_checkout',views.cart_checkout,name='cart_checkout'),
    path('send_receipt',views.send_receipt,name='send_receipt'),
    path('product_view/<int:item_id>/', views.product_view, name='product_view'),
    path('delete_cart/<int:id>',views.delete_cart,name='delete_cart'),
    path('ind',views.ind,name='ind'),


    path('search_feature',views.search_feature,name='search_feature'),
    path('index_search_feature',views.index_search_feature,name='index_search_feature'),
    ]