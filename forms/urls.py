from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FormTemplateViewSet, SubmissionViewSet

router = DefaultRouter()
router.register(r"forms", FormTemplateViewSet)
router.register(r"submissions", SubmissionViewSet)

urlpatterns = router.urls
# redis://localhost:6379/0