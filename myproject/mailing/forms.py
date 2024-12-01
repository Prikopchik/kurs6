from django import forms
from .models import Message, Mailing

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
        labels = {
            'subject': 'Тема письма',
            'body': 'Тело письма',
        }

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_time', 'end_time', 'status', 'message', 'recipients']
        labels = {
            'start_time': 'Дата и время первой отправки',
            'end_time': 'Дата и время окончания отправки',
            'status': 'Статус',
            'message': 'Сообщение',
            'recipients': 'Получатели',
        }
