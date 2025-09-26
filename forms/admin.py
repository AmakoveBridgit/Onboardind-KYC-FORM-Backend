from django.contrib import admin
from .models import FormTemplate, Submission, SubmissionFile

@admin.register(FormTemplate)
class FormTemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "version", "is_active", "created_at")
    search_fields = ("name", "slug")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "form", "status", "created_at")
    search_fields = ("form__name",)
    list_filter = ("status", "created_at")


@admin.register(SubmissionFile)
class SubmissionFileAdmin(admin.ModelAdmin):
    list_display = ("id", "submission", "field_key", "file_url", "uploaded_at")
    search_fields = ("field_key", "original_filename")
