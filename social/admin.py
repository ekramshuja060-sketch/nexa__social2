from django.contrib import admin
# اگر فعلاً مدل نداری، همین فایل کافی است
# وقتی مدل ساختی، این‌طوری ثبتش می‌کنی:
#
# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'created_at')
from .models import Post, UserProfile  # مدل‌های خودتون

admin.site.register(Post)
admin.site.register(UserProfile)