from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()

class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

from django import forms

class ContactForm(forms.Form):
        name = forms.CharField(label="Введите имя")
        sender = forms.EmailField(label="Email для ответа")
        subject = forms.CharField(label="Тема сообщения", initial='Письмо администратору', max_length=100)
        message = forms.CharField(widget=forms.Textarea)
        cc_myself = forms.BooleanField(label="Отправить себе копию", required=False)