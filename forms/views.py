from rest_framework import viewsets, parsers
from .models import FormTemplate, Submission
from .serializers import FormTemplateSerializer, SubmissionSerializer
from .tasks import notify_admin  # 👈 import your Celery task


class FormTemplateViewSet(viewsets.ModelViewSet):
    queryset = FormTemplate.objects.all()
    serializer_class = FormTemplateSerializer


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

    def perform_create(self, serializer):
        # Save the submission first
        submission = serializer.save()

        # ✅ Trigger async email notification via Celery
        notify_admin.delay(submission.id)
