
# IMSUK (อิ่มสุข) – สั่งอาหารเพื่อส่งเสริมความยั่งยืนในชุมชน

## 1. บทคัดย่อ (Abstract)

ระบบ IMSUK (อิ่มสุข) คือเว็บแอปพลิเคชันสำหรับการสั่งอาหารที่ได้รับการออกแบบมาเพื่ออำนวยความสะดวกให้แก่ประชาชนทั่วไปในการเลือกสรรและสั่งอาหารจากร้านค้าท้องถิ่น โดยมีจุดมุ่งหมายหลักในการส่งเสริมแนวคิด “Zero Food Waste” ผ่านการนำเสนอเมนูอาหารที่ใช้วัตถุดิบใกล้หมดอายุ พร้อมทั้งสนับสนุนผู้ประกอบการรายย่อยให้สามารถบริหารจัดการวัตถุดิบและจำหน่ายอาหารได้อย่างมีประสิทธิภาพยิ่งขึ้น

ระบบได้รับการพัฒนาด้วย Django Framework (ภาษา Python) และรองรับการทำงานผ่าน Docker Compose เพื่อให้สามารถติดตั้งและใช้งานได้อย่างสะดวกทั้งในสภาพแวดล้อมการพัฒนาและระบบปฏิบัติการจริง โดยครอบคลุมฟังก์ชันการทำงานที่สำคัญ อาทิ การค้นหาเมนู การจัดการรถเข็น การชำระเงิน และระบบหลังบ้านสำหรับผู้ดูแลร้านอาหาร

---

## 2. กลุ่มเป้าหมายของผู้ใช้งาน (Target Users)

- บุคคลทั่วไปที่ต้องการสั่งอาหารผ่านระบบออนไลน์อย่างมีประสิทธิภาพ  
- ร้านอาหารในชุมชนที่ประสงค์จะลดต้นทุนและจัดการวัตถุดิบอย่างเหมาะสม  
- ผู้สนใจด้านการพัฒนาเทคโนโลยีเพื่อความยั่งยืนทางสังคมและสิ่งแวดล้อม  
- นักเรียน นักศึกษา หรือบุคคลทั่วไปที่ศึกษาเกี่ยวกับการพัฒนาเว็บแอปพลิเคชัน  

---

## 3. ลักษณะการใช้งานของผู้ใช้ (User Stories)

### 3.1 ผู้ใช้ทั่วไป

- ผู้ใช้สามารถค้นหาเมนูอาหารจากร้านค้าต่าง ๆ โดยใช้คำค้นและตัวกรองตามประเภทอาหารหรือสารก่อภูมิแพ้  
- ผู้ใช้สามารถเพิ่มรายการอาหารลงในรถเข็น และดำเนินการสั่งซื้อได้อย่างสะดวก  
- ผู้ใช้สามารถจัดการข้อมูลโปรไฟล์ส่วนตัว รวมถึงเพิ่มและตั้งค่าที่อยู่สำหรับการจัดส่ง  

### 3.2 เจ้าของร้านอาหาร

- เจ้าของร้านสามารถเพิ่ม แก้ไข หรือลบเมนูอาหาร รวมถึงกำหนดโปรโมชั่นพิเศษตามวัตถุดิบคงเหลือ  
- เจ้าของร้านสามารถตรวจสอบคำสั่งซื้อที่เข้ามา และจัดการสถานะการสั่งซื้อได้แบบเรียลไทม์  

---

## 4. ฟังก์ชันการทำงานหลักของระบบ (Key Features)

- ระบบค้นหาและกรองเมนูอาหาร  
- ระบบจัดการรถเข็นสินค้าและประวัติการสั่งซื้อ  
- ระบบจัดการโปรไฟล์ผู้ใช้งานและที่อยู่สำหรับจัดส่ง  
- ระบบเพิ่มรายการโปรด (Favorites)  
- ระบบจำลองการชำระเงิน: QR Code, ชำระเงินปลายทาง และบัตรเครดิต  
- ระบบแนะนำเมนูพิเศษเพื่อลดปริมาณอาหารเหลือทิ้ง (Food Waste Reduction)  
- ระบบจัดการเมนูและข้อมูลร้านอาหารผ่านแผงควบคุมผู้ดูแล (Admin Panel)  

