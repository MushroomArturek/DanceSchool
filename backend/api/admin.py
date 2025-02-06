from django.contrib import admin

# Register your models here.

from .models import Instructor


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'specialization', 'email')
    search_fields = ('first_name', 'last_name', 'specialization')