# forms/serializers.py
from rest_framework import serializers
from .models import FormTemplate, Submission, SubmissionFile


class FormTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormTemplate
        fields = ["id", "name", "slug", "description", "version", "schema", "is_active", "created_at"]


class SubmissionFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionFile
        fields = ["id", "field_key", "file_url", "original_filename", "metadata", "uploaded_at", "submission"]
        read_only_fields = ["id", "uploaded_at", "submission"]


class SubmissionSerializer(serializers.ModelSerializer):
    files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )
    file_field_keys = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Submission
        fields = [
            "id", "form", "form_version", "form_snapshot",
            "data", "status", "client_ip", "created_at",
            "files", "file_field_keys"
        ]
        read_only_fields = ["id", "status", "client_ip", "created_at"]

    def create(self, validated_data):
        files = validated_data.pop("files", [])
        keys = validated_data.pop("file_field_keys", [])
        submission = Submission.objects.create(**validated_data)

        for i, f in enumerate(files):
            field_key = keys[i] if i < len(keys) else "file"
            SubmissionFile.objects.create(
                submission=submission,
                field_key=field_key,
                original_filename=f.name,
                file_url=f"uploads/{f.name}",  
            )
        return submission
