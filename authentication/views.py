from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomLoginForm

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'authentication/login.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Chào mừng {self.request.user.get_full_name() or self.request.user.username}!')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Đăng nhập không thành công. Vui lòng kiểm tra lại thông tin.')
        return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'Bạn đã đăng xuất thành công.')
        return super().dispatch(request, *args, **kwargs)

@login_required
def profile_view(request):
    return render(request, 'authentication/profile.html', {
        'user': request.user
    })
