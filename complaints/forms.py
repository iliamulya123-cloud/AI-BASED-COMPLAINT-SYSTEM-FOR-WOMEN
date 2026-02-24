from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Complaint, ComplaintAttachment


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ComplaintForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
    attachments = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'accept': 'image/*,audio/*,.pdf,.doc,.docx,.txt'})
    )

    class Meta:
        model = Complaint
        fields = ('incident_type', 'location', 'incident_time', 'description', 'evidence_notes')
        widgets = {
            'incident_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'evidence_notes': forms.Textarea(attrs={'rows': 3}),
        }

    def save(self, commit=True, user=None):
        complaint = super().save(commit=False)
        if user:
            complaint.user = user
        complaint.set_description(self.cleaned_data['description'])
        if commit:
            complaint.save()
            for f in self.files.getlist('attachments'):
                ComplaintAttachment.objects.create(complaint=complaint, file=f)
        return complaint


class ComplaintStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('status',)
