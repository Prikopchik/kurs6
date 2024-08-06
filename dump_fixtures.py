import os
import json
from django.core.management import call_command
from django.conf import settings

fixture_path = os.path.join(settings.BASE_DIR, 'catalog', 'fixtures', 'catalog_data.json')

with open(fixture_path, 'w', encoding='utf-8') as f:
    call_command('dumpdata', 'catalog', stdout=f)
