
from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
import re

from polls.models import LogMessage


class LogMessageForm(forms.ModelForm):
    """Form for creating log messages with enhanced validation and widgets."""
    
    class Meta:
        model = LogMessage
        fields = ("message",)
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your message here...',
                'rows': 4,
                'maxlength': 300,
            })
        }
        labels = {
            'message': 'Your Message',
        }
        help_texts = {
            'message': 'Maximum 300 characters. HTML tags will be stripped for security.',
        }

    def clean_message(self):
        """Custom validation for message field."""
        message = self.cleaned_data.get('message')
        
        if not message:
            raise ValidationError("Message cannot be empty.")
        
        message = strip_tags(message)
        
        message = re.sub(r'\s+', ' ', message).strip()
        
        if len(message) < 5:
            raise ValidationError("Message must be at least 5 characters long.")
        
        banned_words = ['spam', 'abuse', 'inappropriate']
        if any(word in message.lower() for word in banned_words):
            raise ValidationError("Message contains inappropriate content.")
        
        return message

    def save(self, commit=True):
        """Override save to add additional processing."""
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


class SearchForm(forms.Form):
    """Form for searching messages."""
    
    query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search messages...',
            'autocomplete': 'off',
        }),
        label='Search Query',
        help_text='Enter keywords to search in messages.'
    )
    
    def clean_query(self):
        """Clean and validate search query."""
        query = self.cleaned_data.get('query')
        
        if not query:
            raise ValidationError("Search query cannot be empty.")
        
        # Strip HTML and normalize whitespace
        query = strip_tags(query).strip()
        
        if len(query) < 2:
            raise ValidationError("Search query must be at least 2 characters long.")
        
        return query


class ContactForm(forms.Form):
    """Example contact form demonstrating various field types."""
    
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('support', 'Technical Support'),
        ('feedback', 'Feedback'),
        ('bug', 'Bug Report'),
    ]
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your full name',
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
        })
    )
    
    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Enter your message here...',
        }),
        help_text='Please provide as much detail as possible.'
    )
    
    urgent = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        label='Mark as urgent'
    )
    
    def clean_email(self):
        """Validate email domain."""
        email = self.cleaned_data.get('email')
        if email:
            domain = email.split('@')[1]
            banned_domains = ['tempmail.com', 'throwaway.email']
            if domain in banned_domains:
                raise ValidationError("Please use a valid email address.")
        return email
    
    def clean(self):
        """Cross-field validation."""
        cleaned_data = super().clean()
        subject = cleaned_data.get('subject')
        urgent = cleaned_data.get('urgent')
        
        # If marked as urgent, require specific subjects
        if urgent and subject not in ['support', 'bug']:
            raise ValidationError("Urgent flag can only be used for support or bug reports.")
        
        return cleaned_data
