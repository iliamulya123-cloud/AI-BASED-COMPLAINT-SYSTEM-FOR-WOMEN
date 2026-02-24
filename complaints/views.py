from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ComplaintForm, ComplaintStatusUpdateForm, RegisterForm
from .models import Complaint, ComplaintStatusLog
from .services import generate_ai_guidance
from .tasks import send_complaint_notifications


def home(request):
    return render(request, 'base/home.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})


@login_required
def dashboard(request):
    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'complaints/dashboard.html', {'complaints': complaints})


@login_required
def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(user=request.user)
            send_complaint_notifications.delay(complaint.id, request.user.email)
            messages.success(request, f'Complaint #{complaint.id} submitted successfully.')
            return redirect('complaint_detail', complaint_id=complaint.id)
    else:
        form = ComplaintForm()
    return render(request, 'complaints/submit_complaint.html', {'form': form})


@login_required
def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id, user=request.user)
    return render(request, 'complaints/complaint_detail.html', {'complaint': complaint})


@login_required
@require_POST
def chatbot_guidance(request):
    user_message = request.POST.get('message', '').strip()
    conversation = [{'role': 'user', 'content': user_message}]
    reply = generate_ai_guidance(conversation)
    return JsonResponse({'reply': reply})


def staff_check(user: User):
    return user.is_staff


@login_required
@user_passes_test(staff_check)
def admin_dashboard(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'admin_portal/dashboard.html', {'complaints': complaints})


@login_required
@user_passes_test(staff_check)
def update_complaint_status(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if request.method == 'POST':
        form = ComplaintStatusUpdateForm(request.POST, instance=complaint)
        if form.is_valid():
            old = complaint.status
            complaint = form.save()
            ComplaintStatusLog.objects.create(
                complaint=complaint,
                old_status=old,
                new_status=complaint.status,
                changed_by=request.user,
            )
            messages.success(request, f'Complaint #{complaint.id} status updated.')
            return redirect('admin_dashboard')
    else:
        form = ComplaintStatusUpdateForm(instance=complaint)
    return render(request, 'admin_portal/update_status.html', {'form': form, 'complaint': complaint})
