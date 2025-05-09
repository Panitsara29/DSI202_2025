#admin.py
from django.contrib import admin
# นำเข้า models ที่ใช้
from .models import (
    Category, MenuItem, CartItem, Order, OrderItem,
    Restaurant, Allergen  # ← เพิ่มสองตัวนี้
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(Allergen)
class AllergenAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'is_available', 'category', 'restaurant']
    list_filter = ['category', 'restaurant', 'is_available']
    search_fields = ['name']
    filter_horizontal = ['allergens']  # สำหรับเลือกหลาย allergens ได้ง่ายขึ้น

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'session_key', 'menu_item', 'quantity']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'status']
    list_filter = ['status', 'created_at']
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'menu_item', 'quantity', 'price']
