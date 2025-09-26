from django.db import models

class FormTemplate(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    version = models.IntegerField(default=1)
    description = models.TextField(blank=True)
    schema = models.JSONField(default=dict)  # Dynamic field configuration
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (v{self.version})"

    def bump_version(self):
        self.version += 1
        self.save(update_fields=["version"])


class Submission(models.Model):
    form = models.ForeignKey(FormTemplate, on_delete=models.PROTECT, related_name="submissions")
    form_version = models.IntegerField()
    form_snapshot = models.JSONField()  # snapshot of schema at submission
    data = models.JSONField()           # submitted data
    status = models.CharField(max_length=32, default="submitted")
    client_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission {self.id} for {self.form.name}"


class SubmissionFile(models.Model):
    submission = models.ForeignKey(Submission, related_name="files", on_delete=models.CASCADE)
    field_key = models.CharField(max_length=255)          # which field this file belongs to
    file_url = models.URLField()                          # URL to S3/MinIO object or local storage
    original_filename = models.CharField(max_length=512, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File {self.original_filename} for submission {self.submission.id}"
