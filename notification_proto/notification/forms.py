from django import forms
from django.contrib.auth.models import User


class SendMsgForm(forms.Form):
    recipient = forms.ModelChoiceField(queryset=User.objects.all())
    message = forms.CharField()
