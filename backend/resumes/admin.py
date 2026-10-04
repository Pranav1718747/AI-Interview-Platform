from django.contrib import admin
from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "user",
        "uploaded_at",
    )

    search_fields = (
        "title",
        "user__username",
    )

    list_filter = (
        "uploaded_at",
    )