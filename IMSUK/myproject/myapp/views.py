from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .models import MenuItem, CartItem, Order, OrderItem, Profile, DeliveryAddress, Category, Allergen, MenuReview, Notification, Coupon
from .forms import UserRegistrationForm, UserProfileForm, DeliveryAddressForm, PaymentForm, PaymentSlipForm, MenuReviewForm

from collections import defaultdict
from promptpay import qrcode as pp_qrcode
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from django.http import HttpResponseRedirect
from django.urls import reverse

from django.utils.decorators import method_decorator

# ⛑ สร้างโปรไฟล์อัตโนมัติถ้ายังไม่มี
def ensure_profile_exists(user):
    Profile.objects.get_or_create(user=user)

# ✅ หน้าแจ้งเตือน
@login_required
def notifications(request):
    notes = Notification.objects.filter(user=request.user).order_by('-created_at')
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return render(request, 'myapp/notifications.html', {'notifications': notes})


# ✅ ทำเครื่องหมายว่าอ่านแล้ว
@login_required
def mark_notification_read(request, notification_id):
    note = get_object_or_404(Notification, id=notification_id, user=request.user)
    note.is_read = True
    note.save()
    return HttpResponseRedirect(reverse('notifications'))

# หน้าแรก
def home(request):
    new_items = MenuItem.objects.filter(is_available=True).order_by('-id')[:6]
    return render(request, 'myapp/home.html', {'new_items': new_items})

# เมนูทั้งหมด + filter
class MenuListView(ListView):
    model = MenuItem
    template_name = 'myapp/menu_list.html'
    context_object_name = 'menu_items'

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_available=True, is_surprise_box=False)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
        categories = self.request.GET.getlist('category')
        if categories:
            queryset = queryset.filter(category__name__in=categories)
        allergens = self.request.GET.getlist('allergen')
        for allergen in allergens:
            queryset = queryset.exclude(allergens__name=allergen)
        sort_option = self.request.GET.get('sort')
        if sort_option == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_option == 'price_desc':
            queryset = queryset.order_by('-price')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price and max_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price), price__lte=float(max_price))
            except ValueError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all(),
            'allergens': Allergen.objects.all(),
            'selected_categories': self.request.GET.getlist('category'),
            'selected_allergens': self.request.GET.getlist('allergen'),
            'search_query': self.request.GET.get('q', ''),
            'sort_option': self.request.GET.get('sort', ''),
        })
        return context

class MenuDetailView(DetailView):
    model = MenuItem
    template_name = 'myapp/menu_detail.html'
    context_object_name = 'menu_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_item = self.get_object()
        context['related_items'] = MenuItem.objects.filter(
            restaurant=current_item.restaurant,
            is_available=True
        ).exclude(id=current_item.id)[:3]
        return context

