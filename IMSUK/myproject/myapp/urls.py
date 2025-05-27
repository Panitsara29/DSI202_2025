from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import (
    home,
    MenuListView,
    add_to_cart,
    view_cart,
    remove_from_cart,
    place_order,
    order_success,
    register,
    my_orders,
    my_account,
    delete_address,
    MenuDetailView,
    submit_review, 
    notifications, 
    mark_notification_read,
    SurpriseBoxListView
)
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🌐 หน้าแรก + เมนู
    path('', home, name='home'),
    path('menu/', MenuListView.as_view(), name='menu_list'),
    path('menu/<int:pk>/', MenuDetailView.as_view(), name='menu_detail'),

    # 🛒 รถเข็นและคำสั่งซื้อ
    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<int:menu_item_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('order/place/', place_order, name='place_order'),
    path('order/success/<int:order_id>/', order_success, name='order_success'),
    path('order/<int:order_id>/upload-slip/', views.upload_payment_slip, name='upload_payment_slip'),
    path('order/<int:order_id>/review/<int:menu_item_id>/', submit_review, name='submit_review'),  # ✅ รีวิว

    path('my-orders/', my_orders, name='my_orders'),
    path('add_to_cart/<int:menu_item_id>/', views.add_to_cart, name='add_to_cart'),
    path('toggle_favorite/<int:menu_item_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_list, name='favorites'),

    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),

    # 👤 การเข้าสู่ระบบ / สมัครสมาชิก
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('my-account/', my_account, name='my_account'),
    path('delete-address/<int:address_id>/', delete_address, name='delete_address'),

    path('about/', views.about, name='about'),

    # 🔗 Google OAuth 
    path('auth/', include('social_django.urls', namespace='social')),

    path('notifications/', notifications, name='notifications'),
    path('notification/<int:notification_id>/read/', mark_notification_read, name='mark_notification_read'),
    
    path('surprise-boxes/', SurpriseBoxListView.as_view(), name='surprise_boxes'),
]
