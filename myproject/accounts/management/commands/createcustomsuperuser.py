from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Создаёт суперпользователя, если он ещё не существует'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        try:
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='adminpassword'
                )
                self.stdout.write(self.style.SUCCESS('Суперпользователь успешно создан'))
            else:
                self.stdout.write(self.style.WARNING('Суперпользователь уже существует'))
        except IntegrityError:
            self.stdout.write(self.style.ERROR('Ошибка при создании суперпользователя'))
