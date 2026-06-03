from django import forms
from .models import ContactInquiry, DemoRequest

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = [
            'name', 'email', 'phone', 'company', 'country',
            'inquiry_type', 'subject', 'message',
        ]
        widgets = {
            'name':         forms.TextInput(attrs={'placeholder': 'Họ và tên *'}),
            'email':        forms.EmailInput(attrs={'placeholder': 'Email *'}),
            'phone':        forms.TextInput(attrs={'placeholder': 'Số điện thoại'}),
            'company':      forms.TextInput(attrs={'placeholder': 'Tên công ty'}),
            'country':      forms.TextInput(attrs={'placeholder': 'Quốc gia'}),
            'subject':      forms.TextInput(attrs={'placeholder': 'Tiêu đề *'}),
            'message':      forms.Textarea(attrs={'placeholder': 'Nội dung tin nhắn *', 'rows': 5}),
            'inquiry_type': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', (
                'w-full bg-slate-900 border border-slate-700 text-slate-200 text-sm '
                'px-4 py-3 rounded-xl placeholder-slate-600 '
                'focus:outline-none focus:border-brand-600 focus:ring-1 '
                'focus:ring-brand-700 transition-colors'
            ))

        self.fields['inquiry_type'].widget.attrs['class'] = (
            'w-full bg-slate-900 border border-slate-700 text-slate-200 text-sm '
            'px-4 py-3 rounded-xl '
            'focus:outline-none focus:border-brand-600 focus:ring-1 '
            'focus:ring-brand-700 transition-colors'
        )

class DemoRequestForm(forms.ModelForm):
    class Meta:
        model = DemoRequest
        fields = [
            'name', 'email', 'phone', 'company',
            'job_title', 'country', 'solution',
            'preferred_date', 'message',
        ]
        
        widgets = {
            'name':           forms.TextInput(attrs={'placeholder': 'Họ và tên *'}),
            'email':          forms.EmailInput(attrs={'placeholder': 'Email *'}),
            'phone':          forms.TextInput(attrs={'placeholder': 'Số điện thoại'}),
            'company':        forms.TextInput(attrs={'placeholder': 'Tên công ty'}),
            'job_title':      forms.TextInput(attrs={'placeholder': 'Chức danh'}),
            'country':        forms.TextInput(attrs={'placeholder': 'Quốc gia'}),
            'solution':       forms.Select(),
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
            'message':        forms.Textarea(attrs={
                'placeholder': 'Mô tả nhu cầu demo của bạn...', 'rows': 4,
            }),
        }
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_cls = (
            'w-full bg-slate-900 border border-slate-700 text-slate-200 text-sm '
            'px-4 py-3 rounded-xl placeholder-slate-600 '
            'focus:outline-none focus:border-brand-600 focus:ring-1 '
            'focus:ring-brand-700 transition-colors'
        )
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', base_cls)
        self.fields['solution'].required = False
        self.fields['preferred_date'].required = False