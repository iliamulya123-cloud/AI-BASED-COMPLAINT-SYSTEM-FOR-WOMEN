from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from twilio.rest import Client


@shared_task
def send_complaint_notifications(complaint_id, email, phone=None):
    subject = f'Complaint #{complaint_id} Submitted'
    body = (
        f'Your complaint (ID: {complaint_id}) has been received and is under review. '
        'We will update you on any status changes.'
    )
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=True)

    if phone and settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN and settings.TWILIO_FROM_NUMBER:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(from_=settings.TWILIO_FROM_NUMBER, to=phone, body=body)
