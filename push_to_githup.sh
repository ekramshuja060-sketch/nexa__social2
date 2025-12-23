# -----------------------------
# 🟢 run_nexa.ps1
# اجرای خودکار پروژه Nexa Social با داده‌های نمونه
# -----------------------------

Write-Host "🚀 اجرای پروژه Nexa Social (نسخه خودکار)..."

# 1️⃣ فعال کردن محیط مجازی
$venvPath = ".\venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    Write-Host "فعال کردن محیط مجازی..."
    & $venvPath
} else {
    Write-Host "⚠️ محیط مجازی پیدا نشد! لطفا ابتدا venv را بساز و فعال کن."
    exit
}

# 2️⃣ نصب پیش‌نیازها
Write-Host "بررسی نصب پکیج‌های مورد نیاز..."
pip install -r requirements.txt

# 3️⃣ ساخت پوشه‌های ضروری
$folders = @(".\static\uploads")
foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        Write-Host "ایجاد پوشه: $folder"
        New-Item -ItemType Directory -Force -Path $folder | Out-Null
    }
}

# 4️⃣ ایجاد فایل app_auto.py با نمونه داده خودکار
$appFile = ".\app_auto.py"
Write-Host "ایجاد فایل Flask خودکار: $appFile"

@"
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = SQLAlchemy(app)

# مدل User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    bio = db.Column(db.Text, default="")
    profile_image = db.Column(db.String(200), default="https://picsum.photos/100")

# مدل Post
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200))
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# نمونه داده‌ها
users = [
    {"username": "ekram", "bio": "عاشق برنامه‌نویسی 🚀", "profile_image": "https://picsum.photos/100/100"},
    {"username": "shuja", "bio": "دوستدار سفر و عکاسی 😎", "profile_image": "https://picsum.photos/101/100"}
]

posts = [
    {"id": 1, "user": "ekram", "content": "سلام دنیا! این اولین پستم هست 🚀", "image_url": "https://picsum.photos/500/300", "likes": 10, "comments": 2},
    {"id": 2, "user": "shuja", "content": "یک روز عالی در کنار دوستان 😎", "image_url": "https://picsum.photos/500/301", "likes": 7, "comments": 1}
]

# روت اصلی
@app.route("/")
def home():
    return render_template("home.html", posts=posts)

# اجرای سرور
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
"@ | Out-File -Encoding UTF8 $appFile

# 5️⃣ اجرای Flask خودکار
Write-Host "🚀 اجرای وب سرور Nexa Social با داده‌های خودکار..."
python app_auto.py

# 6️⃣ نمایش اطلاعات دسترسی
Write-Host "🌐 مرورگر خود را باز کنید و به http://127.0.0.1:5000 بروید"
