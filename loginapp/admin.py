from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # 필요에 따라 list_display, fieldsets 등을 커스터마이징할 수 있음

admin.site.register(CustomUser, CustomUserAdmin)
