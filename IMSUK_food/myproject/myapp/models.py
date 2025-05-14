#models.py 
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

# ✅ ขยายโปรไฟล์ผู้ใช้
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"โปรไฟล์ของ {self.user.username}"

# ✅ เก็บที่อยู่ได้หลายรายการ
class DeliveryAddress(models.Model):
    ICON_CHOICES = [
        ('home', 'บ้าน'),
        ('office', 'ที่ทำงาน'),
        ('other', 'อื่นๆ'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')

    # 🆕 ฟิลด์ใหม่
    label = models.CharField(max_length=50, blank=True, verbose_name="ชื่อที่อยู่")
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default='home', verbose_name="ไอคอน")
    
    street = models.CharField(max_length=255, verbose_name="ที่อยู่/บ้านเลขที่", default='')
    subdistrict = models.CharField(max_length=100, verbose_name="แขวง/ตำบล", default='')
    district = models.CharField(max_length=100, verbose_name="เขต/อำเภอ", default='')
    province = models.CharField(max_length=100, verbose_name="จังหวัด", default='')
    postal_code = models.CharField(max_length=10, verbose_name="รหัสไปรษณีย์", default='')
    note = models.TextField(blank=True, verbose_name="หมายเหตุ", default='')

    is_default = models.BooleanField(default=False, verbose_name="ที่อยู่หลัก")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.label or 'ที่อยู่'} | {self.street}, {self.subdistrict}, {self.district}, {self.province} {self.postal_code}"


# หมวดหมู่เมนู 
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# ชื่อร้านค้า 
class Restaurant(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

# ส่วนผสมที่แพ้ 
class Allergen(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.PositiveIntegerField(help_text="เช่น 10 = ลด 10%")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def __str__(self):
        return f"{self.code} ({self.discount_percent}% off)"

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
    favorited_by = models.ManyToManyField(User, related_name='favorite_items', blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_discounted_price(self):
        if self.coupon and self.coupon.is_active():
            discount = Decimal(self.coupon.discount_percent) / Decimal(100)
            return self.price * (Decimal(1) - discount)
        return self.price

    def get_discount_percent(self):
        if self.coupon and self.coupon.is_active():
            return self.coupon.discount_percent
        return 0

# รายการในรถเข็น
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"


# ออเดอร์
# ✅ ออเดอร์
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'รอยืนยันชำระเงิน'),
        ('paid', 'ชำระเงินแล้ว'),
        ('preparing', 'กำลังเตรียมอาหาร'),
        ('delivering', 'กำลังจัดส่ง'),
        ('completed', 'ส่งสำเร็จ'),
        ('cancelled', 'ยกเลิก'),
    ]

    PAYMENT_METHODS = [
        ('qr', 'PromptPay QR'),
        ('cod', 'ชำระเงินปลายทาง'),
        ('card', 'บัตรเครดิต'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_address = models.ForeignKey(DeliveryAddress, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # ✅ ใช้สถานะละเอียด
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='cod')
    payment_info = models.TextField(blank=True, null=True)
    payment_slip = models.ImageField(upload_to='slips/', blank=True, null=True)
    qr_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

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
