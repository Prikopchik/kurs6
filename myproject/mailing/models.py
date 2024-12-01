from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Recipient(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.email

class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject

class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient)

    def __str__(self):
        return f"Mailing {self.id}: {self.status}"

class MailingAttempt(models.Model):
    ATTEMPT_STATUS = [
        ('success', 'Успешно'),
        ('failure', 'Не успешно'),
    ]

    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=ATTEMPT_STATUS)
    server_response = models.TextField()
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    def __str__(self):
        return f"Attempt for mailing {self.mailing.id} - {self.status}"


class MailingStat(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    successful_attempts = models.IntegerField(default=0)
    failed_attempts = models.IntegerField(default=0)
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE)

    def __str__(self):
        return f'Статистика рассылки для {self.user}'