from django import forms
from django.contrib.auth.models import User
from .models import ProblemReport, ProblemPhoto, ProblemResponse

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ProblemReportForm(forms.ModelForm):
    photos = MultipleFileField(
        required=False,
        help_text='Upload multiple photos of the problem (JPG, PNG, GIF)'
    )
    
    class Meta:
        model = ProblemReport
        fields = ['title', 'description', 'problem_type', 'priority', 'location', 'phone_number']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief description of your bike problem'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your problem in detail...'
            }),
            'problem_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your current location (e.g., Dhanmondi, Dhaka)'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your contact number'
            }),
        }
        help_texts = {
            'title': 'Give a brief title for your problem',
            'description': 'Describe what happened and when',
            'problem_type': 'Select the type of problem',
            'priority': 'How urgent is this problem?',
            'location': 'Where did this problem occur?',
            'phone_number': 'We may need to contact you for more details',
        }

class ProblemResponseForm(forms.ModelForm):
    class Meta:
        model = ProblemResponse
        fields = ['message', 'is_solution']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Type your response to the user...'
            }),
            'is_solution': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        help_texts = {
            'message': 'Provide helpful information or solution to the user',
            'is_solution': 'Check if this response solves the problem',
        }

class ProblemReportUpdateForm(forms.ModelForm):
    class Meta:
        model = ProblemReport
        fields = ['status', 'assigned_agent', 'assigned_center', 'priority']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'assigned_agent': forms.Select(attrs={
                'class': 'form-select'
            }),
            'assigned_center': forms.Select(attrs={
                'class': 'form-select'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

