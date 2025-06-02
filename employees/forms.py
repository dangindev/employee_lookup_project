# employees/forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from crispy_forms.bootstrap import FormActions

class EmployeeLookupForm(forms.Form):
    cccd = forms.CharField(
        max_length=12,
        label="Số căn cước công dân",
        widget=forms.TextInput(attrs={
            'placeholder': 'Nhập 12 chữ số CCCD',
            'pattern': '[0-9]{12}',
            'title': 'CCCD phải có đúng 12 chữ số'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_id = 'lookup-form'
        self.helper.layout = Layout(
            Field('cccd', css_class='form-control-lg'),
            FormActions(
                Submit('submit', 'Tra cứu', css_class='btn btn-primary btn-lg')
            )
        )
    
    def clean_cccd(self):
        cccd = self.cleaned_data.get('cccd')
        if cccd and not cccd.isdigit():
            raise forms.ValidationError("CCCD chỉ được chứa chữ số.")
        if cccd and len(cccd) != 12:
            raise forms.ValidationError("CCCD phải có đúng 12 chữ số.")
        return cccd