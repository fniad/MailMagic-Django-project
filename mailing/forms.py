from django import forms

from client.models import MailClient
from mailing.models import MailingSettings, MailingMessage, MailingLog


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # if user and self.instance:
        #     if not user.is_superuser:
        #         owner = self.instance.owner
        #         self.fields['clients'].queryset = MailClient.objects.filter(owner=owner)

    class Meta:
        model = MailingSettings
        fields = '__all__'
        exclude = ('owner',)


class MailingMessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingMessage
        fields = '__all__'


class MailingLogFilterForm(StyleFormMixin, forms.ModelForm):
    last_attempt_datetime = forms.DateTimeField(required=False)
    status = forms.ChoiceField(choices=MailingLog.STATUS_CHOICES, required=False)
    server_response = forms.CharField(required=False)
