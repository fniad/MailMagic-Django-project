from django import forms
from client.models import MailClient
from mailing.forms import StyleFormMixin
from django.core.exceptions import ValidationError


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailClient
        fields = '__all__'
        exclude = ('owner',)

    def clean_email(self):
        email = self.cleaned_data['email']
        owner = self.instance.owner

        existing_client = MailClient.objects.filter(email=email, owner=owner).exclude(pk=self.instance.pk)

        if existing_client.exists():
            raise forms.ValidationError('Клиент с таким email уже существует у вас.')

        return email
