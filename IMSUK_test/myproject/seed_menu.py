# seed_menu.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import Category, MenuItem
from django.core.files import File

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ล้างข้อมูลเดิม (optional)
#MenuItem.objects.all().delete()
#Category.objects.all().delete()

# สร้างหมวดหมู่
shrimp = Category.objects.create(name='แพ้กุ้ง')
peanut = Category.objects.create(name='แพ้ถั่ว')

# เมนู + ภาพประกอบ (ชื่อไฟล์ภาพใน /media/menu_images/)
menus = [
    {
        'name': 'ข้าวกระเพราไก่ไข่ดาว',
        'description': 'กระเพราไก่รสเผ็ดจัดจ้าน พร้อมไข่ดาวทอดกรอบ',
        'price': 55.00,
        'category': shrimp,
        'image_file': 'กะเพราไก่ไข่ดาว.jpg'
    },
    {
        'name': 'มัฟฟินช็อกโกแลตชิพไร้ถั่ว',
        'description': 'มัฟฟินเนื้อฟูผสมช็อกโกแลตชิพหวานนิดๆ ไม่มีถั่วเจือปน ปลอดภัยสำหรับผู้แพ้ถั่ว',
        'price': 40.00,
        'category': 'peanut',
        'image_file':'มัฟฟิน.jpg'
    }
]


# เพิ่มข้อมูลพร้อมโหลดภาพ
for m in menus:
    image_path = os.path.join(BASE_DIR, 'media', 'menu', m['image_file'])
    with open(image_path, 'rb') as img_file:
        menu = MenuItem.objects.create(
            name=m['name'],
            description=m['description'],
            price=m['price'],
            category=m['category'],
            is_available=True
        )
        menu.image.save(m['image_file'], File(img_file), save=True)

print("✅ Seed พร้อมภาพเมนูอาหารสำเร็จแล้ว!")
