from django.core.management.base import BaseCommand
from catalog.models import Category, Product
import json
import os


class Command(BaseCommand):
    help = 'Load categories and products from fixtures'

    @staticmethod
    def json_read_categories():
        fixture_path = os.path.join(
            'myproject', 'catalog', 'fixtures', 'categories.json')
        with open(fixture_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def json_read_products():
        fixture_path = os.path.join(
            'myproject', 'catalog', 'fixtures', 'products.json')
        with open(fixture_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def handle(self, *args, **options):
        self.stdout.write('Clearing old data...')
        Product.objects.all().delete()
        Category.objects.all().delete()

        product_for_create = []
        category_for_create = []

        self.stdout.write('Loading categories...')
        for category_data in Command.json_read_categories():
            category_for_create.append(
                Category(
                    name=category_data['fields']['name'],
                    description=category_data['fields'].get('description', '')
                )
            )
        Category.objects.bulk_create(category_for_create)

        self.stdout.write('Loading products...')
        for product_data in Command.json_read_products():
            product_for_create.append(
                Product(
                    name=product_data['fields']['name'],
                    description=product_data['fields'].get('description', ''),
                    price=product_data['fields']['price'],
                    category=Category.objects.get(
                        pk=product_data['fields']['category']),
                )
            )
        Product.objects.bulk_create(product_for_create)

        self.stdout.write(self.style.SUCCESS(
            'Successfully loaded categories and products'))