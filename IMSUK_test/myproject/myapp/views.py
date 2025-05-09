from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib import messages

from .models import MenuItem, CartItem

# ✅ หน้าแรก
def home(request):
    return render(request, 'myapp/home.html')

# ✅ เมนูทั้งหมด + Search
class MenuListView(ListView):
    model = MenuItem
    template_name = 'myapp/menu_list.html'
    context_object_name = 'menu_items'

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_available=True).order_by('-price')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        return queryset

# ✅ รายละเอียดเมนู
class MenuItemDetailView(DetailView):
    model = MenuItem
    template_name = 'myapp/menu_detail.html'
    context_object_name = 'menu_item'

# ✅ ฟังก์ชัน session_key สำหรับ cart แบบไม่ต้อง login
def get_or_create_session_key(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key

# 🛒 เพิ่มอาหารลงรถเข็น
def add_to_cart(request, menu_item_id):
    session_key = get_or_create_session_key(request)
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)

    cart_item, created = CartItem.objects.get_or_create(
        session_key=session_key,
        menu_item=menu_item,
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'เพิ่ม {menu_item.name} ลงในรถเข็นแล้ว')
    return redirect('menu_list')

# 🛒 แสดงรถเข็น
def view_cart(request):
    session_key = get_or_create_session_key(request)
    cart_items = CartItem.objects.filter(session_key=session_key)
    total_price = sum(item.menu_item.price * item.quantity for item in cart_items)
    return render(request, 'myapp/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

# 🗑 ลบเมนูออกจากรถเข็น
def remove_from_cart(request, item_id):
    session_key = get_or_create_session_key(request)
    cart_item = get_object_or_404(CartItem, id=item_id, session_key=session_key)
    cart_item.delete()
    messages.info(request, f'ลบ {cart_item.menu_item.name} ออกจากรถเข็นแล้ว')
    return redirect('view_cart')

from .models import Order, OrderItem

def place_order(request):
    session_key = get_or_create_session_key(request)
    cart_items = CartItem.objects.filter(session_key=session_key)

    if not cart_items.exists():
        messages.warning(request, "รถเข็นของคุณว่างเปล่า")
        return redirect('view_cart')

    # 🔸 สร้าง Order
    order = Order.objects.create(session_key=session_key)

    # 🔸 บันทึกรายการ OrderItem
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            menu_item=item.menu_item,
            quantity=item.quantity,
            price=item.menu_item.price
        )

    # 🔸 ล้างรถเข็น
    cart_items.delete()

    # 🔸 ไปหน้าแสดงผล
    return redirect('order_success', order_id=order.id)

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'myapp/order_success.html', {'order': order})
