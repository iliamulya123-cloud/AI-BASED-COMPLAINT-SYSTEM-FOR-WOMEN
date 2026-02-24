from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('complaints/new/', views.submit_complaint, name='submit_complaint'),
    path('complaints/<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
    path('chatbot/guidance/', views.chatbot_guidance, name='chatbot_guidance'),
    path('staff/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff/complaints/<int:complaint_id>/status/', views.update_complaint_status, name='update_complaint_status'),
]
