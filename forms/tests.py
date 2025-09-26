# forms/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import FormTemplate, Submission
from django.contrib.auth import get_user_model

User = get_user_model()

class FormTemplateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

        # Sample form data
        self.form_data = {
            "name": "KYC Form",
            "slug": "kyc-form",
            "description": "Customer KYC form",
            "schema": {
                "fields": [
                    {"key": "full_name", "type": "text", "required": True},
                    {"key": "dob", "type": "date", "required": True},
                    {"key": "id_document", "type": "file", "required": True}
                ]
            }
        }

    def test_create_form_template(self):
        response = self.client.post("/api/forms/", self.form_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FormTemplate.objects.count(), 1)
        self.assertEqual(FormTemplate.objects.first().name, "KYC Form")

    def test_list_form_templates(self):
        FormTemplate.objects.create(
            name="Loan Form",
            slug="loan-form",
            description="Loan application",
            schema={}
        )
        response = self.client.get("/api/forms/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class SubmissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser2", password="testpass")
        self.client.force_authenticate(user=self.user)

        self.form = FormTemplate.objects.create(
            name="Investment Form",
            slug="investment-form",
            description="Investment details",
            schema={"fields": [{"key": "amount", "type": "number", "required": True}]}
        )

        self.submission_data = {
            "form": self.form.id,
            "form_version": self.form.version,
            "form_snapshot": self.form.schema,
            "data": {"amount": 1000},
            "submitted_by": self.user.id
        }

    def test_create_submission(self):
        response = self.client.post("/api/submissions/", self.submission_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Submission.objects.count(), 1)
        self.assertEqual(Submission.objects.first().form.name, "Investment Form")

    def test_list_submissions(self):
        Submission.objects.create(
            form=self.form,
            form_version=self.form.version,
            form_snapshot=self.form.schema,
            data={"amount": 500},
            submitted_by=self.user
        )
        response = self.client.get("/api/submissions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
