# -----------------------------
# 🟢 run_nexa.ps1
# اجرای اتوماتیک پروژه Nexa Social (نسخه پیشرفته)
# -----------------------------

Write-Host "🚀 اجرای پروژه Nexa Social..."

# 1️⃣ فعال کردن محیط مجازی
$venvPath = ".\venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    Write-Host "فعال کردن محیط مجازی..."
    & $venvPath
} else {
    Write-Host "⚠️ محیط مجازی پیدا نشد! لطفا ابتدا venv را بساز و فعال کن."
    exit
}

# 2️⃣ نصب پیش‌نیازها (در صورت نیاز)
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

# 4️⃣ اجرای Flask
Write-Host "🚀 اجرای وب سرور Nexa Social..."
python app.py

# 5️⃣ نمایش اطلاعات دسترسی
Write-Host "🌐 مرورگر خود را باز کنید و به http://127.0.0.1:5000 بروید"
