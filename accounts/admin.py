from django.contrib import admin
from accounts.models import MyUser
from django.contrib.auth.admin import UserAdmin


@admin.action(description="activate selected users")
def activate_users(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="deactivate selected users")
def deactivate_users(modeladmin, request, queryset):
    queryset.update(is_active=False)
    
@admin.action(description="Set chairperson")
def set_chairpersons(modeladmin, request, queryset):
    queryset.update(role='Chairperson')

@admin.register(MyUser)
class UserAdminConfig(UserAdmin):
    ordering = ('-date_joined',)
    search_fields = ('email', 'full_name', 'username')
    list_filter = ('is_active', 'role','groups')
    list_display = ('id', 'email', 'full_name', 'phone', 'reg_no', 'username', 'role', 'is_active', 'get_groups')
    list_display_links = ('email', 'username')

    fieldsets = (
        (None, {'fields': ('email', 'password', 'full_name', 'phone', 'username', 'reg_no')}),
        ("Permissions", {"fields": ('is_staff', 'is_active', 'is_superuser', 'groups')}),
        ("Personal", {"fields": ("role", "profile_pic")}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'reg_no', 'password1', 'password2', 'phone', 'is_staff', 'is_active', 'is_superuser', 'profile_pic', 'groups'),
        }),
    )

    @admin.display(description='Teams')
    def get_groups(self, obj):
        # Display groups as a comma-separated string
        groups = obj.groups.all()
        return ", ".join([group.name for group in groups]) if groups else "No Teams"

    actions = [activate_users,deactivate_users,set_chairpersons]
# Register your models here.
