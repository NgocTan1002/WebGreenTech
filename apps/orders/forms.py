from django import forms
from .models import QuoteRequest


_input_cls = (
    'w-full bg-slate-900 border border-slate-700 text-slate-200 text-sm '
    'px-4 py-3 rounded-xl placeholder-slate-600 '
    'focus:outline-none focus:border-brand-600 focus:ring-1 '
    'focus:ring-brand-700 transition-colors'
)


class CheckoutForm(forms.Form):
    email         = forms.EmailField()
    first_name    = forms.CharField(max_length=150)
    last_name     = forms.CharField(max_length=150)
    company_name  = forms.CharField(max_length=300, required=False)
    phone         = forms.CharField(max_length=30, required=False)
    address_line1 = forms.CharField(max_length=300, required=False)  # tên đường/tòa nhà
    address_line2 = forms.CharField(max_length=300, required=False)  # phường
    city          = forms.CharField(max_length=100, required=False)  # thành phố/tỉnh
    notes         = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    po_number     = forms.CharField(max_length=100, required=False, label='PO Number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', _input_cls)

    def clean(self):
        cleaned = super().clean()
        cleaned['shipping_address'] = {
            'address_line1': cleaned.get('address_line1', ''),  # tên đường/tòa nhà
            'address_line2': cleaned.get('address_line2', ''),  # phường
            'city':          cleaned.get('city', ''),           # thành phố/tỉnh
        }
        cleaned['billing_address'] = cleaned['shipping_address']
        return cleaned

class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model  = QuoteRequest
        fields = [
            'name', 'email', 'phone', 'company',
            'solution', 'application', 'message',
        ]
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Mô tả yêu cầu dự án, số lượng cần thiết và các thông số kỹ thuật cụ thể...',
            }),
            'application': forms.TextInput(attrs={
                'placeholder': 'VD: Nhà kính thông minh, Giám sát nhà máy...',
            }),
            'solution': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', _input_cls)
        self.fields['solution'].required    = False
        self.fields['phone'].required       = False
        self.fields['company'].required     = False
        self.fields['application'].required = False