---

## 5. เทคโนโลยีที่ใช้ในการพัฒนา (Technology Stack)

- **Frontend**: HTML5, Tailwind CSS  
- **Backend**: Django 4.x (Python)  
- **Database**: PostgreSQL  
- **Deployment**: Docker Compose  
- **Image Processing**: Pillow  
- **Libraries/Tools เพิ่มเติม**: Fontawesome, Flaticon, Google Fonts  

---

## 6. การติดตั้งและการใช้งานระบบ (Installation and Usage)

### 6.1 ข้อกำหนดเบื้องต้น (Prerequisites)

กรุณาติดตั้งเครื่องมือดังต่อไปนี้ก่อนเริ่มการติดตั้งระบบ:

- Docker: https://docs.docker.com/get-docker/  
- Docker Compose: https://docs.docker.com/compose/install/  

---

### 6.2 ขั้นตอนการติดตั้งและเริ่มต้นใช้งาน (Setup and Run)

#### ขั้นตอนที่ 1: โคลน Repository

```bash
git clone https://github.com/Panitsara29/DSI202_2025.git
```

> หมายเหตุ: กรุณาเปลี่ยน `yourusername` ให้ตรงกับชื่อ GitHub ของคุณ

---

#### ขั้นตอนที่ 2: เข้าสู่ไดเรกทอรีโปรเจกต์

```bash
cd DSI202_2025
```

---

#### ขั้นตอนที่ 3: สร้างและรัน Container ด้วย Docker Compose

```bash
docker-compose up --build
```

---

#### หากต้องการรันแบบ background mode ให้ใช้คำสั่ง:

```bash
docker-compose up --build -d
```

---

### 6.3 การเข้าถึงระบบ (Accessing the System)

#### เว็บไซต์หลัก:

- http://localhost:8000  

#### ระบบผู้ดูแล (Django Admin):

- http://localhost:8000/admin  

#### บัญชีสำหรับทดลองใช้งาน:

```text
Username: XXXXX
Password: XXXX
```

---

## 7. วิดีโอสาธิตการใช้งานระบบ (System Demonstration Video)

สามารถรับชมวิดีโอการใช้งานระบบ IMSUK ได้ที่ลิงก์ด้านล่าง:

📽️ [คลิกเพื่อรับชมวิดีโอการสาธิต](https://youtu.be/your-demo-link)

---

## 8. คุณประโยชน์ของระบบต่อชุมชน (Social and Community Impact)

IMSUK มีบทบาทสำคัญในการลดปริมาณอาหารเหลือทิ้ง (food waste) ผ่านการเสนอเมนูพิเศษที่ใช้วัตถุดิบคงเหลืออย่างมีประสิทธิภาพ สนับสนุนการบริโภคอย่างยั่งยืน และสร้างโอกาสทางรายได้เพิ่มเติมให้แก่ผู้ประกอบการร้านอาหารในชุมชน ถือเป็นแนวทางที่สอดคล้องกับเป้าหมายการพัฒนาที่ยั่งยืนในระยะยาว

---

## 9. การติดต่อและข้อเสนอแนะ (Contact and Feedback)

หากผู้ใช้งานพบปัญหา หรือมีข้อเสนอแนะเกี่ยวกับระบบ IMSUK สามารถติดต่อทีมพัฒนาได้ผ่านช่องทาง GitHub Repository:

🔗 https://github.com/Panitsara29/DSI202_2025.git

---

## ข้อมูลผู้จัดทำ (Author Information) ദ്ദി(˵ •̀ ᴗ - ˵ ) 

**ผู้จัดทำ** : นางสาวปาณิสรา ตติไตรสกุล (รหัสนักศึกษา 6624650096)  
**รายวิชา** : DSI310 Data Exploration and Preprocessing  
วิทยาลัยสหวิทยาการ สาขาวิทยาศาสตร์และนวัตกรรมข้อมูล มหาวิทยาลัยธรรมศาสตร์  
ภาคเรียนที่ 2 ปีการศึกษา 2567

---
