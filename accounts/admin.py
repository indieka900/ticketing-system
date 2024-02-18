from django.contrib import admin
from accounts.models import MyUser
from django.contrib.auth.admin import UserAdmin


@admin.action(description="activate selected users")
def activate_users(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="deactivate selected users")
def deactivate_users(modeladmin, request, queryset):
    queryset.update(is_active=False)

@admin.register(MyUser)
class UserAdminConfig(UserAdmin):
    ordering = ('-date_joined',)
    search_fields = ('email','full_name','username')
    list_filter = ('email','is_active','is_staff','role',)
    list_display = ('id','email','full_name','phone','reg_no','username','role','is_active')
    fieldsets = (
        (None, {'fields': ('email','full_name','phone','username','reg_no',)}),
        ("Permissions", {"fields" :('is_staff','is_active','is_superuser',)}),
        ("Personal", {"fields":("role","profile_pic")}),
    )
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields': ('email','full_name','reg_no','password1','password2','phone','is_staff','is_active','is_superuser','profile_pic')
        }),
    )
    actions = [activate_users,deactivate_users]
# Register your models here.
