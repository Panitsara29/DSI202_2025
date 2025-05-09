from django.urls import path
from .views import (
    home,
    MenuListView,
    MenuItemDetailView,
    add_to_cart,
    view_cart,
    remove_from_cart,
)

urlpatterns = [
    path('', home, name='home'),  # หน้าแรก
    path('menu/', MenuListView.as_view(), name='menu_list'),  # รายการเมนูทั้งหมด
    path('menu/<int:pk>/', MenuItemDetailView.as_view(), name='menu_detail'),  # รายละเอียดเมนู

    # 🛒 เส้นทางสำหรับระบบรถเข็น
    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<int:menu_item_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
]


