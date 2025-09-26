"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from forms.views import FormTemplateViewSet, SubmissionViewSet

router = DefaultRouter()
router.register(r"forms", FormTemplateViewSet)
router.register(r"submissions", SubmissionViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/forms/', include('forms.urls'))  , 
    # path("api/users/", include("users.urls")),
    # path("onboarding/", include("onboarding.urls")),
    # /api/forms/submissions/

]

# Register → POST http://127.0.0.1:8000/api/users/register/

# Login → POST http://127.0.0.1:8000/api/users/login/

# Profile → GET http://127.0.0.1:8000/api/users/profile/ (with Bearer token)