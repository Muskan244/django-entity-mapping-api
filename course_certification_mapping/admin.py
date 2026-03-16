from django.contrib import admin
from .models import CourseCertificationMapping


@admin.register(CourseCertificationMapping)
class CourseCertificationMappingAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "certification", "primary_mapping", "is_active", "created_at")
    list_filter = ("primary_mapping", "is_active", "course", "certification")
