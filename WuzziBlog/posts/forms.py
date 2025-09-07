from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

# ----- Updated PostForm -----
class PostForm(forms.ModelForm):
    # This line makes the image field optional and uses the correct widget for "Clear" functionality.
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput)

    class Meta:
        model = Post
        fields = ["title", "content", "image", "category", "published", 'image_url', 'image_caption']
    
    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        image_url = cleaned_data.get('image_url')

        # Custom validation: ensure only one image source is provided
        if image and image_url:
            raise ValidationError("Please provide either an uploaded image or an image URL, but not both.")
        
        return cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...',
                'required': True,
                'minlength': 1
            })
        }
        labels = {
            'content': ''
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise forms.ValidationError('Comment cannot be empty')
        if len(content) < 1:
            raise forms.ValidationError('Comment is too short')
        return content