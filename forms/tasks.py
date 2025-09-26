from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def notify_admin(submission_id):
    from .models import Submission  
    submission = Submission.objects.get(id=submission_id)
    admin_email = "amakovebridgit@gmail.com"  

    send_mail(
        subject=f"New submission for {submission.form.name}",
        message=f"A new submission has been made by {submission.submitted_by or 'Anonymous'}.\nSubmission ID: {submission.id}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[admin_email],
    )
    return f"Notification sent for submission {submission_id}"
