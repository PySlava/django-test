from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError

from .models import Category, Husband, Man


@deconstructible
class UkValidator:
    ALLOWED_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789- "
    code = 'ukraine'

    def __init__(self, message=None):
        self.message = message if message else "Be must only english simbols, hyphen or space"

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)

class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='category', empty_label='category dont agree')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label='husband', empty_label='dont have husband')

    class Meta:
        model = Man
        fields = ['title', 'slug', 'content', 'photo', 'is_active', 'cat', 'husband', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels = {'slug': 'URL'}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Length is more than 50 characters')

        return title

class UploadFileForm(forms.Form):
    file = forms.ImageField(label='FILE')
