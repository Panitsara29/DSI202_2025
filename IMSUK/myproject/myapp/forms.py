from django import forms
from django.contrib.auth.models import User
from .models import Profile, DeliveryAddress, Order, MenuReview, Coupon 

ICON_CHOICES = [
    ('home', 'บ้าน'),
    ('office', 'ที่ทำงาน'),
    ('other', 'อื่นๆ'),
]

# ✅ แบบฟอร์มสมัครสมาชิก
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='รหัสผ่าน', widget=forms.PasswordInput)
    password2 = forms.CharField(label='ยืนยันรหัสผ่าน', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'ชื่อผู้ใช้',
            'email': 'อีเมล',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError('รหัสผ่านไม่ตรงกัน')
        return cd['password2']


# ✅ แบบฟอร์มข้อมูลส่วนตัว
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'phone']
        labels = {
            'full_name': 'ชื่อ - นามสกุล',
            'phone': 'เบอร์โทรศัพท์',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded'}),
        }


# ✅ แบบฟอร์มที่อยู่จัดส่ง
class DeliveryAddressForm(forms.ModelForm):
    label = forms.CharField(
        label='ชื่อที่อยู่',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border rounded',
            'placeholder': 'เช่น บ้าน, ที่ทำงาน...'
        })
    )

    icon = forms.ChoiceField(
        label='ไอคอน',
        choices=ICON_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'mr-2 text-pink-500'})
    )

    class Meta:
        model = DeliveryAddress
        fields = ['label', 'icon', 'street', 'subdistrict', 'district', 'province', 'postal_code', 'note', 'is_default']
        labels = {
            'street': 'ที่อยู่/บ้านเลขที่',
            'subdistrict': 'แขวง/ตำบล',
            'district': 'เขต/อำเภอ',
            'province': 'จังหวัด',
            'postal_code': 'รหัสไปรษณีย์',
            'note': 'หมายเหตุ',
            'is_default': 'ตั้งเป็นที่อยู่หลัก',
        }
        widgets = {
            'street': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'subdistrict': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'district': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'province': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'postal_code': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded'}),
            'note': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded', 'rows': 2}),
            'is_default': forms.CheckboxInput(attrs={'class': 'mr-2'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


# ✅ แบบฟอร์มเลือกวิธีการชำระเงิน
class PaymentForm(forms.Form):
    PAYMENT_CHOICES = [
        ('qr', 'PromptPay QR'),
        ('cod', 'ชำระเงินปลายทาง'),
        ('card', 'บัตรเครดิต'),
    ]

    payment_method = forms.ChoiceField(
        label='เลือกวิธีชำระเงิน',
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'mr-2 text-pink-500'})
    )

    card_number = forms.CharField(
        label='เลขบัตรเครดิต',
        max_length=16,
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded', 'placeholder': 'เช่น 4242424242424242'})
    )

    expiry_date = forms.CharField(
        label='วันหมดอายุ (MM/YY)',
        max_length=5,
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded', 'placeholder': 'MM/YY'})
    )

    cvv = forms.CharField(
        label='CVV',
        max_length=4,
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded'})
    )

    coupon_code = forms.ChoiceField(
        label='เลือกคูปองส่วนลด (ถ้ามี)',
        required=False,
        choices=[],
        widget=forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded bg-white'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        active_coupons = Coupon.objects.filter(is_public=True)
        self.fields['coupon_code'].choices = [('', 'ไม่ใช้คูปอง')] + [
            (c.code, f"{c.code} - ลด {c.discount_percent}%") for c in active_coupons if c.is_active()
        ]

    def clean(self):
        cleaned_data = super().clean()
        method = cleaned_data.get('payment_method')
        if method == 'card':
            if not all([
                cleaned_data.get('card_number'),
                cleaned_data.get('expiry_date'),
                cleaned_data.get('cvv')
            ]):
                raise forms.ValidationError("กรุณากรอกข้อมูลบัตรให้ครบถ้วนสำหรับการชำระด้วยบัตรเครดิต")
        return cleaned_data

    
# ✅ แบบฟอร์มอัปโหลดสลิปชำระเงิน
class PaymentSlipForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_slip']
        labels = {
            'payment_slip': 'อัปโหลดสลิปการชำระเงิน',
        }
        widgets = {
            'payment_slip': forms.ClearableFileInput(attrs={'class': 'w-full px-4 py-2 border rounded bg-white'}),
        }


# ✅ แบบฟอร์มให้คะแนนเมนูอาหาร
class MenuReviewForm(forms.ModelForm):
    class Meta:
        model = MenuReview
        fields = ['rating', 'comment']
        labels = {
            'rating': 'ให้คะแนน',
            'comment': 'ความคิดเห็นเพิ่มเติม (ถ้ามี)',
        }
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'hidden'  # ⭐ ใช้ JS แทน star selector UI
            }),
            'comment': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded', 'rows': 3}),
        }
