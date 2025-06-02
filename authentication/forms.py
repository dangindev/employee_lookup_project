from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Div, HTML
from crispy_forms.bootstrap import FormActions

class CustomLoginForm(AuthenticationForm):
    ACCOUNT_TYPE_CHOICES = [
        ('system', 'System Account'),
        ('ttgroup', 'TTGroup Account'),
    ]
    
    account_type = forms.ChoiceField(
        choices=ACCOUNT_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label="Loại tài khoản",
        initial='system'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<div class="text-center mb-4"><h3>Đăng nhập hệ thống</h3></div>'),
            Field('account_type', css_class='mb-3'),
            Field('username', placeholder='Tên đăng nhập', css_class='form-control-lg'),
            Field('password', placeholder='Mật khẩu', css_class='form-control-lg'),
            FormActions(
                Submit('submit', 'Đăng nhập', css_class='btn btn-primary btn-lg w-100')
            )
        )
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        account_type = self.cleaned_data.get('account_type')
        
        if username and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
                account_type=account_type
            )
            if self.user_cache is None:
                if account_type == 'ttgroup':
                    raise forms.ValidationError(
                        "Tài khoản LDAP không hợp lệ hoặc không có quyền truy cập hệ thống. "
                        "Vui lòng liên hệ admin để được cấp quyền."
                    )
                else:
                    raise forms.ValidationError("Tên đăng nhập hoặc mật khẩu không đúng.")
            else:
                self.confirm_login_allowed(self.user_cache)
        
        return self.cleaned_data
