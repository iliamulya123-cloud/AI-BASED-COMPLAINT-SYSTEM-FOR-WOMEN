from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incident_type', models.CharField(choices=[('harassment', 'Harassment'), ('domestic_violence', 'Domestic Violence'), ('stalking', 'Stalking'), ('cyber_abuse', 'Cyber Abuse'), ('other', 'Other')], max_length=30)),
                ('location', models.CharField(max_length=255)),
                ('incident_time', models.DateTimeField()),
                ('description_encrypted', models.TextField()),
                ('evidence_notes', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('submitted', 'Submitted'), ('under_review', 'Under Review'), ('action_taken', 'Action Taken'), ('closed', 'Closed')], default='submitted', max_length=30)),
                ('ai_summary', models.TextField(blank=True)),
                ('ai_risk_score', models.PositiveSmallIntegerField(default=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaints', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ComplaintAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='complaint_evidence/%Y/%m/%d/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('complaint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='complaints.complaint')),
            ],
        ),
        migrations.CreateModel(
            name='ComplaintStatusLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_status', models.CharField(choices=[('submitted', 'Submitted'), ('under_review', 'Under Review'), ('action_taken', 'Action Taken'), ('closed', 'Closed')], max_length=30)),
                ('new_status', models.CharField(choices=[('submitted', 'Submitted'), ('under_review', 'Under Review'), ('action_taken', 'Action Taken'), ('closed', 'Closed')], max_length=30)),
                ('changed_at', models.DateTimeField(auto_now_add=True)),
                ('note', models.CharField(blank=True, max_length=255)),
                ('changed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('complaint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_logs', to='complaints.complaint')),
            ],
        ),
    ]
