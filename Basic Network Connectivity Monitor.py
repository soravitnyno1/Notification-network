import subprocess
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# กำหนดเป้าหมายที่จะ Ping
target = "1.1.1.1"

# --- ตั้งค่า Gmail สำหรับส่งแจ้งเตือน ---
SENDER_EMAIL = "xxxxxx@gmail.com"        # อีเมลของคุณ (ผู้ส่ง)
SENDER_PASSWORD = "xxxx xxxx xxxx xxxx"      # รหัสผ่านแอป 16 หลักที่สร้างจาก Google Account
RECEIVER_EMAIL = "xxxxxx@gmail.com"      # อีเมลปลายทางที่จะรับแจ้งเตือน (ส่งหาตัวเองได้)

def send_alert_email():
    try:
        subject = "⚠️ Network Alert: CONNECTION DOWN!"
        body = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ระบบตรวจพบว่าอินเทอร์เน็ตขาดการเชื่อมต่อ (Connection Down) ไปยังเป้าหมาย {target}"
        
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # เชื่อมต่อกับ Gmail SMTP Server (พอร์ต 587 สำหรับ TLS)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ✉️ ส่งอีเมลแจ้งเตือนผ่าน Gmail สำเร็จ!")
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ❌ ส่งอีเมลไม่สำเร็จ: {e}")

print(f"[*] Starting Network Connectivity Monitor for {target} with Gmail Alerts...")
print("-" * 50)

while True:
    try:
        # สั่งรันคำสั่ง ping (ใช้ -n 1 สำหรับ Windows)
        result = subprocess.run(
            ["ping", "-n", "1", target], 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        
        # ตรวจสอบผลลัพธ์ (returncode == 0 แปลว่าเชื่อมต่อสำเร็จ)
        if result.returncode == 0:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Connection OK: เชื่อมต่อปกติ")
        else:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] CONNECTION DOWN: ขาดการเชื่อมต่อ!")
            send_alert_email()
            
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Encountered an error: {e}")

    time.sleep(60)