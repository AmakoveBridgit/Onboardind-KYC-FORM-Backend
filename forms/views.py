# forms/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import FormTemplate, Submission, SubmissionFile
from .serializers import FormTemplateSerializer, SubmissionSerializer, SubmissionFileSerializer
from .tasks import notify_admin  # Celery task


class FormTemplateViewSet(viewsets.ModelViewSet):
    queryset = FormTemplate.objects.all()
    serializer_class = FormTemplateSerializer

    @action(detail=True, methods=["get"])
    def schema(self, request, pk=None):
        """
        Returns the JSON schema of a form template.
        """
        form = self.get_object()
        return Response(form.schema)



class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def create(self, request, *args, **kwargs):
        """
        Override create to attach async notification.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = serializer.save()

        # Trigger async notification to admin
        notify_admin.delay(submission.id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def add_file(self, request, pk=None):
        """
        Add a file to an existing submission.
        """
        submission = self.get_object()
        serializer = SubmissionFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(submission=submission)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
