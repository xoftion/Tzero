import random
from django.core.management.base import BaseCommand
from django.db import transaction
from users.models import User
from marketplace.models import Category, Product, Tag

class Command(BaseCommand):
    help = 'Seeds the database with sample data for UltrokPay'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Seeding database...'))

        # Clean up existing data
        self.stdout.write('Deleting old data...')
        User.objects.all().delete()
        Category.objects.all().delete()
        Product.objects.all().delete()
        Tag.objects.all().delete()

        # Create Superuser
        self.stdout.write('Creating superuser...')
        User.objects.create_superuser(
            username='admin',
            email='admin@ultrokpay.com',
            password='adminpassword',
            role=User.Role.ADMIN
        )

        # Create Users
        self.stdout.write('Creating users...')
        buyer1 = User.objects.create_user(username='buyer1', email='buyer1@example.com', password='password123', role=User.Role.BUYER)
        seller1 = User.objects.create_user(username='seller1', email='seller1@example.com', password='password123', role=User.Role.SELLER, kyc_status=User.KYCStatus.VERIFIED)
        seller2 = User.objects.create_user(username='seller2', email='seller2@example.com', password='password123', role=User.Role.SELLER, kyc_status=User.KYCStatus.VERIFIED)

        # Create Categories
        self.stdout.write('Creating categories...')
        cat_digital = Category.objects.create(name='Digital Products')
        cat_ebooks = Category.objects.create(name='Ebooks', parent=cat_digital)
        cat_software = Category.objects.create(name='Software', parent=cat_digital)

        cat_physical = Category.objects.create(name='Physical Goods')
        cat_electronics = Category.objects.create(name='Electronics', parent=cat_physical)
        cat_clothing = Category.objects.create(name='Clothing', parent=cat_physical)

        # Create Tags
        self.stdout.write('Creating tags...')
        tag_python = Tag.objects.create(name='Python')
        tag_django = Tag.objects.create(name='Django')
        tag_fiction = Tag.objects.create(name='Fiction')
        tag_mobile = Tag.objects.create(name='Mobile')
        tag_fashion = Tag.objects.create(name='Fashion')

        # Create Products
        self.stdout.write('Creating products...')

        # Digital Products
        p1 = Product.objects.create(
            product_type='DIGITAL', seller=seller1, category=cat_software,
            title='Pro Web Analytics Tool', description='A powerful SaaS for tracking website performance.',
            price_usd=49.99, currency_preference='PI'
        )
        p1.tags.add(tag_python, tag_django)

        p2 = Product.objects.create(
            product_type='DIGITAL', seller=seller2, category=cat_ebooks,
            title='The Last Starlight: A Sci-Fi Novel', description='A thrilling journey across the galaxy.',
            price_usd=9.99, currency_preference='SIDRA'
        )
        p2.tags.add(tag_fiction)

        # Physical Products
        p3 = Product.objects.create(
            product_type='PHYSICAL', seller=seller1, category=cat_electronics,
            title='Quantum Core Smartphone', description='The latest smartphone with a quantum processor.',
            price_usd=899.99, currency_preference='PI'
        )
        p3.tags.add(tag_mobile)

        p4 = Product.objects.create(
            product_type='PHYSICAL', seller=seller2, category=cat_clothing,
            title='Designer Silk Scarf', description='A beautiful hand-made silk scarf.',
            price_usd=75.00, currency_preference='SIDRA'
        )
        p4.tags.add(tag_fashion)

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
