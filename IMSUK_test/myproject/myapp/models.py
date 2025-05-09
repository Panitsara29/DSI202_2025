#models.py 
from django.db import models
from django.contrib.auth.models import User

# หมวดหมู่เมนู เช่น อาหารจานเดียว เครื่องดื่ม 
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# ชื่อร้านค้า เช่น ร้านส้มตำ ร้านชาบู
class Restaurant(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

# ส่วนผสมที่แพ้ เช่น กลูเตน ถั่ว นม อาหารทะเล
class Allergen(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# รายการเมนูอาหาร
class MenuItem(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=50.00)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)
    allergens = models.ManyToManyField(Allergen, blank=True)
    image = models.ImageField(upload_to='menu/', blank=True, null=True)

    def __str__(self):
        return self.name

# รายการในรถเข็น
class CartItem(models.Model):
    session_key = models.CharField(max_length=40, null=True, blank=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"

# ออเดอร์
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order #{self.pk} by {self.user.username}"

# รายการอาหารในออเดอร์
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity} (Order #{self.order.id})"