# รถเข็น
@csrf_exempt
@login_required
def add_to_cart(request, menu_item_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quantity = int(data.get('quantity', 1))
            menu_item = get_object_or_404(MenuItem, id=menu_item_id)
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                menu_item=menu_item,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            total_qty = sum(item.quantity for item in CartItem.objects.filter(user=request.user))
            return JsonResponse({'success': True, 'cart_count': total_qty})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@login_required
def toggle_favorite(request, menu_item_id):
    item = get_object_or_404(MenuItem, id=menu_item_id)
    if request.user in item.favorited_by.all():
        item.favorited_by.remove(request.user)
        return JsonResponse({'favorited': False})
    else:
        item.favorited_by.add(request.user)
        return JsonResponse({'favorited': True})

@login_required
def favorite_list(request):
    favorites = request.user.favorite_items.all()
    return render(request, 'myapp/favorites.html', {'favorites': favorites})

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.menu_item.price * item.quantity for item in cart_items)
    return render(request, 'myapp/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    messages.info(request, f'ลบ {cart_item.menu_item.name} ออกจากรถเข็นแล้ว')
    return redirect('view_cart')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            login(request, new_user)
            messages.success(request, "สมัครสมาชิกเรียบร้อยแล้ว")
            return redirect('menu_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'myapp/register.html', {'form': form})

@login_required
def place_order(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            messages.warning(request, "รถเข็นของคุณว่างเปล่า")
            return redirect('view_cart')

        address_id = request.POST.get('address')
        if not address_id:
            messages.error(request, "กรุณาเลือกที่อยู่จัดส่ง")
            return redirect('checkout')

        delivery_address = get_object_or_404(DeliveryAddress, id=address_id, user=request.user)
        payment_form = PaymentForm(request.POST)
        if not payment_form.is_valid():
            messages.error(request, "กรุณาเลือกวิธีการชำระเงินให้ถูกต้อง")
            return redirect('checkout')

        method = payment_form.cleaned_data['payment_method']
        coupon_code = payment_form.cleaned_data.get('coupon_code')  # ✅ คูปอง
        coupon = None
        discount_percent = 0

        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, is_public=True)
                if not coupon.is_active():
                    messages.warning(request, "คูปองหมดอายุหรือยังไม่เริ่มใช้งาน")
                    return redirect('checkout')
                discount_percent = coupon.discount_percent
            except Coupon.DoesNotExist:
                messages.warning(request, "ไม่พบคูปองที่ใช้ได้")
                return redirect('checkout')

        order = Order.objects.create(
            user=request.user,
            delivery_address=delivery_address,
            payment_method=method,
            status='paid' if method != 'qr' else 'pending',
        )

        total = 0
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                menu_item=item.menu_item,
                quantity=item.quantity,
                price=item.menu_item.price
            )
            total += item.menu_item.price * item.quantity

        # ✅ คำนวณราคาหลังหักคูปอง
        if discount_percent:
            discount_amount = (total * discount_percent) / 100
            total -= discount_amount

        order.total_price = total

        # ✅ QR code
        if method == 'qr':
            qr_string = pp_qrcode.generate_payload('0971561314', amount=float(total))
            qr_image = qrcode.make(qr_string)
            buffer = BytesIO()
            qr_image.save(buffer, format='PNG')
            filename = f"qr_order_{order.id}.png"
            order.qr_image.save(filename, ContentFile(buffer.getvalue()), save=False)

        # ✅ Credit card info
        elif method == 'card':
            card_info = f"""
            หมายเลขบัตร: {payment_form.cleaned_data['card_number']}
            วันหมดอายุ: {payment_form.cleaned_data['expiry_date']}
            CVV: {payment_form.cleaned_data['cvv']}
            """
            order.payment_info = card_info

        order.save()
        cart_items.delete()

        return redirect('payment_success', order_id=order.id)

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    reviewed_pairs = MenuReview.objects.filter(user=request.user).values_list('order_id', 'menu_item_id')
    reviewed = [f"{str(order_id)}-{str(menu_id)}" for order_id, menu_id in reviewed_pairs]
    return render(request, 'myapp/my_orders.html', {
        'orders': orders,
        'reviewed': reviewed,
    })


@login_required
def my_account(request):
    ensure_profile_exists(request.user)
    profile_form = UserProfileForm(instance=request.user.profile)
    address_form = DeliveryAddressForm(user=request.user)
    addresses = DeliveryAddress.objects.filter(user=request.user)

    try:
        social_email = request.user.social_auth.get(provider='google-oauth2').uid
    except Exception:
        social_email = request.user.email

    if request.method == 'POST' and 'save_profile' in request.POST:
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('my_account')

    if request.method == 'POST' and 'save_address' in request.POST:
        address_id = request.POST.get('address_id')
        if address_id:
            address = get_object_or_404(DeliveryAddress, id=address_id, user=request.user)
            address_form = DeliveryAddressForm(request.POST, instance=address)
        else:
            address_form = DeliveryAddressForm(request.POST)

        if address_form.is_valid():
            new_address = address_form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            if new_address.is_default:
                DeliveryAddress.objects.filter(user=request.user).exclude(id=new_address.id).update(is_default=False)
            return redirect('my_account')

    return render(request, 'myapp/my_account.html', {
        'profile_form': profile_form,
        'address_form': address_form,
        'addresses': addresses,
        'social_email': social_email,
    })

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(DeliveryAddress, id=address_id, user=request.user)
    address.delete()
    messages.success(request, "ลบที่อยู่เรียบร้อยแล้ว")
    return redirect('my_account')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    addresses = DeliveryAddress.objects.filter(user=request.user)
    default_address = addresses.filter(is_default=True).first()
    payment_form = PaymentForm()

    if not cart_items.exists():
        messages.warning(request, "รถเข็นของคุณว่างเปล่า")
        return redirect('view_cart')

    total_price = sum(item.menu_item.price * item.quantity for item in cart_items)

    
    return render(request, 'myapp/checkout.html', {
        'cart_items': cart_items,
        'addresses': addresses,
        'default_address': default_address,
        'payment_form': payment_form,
        'total_price': total_price,
    })

@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST' and 'payment_slip' in request.FILES:
        form = PaymentSlipForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            order.status = 'pending'
            form.save()
            messages.success(request, "อัปโหลดสลิปเรียบร้อยแล้ว")
            return redirect('payment_success', order_id=order.id)
    else:
        form = PaymentSlipForm(instance=order)

    return render(request, 'myapp/payment_success.html', {'order': order, 'form': form})

@login_required
def upload_payment_slip(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        form = PaymentSlipForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            order.status = 'pending'
            form.save()
            messages.success(request, "อัปโหลดสลิปเรียบร้อยแล้ว กรุณารอการตรวจสอบจากแอดมิน")
            return redirect('my_orders')
    else:
        form = PaymentSlipForm(instance=order)

    return render(request, 'myapp/upload_slip.html', {'form': form, 'order': order})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'myapp/order_success.html', {'order': order})

# ✅ ฟังก์ชันให้คะแนนเมนูอาหาร
@login_required
def submit_review(request, order_id, menu_item_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)

    if not order.items.filter(menu_item=menu_item).exists():
        messages.error(request, "ไม่สามารถให้คะแนนเมนูนี้ได้")
        return redirect('my_orders')

    if request.method == 'POST':
        form = MenuReviewForm(request.POST)
        if form.is_valid():
            review, created = MenuReview.objects.get_or_create(
                menu_item=menu_item,
                user=request.user,
                order=order,
                defaults={
                    'rating': form.cleaned_data['rating'],
                    'comment': form.cleaned_data['comment']
                }
            )
            if not created:
                review.rating = form.cleaned_data['rating']
                review.comment = form.cleaned_data['comment']
                review.save()
            messages.success(request, f"คุณได้ให้คะแนน {menu_item.name} เรียบร้อยแล้ว")
            return redirect('my_orders')
    else:
        form = MenuReviewForm()

    return render(request, 'myapp/review_popup.html', {
        'form': form,
        'menu_item': menu_item,
        'order': order,
    })


def about(request):
    return render(request, 'myapp/about.html')


class SurpriseBoxListView(ListView):
    model = MenuItem
    template_name = 'myapp/surprise_boxes.html'
    context_object_name = 'menu_items'

    def get_queryset(self):
        queryset = MenuItem.objects.filter(is_available=True, is_surprise_box=True)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
        categories = self.request.GET.getlist('category')
        if categories:
            queryset = queryset.filter(category__name__in=categories)
        allergens = self.request.GET.getlist('allergen')
        for allergen in allergens:
            queryset = queryset.exclude(allergens__name=allergen)
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price and max_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price), price__lte=float(max_price))
            except ValueError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all(),
            'allergens': Allergen.objects.all(),
            'selected_categories': self.request.GET.getlist('category'),
            'selected_allergens': self.request.GET.getlist('allergen'),
            'search_query': self.request.GET.get('q', ''),
        })
        return context