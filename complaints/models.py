from django.conf import settings
from django.db import models
from .encryption import EncryptionService


class Complaint(models.Model):
    class IncidentType(models.TextChoices):
        HARASSMENT = 'harassment', 'Harassment'
        DOMESTIC_VIOLENCE = 'domestic_violence', 'Domestic Violence'
        STALKING = 'stalking', 'Stalking'
        CYBER_ABUSE = 'cyber_abuse', 'Cyber Abuse'
        OTHER = 'other', 'Other'

    class Status(models.TextChoices):
        SUBMITTED = 'submitted', 'Submitted'
        UNDER_REVIEW = 'under_review', 'Under Review'
        ACTION_TAKEN = 'action_taken', 'Action Taken'
        CLOSED = 'closed', 'Closed'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints')
    incident_type = models.CharField(max_length=30, choices=IncidentType.choices)
    location = models.CharField(max_length=255)
    incident_time = models.DateTimeField()
    description_encrypted = models.TextField()
    evidence_notes = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.SUBMITTED)
    ai_summary = models.TextField(blank=True)
    ai_risk_score = models.PositiveSmallIntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def description(self):
        return EncryptionService.decrypt_text(self.description_encrypted)

    @description.setter
    def description(self, value):
        self.description_encrypted = EncryptionService.encrypt_text(value)

    def set_description(self, value: str):
        self.description = value

    def __str__(self):
        return f'Complaint #{self.pk} - {self.get_incident_type_display()}'


class ComplaintAttachment(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='complaint_evidence/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ComplaintStatusLog(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='status_logs')
    old_status = models.CharField(max_length=30, choices=Complaint.Status.choices)
    new_status = models.CharField(max_length=30, choices=Complaint.Status.choices)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=255, blank=True)
