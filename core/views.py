# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    """Dashboard chính của hệ thống"""
    context = {
        'user': request.user,
    }
    
    # Thống kê cho admin
    if request.user.has_company_permission():
        from employees.models import Employee, AuditLog
        from companies.models import Company
        
        if request.user.has_corporation_permission():
            # Admin tập đoàn - thống kê toàn hệ thống
            context.update({
                'total_companies': Company.objects.filter(is_active=True).count(),
                'total_employees': Employee.objects.filter(is_active=True).count(),
                'recent_lookups': AuditLog.objects.filter(action='lookup')[:10],
            })
        else:
            # Admin công ty - thống kê công ty
            context.update({
                'company_employees': Employee.objects.filter(
                    company=request.user.company, 
                    is_active=True
                ).count(),
                'recent_lookups': AuditLog.objects.filter(
                    user__company=request.user.company,
                    action='lookup'
                )[:10],
            })
    
    return render(request, 'core/dashboard.html', context)

def home_view(request):
    """Trang chủ - redirect đến dashboard nếu đã login"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    else:
        return redirect('authentication:login')