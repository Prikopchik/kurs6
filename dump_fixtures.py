import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

django.setup()

fixture_path = os.path.join('myproject', 'catalog', 'fixtures', 'catalog_data.json')

with open(fixture_path, 'w', encoding='utf-8') as f:
    call_command('dumpdata', 'catalog', stdout=f)
