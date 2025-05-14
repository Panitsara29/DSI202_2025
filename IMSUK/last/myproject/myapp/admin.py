from django.contrib import admin
from .models import Order, OrderItem, MenuItem, Category, Restaurant, Allergen, CartItem, Profile, DeliveryAddress, Coupon

from django.utils.html import format_html

# 🥗 หมวดหมู่
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

# 🍽 ร้านอาหาร
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

# ⚠️ ส่วนผสมที่แพ้
@admin.register(Allergen)
class AllergenAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

# 🍱 เมนูอาหาร
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'is_available', 'category', 'restaurant', 'coupon']
    list_filter = ['category', 'restaurant', 'is_available', 'coupon']
    search_fields = ['name']
    filter_horizontal = ['allergens']  

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'start_date', 'end_date']
    list_filter = ['start_date', 'end_date']

# 🛒 รถเข็น
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'menu_item', 'quantity']

# 📦 ออเดอร์และรายการในออเดอร์
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'colored_status', 'total_price', 'created_at', 'show_payment_slip')
    list_filter = ('status', 'payment_method', 'created_at')
    readonly_fields = ('created_at', 'updated_at', 'qr_image', 'payment_slip_preview')
    fields = (
        'user', 'delivery_address', 'status', 'payment_method', 'total_price',
        'created_at', 'updated_at', 'payment_info',
        'qr_image', 'payment_slip', 'payment_slip_preview'
    )
    change_list_template = "admin/order_change_list.html"  
    def changelist_view(self, request, extra_context=None):
        pending_count = Order.objects.filter(status='pending').count()
        if extra_context is None:
            extra_context = {}
        extra_context['pending_count'] = pending_count
        return super().changelist_view(request, extra_context=extra_context)
    
    def show_payment_slip(self, obj):
        if obj.payment_slip:
            return format_html('<img src="{}" width="100" />', obj.payment_slip.url)
        return '-'
    show_payment_slip.short_description = 'สลิปชำระเงิน'

    def payment_slip_preview(self, obj):
        if obj.payment_slip:
            return format_html('<img src="{}" width="250" style="border:1px solid #ccc;"/>', obj.payment_slip.url)
        return "ยังไม่มีสลิป"
    payment_slip_preview.short_description = "พรีวิวสลิป"
    
    def colored_status(self, obj):
        color_map = {
            'pending': 'orange',
            'paid': 'blue',
            'preparing': 'purple',
            'delivering': 'teal',
            'completed': 'green',
            'cancelled': 'red',
        }
        color = color_map.get(obj.status, 'black')
        label = dict(Order.STATUS_CHOICES).get(obj.status, obj.status)
        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 8px; border-radius: 10px;">{}</span>',
            color,
            label
        )
    colored_status.short_description = 'สถานะ'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'menu_item', 'quantity', 'price']

# 🏠 ที่อยู่จัดส่ง
@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'label', 'icon', 'province', 'district', 'is_default']
    list_filter = ['icon', 'is_default', 'province']
    search_fields = ['user__username', 'label', 'province', 'district', 'postal_code']
    readonly_fields = ['created_at']
    fieldsets = (
        (None, {
            'fields': ('user', 'label', 'icon', 'is_default')
        }),
        ('ที่อยู่', {
            'fields': ('street', 'subdistrict', 'district', 'province', 'postal_code', 'note')
        }),
        ('ระบบ', {
            'fields': ('created_at',)
        }),
    )


