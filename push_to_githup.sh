#!/bin/bash
# 🟢 دستورالعمل آماده Push پروژه Nexa Social به GitHub

# 1️⃣ اطمینان از اینکه گیت نصب شده
git --version >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Git نصب نیست! لطفا Git را نصب کن و دوباره اجرا کن."
    exit 1
fi

# 2️⃣ Initialize کردن گیت (در صورت نیاز)
if [ ! -d ".git" ]; then
    git init
    echo "🟢 گیت Initialize شد"
fi

# 3️⃣ اضافه کردن remote
git remote remove origin >/dev/null 2>&1
git remote add origin https://github.com/USERNAME/nexa__social.git
echo "🟢 Remote به GitHub اضافه شد"

# 4️⃣ ایجاد فایل .gitignore
cat > .gitignore <<EOL
__pycache__/
*.pyc
static/uploads/
EOL
echo "🟢 .gitignore ساخته شد"

# 5️⃣ مرحله اول: فایل‌های اصلی
git add app.py templates/home.html
git commit -m "✅ اضافه کردن فایل‌های اصلی پروژه با فید، لایک، کامنت و انیمیشن"
git push -u origin main
echo "🟢 مرحله 1: فایل‌های اصلی Push شد"

# 6️⃣ مرحله دوم: فرم ایجاد پست
git add templates/new_post.html
git commit -m "➕ اضافه کردن فرم ایجاد پست با متن و عکس"
git push
echo "🟢 مرحله 2: فرم ایجاد پست Push شد"

# 7️⃣ مرحله سوم: آپلود تصویر واقعی
git add app.py
git commit -m "📤 اضافه کردن قابلیت آپلود تصویر واقعی از کامپیوتر کاربر"
git push
echo "🟢 مرحله 3: آپلود تصویر Push شد"

# 8️⃣ مرحله چهارم: ویرایش و حذف پست
git add templates/edit_post.html app.py
git commit -m "✏️🗑️ اضافه کردن ویرایش و حذف پست"
git push
echo "🟢 مرحله 4: ویرایش و حذف پست Push شد"

echo "🎉 همه مراحل Push شد. پروژه اکنون روی GitHub موجود است!"
