from django.contrib import admin
from services.models import (Department, Complaint, Feedback, DepartmentChairperson)
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html


@admin.action(description="book selected rooms")
def book_rooms(modeladmin, request, queryset):
    queryset.update(booked=True)


@admin.action(description="Unbook selected rooms")
def unbook_rooms(modeladmin, request, queryset):
    queryset.update(booked=False)
    
admin.site.register(Feedback)

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    ordering = ('-date_posted',)
    # search_fields = ('apartment__apartment_name__icontains','room_type__icontains','rent__icontains','room_number__icontains')
    list_filter = ('date_posted','department','status')
    list_display = ('date_posted','department','sender','status',)
    # actions = [book_rooms, unbook_rooms]
    # fieldsets = [
    #     ("New-room", {
    #         "classes": ("collapse", "expanded"),
    #         "fields": ('room_number','rent','rate','booked','room_type','size','apartment'),
    #     }),
    # ]
    
    
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    ordering = ('department_name',)
    list_display = ('department_number', 'department_name', 'display_chairs')
    
    def display_chairs(self, obj):
        chairs = obj.chairs.all()
        return ", ".join([str(chair.user) for chair in chairs])
    display_chairs.short_description = 'Chairpersons'

@admin.register(DepartmentChairperson)
class DepartmentChairpersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'date_assigned')
    list_filter = ('department',)
    search_fields = ('user__username', 'department__department_name')