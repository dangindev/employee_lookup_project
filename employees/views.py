from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Employee, PurchaseHistory, AuditLog
from .forms import EmployeeLookupForm
from companies.models import Company
import json

class EmployeeLookupView(LoginRequiredMixin, TemplateView):
    template_name = 'employees/lookup.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EmployeeLookupForm()
        return context

@login_required
@require_http_methods(["GET"])
def employee_search_api(request):
    """API endpoint để tra cứu nhân viên - cho phép cross-company lookup"""
    cccd = request.GET.get('cccd', '').strip()
    
    if not cccd:
        return JsonResponse({
            'success': False,
            'error': 'Vui lòng nhập số CCCD'
        })
    
    if len(cccd) != 12 or not cccd.isdigit():
        return JsonResponse({
            'success': False,
            'error': 'CCCD phải có đúng 12 chữ số'
        })
    
    try:
        employee = Employee.objects.select_related('company').get(
            cccd=cccd,
            is_active=True
        )
        
        # Kiểm tra quyền tra cứu - tất cả user đều có thể tra cứu cross-company
        if not request.user.can_lookup_employee():
            # Log unauthorized access (trong trường hợp user chưa đăng nhập)
            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action='lookup',
                target_cccd=cccd,
                target_employee=employee,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                details={'status': 'unauthorized', 'reason': 'not_authenticated'}
            )
            return JsonResponse({
                'success': False,
                'error': 'Bạn cần đăng nhập để tra cứu thông tin'
            })
        
        # Lấy lịch sử mua hàng
        purchases = PurchaseHistory.objects.filter(
            employee=employee
        ).order_by('-purchase_date')[:50]  # Giới hạn 50 records gần nhất
        
        # Log successful lookup với thông tin cross-company
        lookup_details = {
            'status': 'success',
            'cross_company': employee.company != request.user.company if request.user.company else False,
            'target_company': employee.company.code if employee.company else None,
            'user_company': request.user.company.code if request.user.company else None,
        }
        
        AuditLog.objects.create(
            user=request.user,
            action='lookup',
            target_cccd=cccd,
            target_employee=employee,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            details=lookup_details
        )
        
        # Chỉ trả về thông tin cần thiết cho lịch sử mua hàng
        purchase_data = []
        for purchase in purchases:
            purchase_data.append({
                'product_name': purchase.product_name,
                'purchase_date': purchase.purchase_date.strftime('%d/%m/%Y'),
                'quantity': purchase.quantity,
                'unit_price': float(purchase.unit_price),
                'total_amount': float(purchase.total_amount),
                'description': purchase.description,
            })
        
        # Chỉ trả về thông tin cần thiết cho nhân viên
        data = {
            'success': True,
            'employee': {
                'cccd': employee.cccd,
                'full_name': employee.full_name,
                'birth_date': employee.birth_date.strftime('%d/%m/%Y'),
                'company_name': employee.company.name,
            },
            'purchases': purchase_data,
            'total_purchases': len(purchase_data),
            'cross_company_lookup': employee.company != request.user.company if request.user.company else False,
        }
        
        return JsonResponse(data)
        
    except Employee.DoesNotExist:
        # Log failed lookup
        AuditLog.objects.create(
            user=request.user,
            action='lookup',
            target_cccd=cccd,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            details={'status': 'not_found'}
        )
        
        return JsonResponse({
            'success': False,
            'error': 'Không tìm thấy thông tin nhân viên với số CCCD này'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Có lỗi xảy ra. Vui lòng thử lại sau.'
        })

def get_client_ip(request):
    """Helper function để lấy IP address của client"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
