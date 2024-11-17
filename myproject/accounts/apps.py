from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        post_migrate.connect(create_superuser_after_migrations, sender=self)


def create_superuser_after_migrations(sender, **kwargs):
    call_command('createcustomsuperuser')
