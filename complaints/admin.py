from django.contrib import admin
from .models import Complaint, ComplaintAttachment, ComplaintStatusLog


class ComplaintAttachmentInline(admin.TabularInline):
    model = ComplaintAttachment
    extra = 0


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'incident_type', 'status', 'created_at')
    search_fields = ('user__username', 'location', 'description_encrypted')
    list_filter = ('incident_type', 'status', 'created_at')
    inlines = [ComplaintAttachmentInline]


@admin.register(ComplaintStatusLog)
class ComplaintStatusLogAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'old_status', 'new_status', 'changed_by', 'changed_at')
