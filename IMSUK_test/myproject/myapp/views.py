from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import MenuItem
from django.db.models import Q

# ✅ 1. Home Page (FBV)
def home(request):
    return render(request, 'myapp/home.html')

# ✅ 2. เมนูอาหารทั้งหมด + ค้นหา (CBV: ListView)
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

# ✅ 3. รายละเอียดอาหาร (CBV: DetailView)
class MenuItemDetailView(DetailView):
    model = MenuItem
    template_name = 'myapp/menu_detail.html'
    context_object_name = 'menu_item'

#เพิ่มมา
from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# 🛒 เพิ่มลงตะกร้า
@login_required
def add_to_cart(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        menu_item=menu_item,
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'เพิ่ม {menu_item.name} ลงในรถเข็นแล้ว')
    return redirect('menu_list')  # หรือ redirect ไปยัง menu_detail

# 🛒 แสดงรถเข็นสินค้า
@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.menu_item.price * item.quantity for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'myapp/cart.html', context)

# 🗑 ลบออกจากรถเข็น
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    messages.info(request, f'ลบ {cart_item.menu_item.name} ออกจากรถเข็นแล้ว')
    return redirect('view_cart')


