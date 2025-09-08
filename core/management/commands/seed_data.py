import random
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from users.models import User
from marketplace.models import Category, Product, Tag, Review
from orders.models import Order, OrderItem
from support.models import SupportTicket

class Command(BaseCommand):
    help = 'Seeds the database with a large set of sample data for UltrokPay'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Seeding database with enhanced data...'))
        fake = Faker()

        # Clean up existing data
        self.stdout.write('Deleting old data...')
        User.objects.all().delete()
        Category.objects.all().delete()
        Product.objects.all().delete()
        Tag.objects.all().delete()
        Order.objects.all().delete()
        SupportTicket.objects.all().delete()

        # Create Superuser
        self.stdout.write('Creating superuser...')
        admin_user = User.objects.create_superuser('admin', 'admin@ultrokpay.com', 'adminpassword', role=User.Role.ADMIN, is_active=True)

        # Create Users
        self.stdout.write('Creating users...')
        buyers = [User.objects.create_user(f'buyer{i}', f'buyer{i}@example.com', 'password123', role=User.Role.BUYER, is_active=True) for i in range(10)]
        sellers = [User.objects.create_user(f'seller{i}', f'seller{i}@example.com', 'password123', role=User.Role.SELLER, kyc_status=User.KYCStatus.VERIFIED, is_active=True) for i in range(5)]

        # Create Categories and Tags
        self.stdout.write('Creating categories and tags...')
        tags = [Tag.objects.create(name=name) for name in ['Python', 'JavaScript', 'Sci-Fi', 'Fantasy', 'Mobile', 'Fashion', 'Home Decor', 'Gadget', 'Productivity', 'Art']]

        cat_digital = Category.objects.create(name='Digital Products')
        cat_ebooks = Category.objects.create(name='Ebooks', parent=cat_digital)
        cat_software = Category.objects.create(name='Software', parent=cat_digital)
        cat_courses = Category.objects.create(name='Online Courses', parent=cat_digital)

        cat_physical = Category.objects.create(name='Physical Goods')
        cat_electronics = Category.objects.create(name='Electronics', parent=cat_physical)
        cat_clothing = Category.objects.create(name='Clothing', parent=cat_physical)
        cat_home = Category.objects.create(name='Home & Garden', parent=cat_physical)

        categories = [cat_ebooks, cat_software, cat_courses, cat_electronics, cat_clothing, cat_home]

        # Create Products
        self.stdout.write('Creating products...')
        products = []
        for i in range(30):
            seller = random.choice(sellers)
            category = random.choice(categories)
            product_type = 'DIGITAL' if category.parent == cat_digital else 'PHYSICAL'
            product = Product.objects.create(
                product_type=product_type,
                seller=seller,
                category=category,
                title=fake.company() + ' ' + ('Software' if product_type == 'DIGITAL' else 'Device'),
                description=fake.paragraph(nb_sentences=5),
                price_usd=random.uniform(5.0, 1500.0),
                currency_preference=random.choice(['PI', 'SIDRA'])
            )
            product.tags.set(random.sample(tags, k=random.randint(1, 3)))
            products.append(product)

        # Create Orders, Reviews, and Support Tickets
        self.stdout.write('Creating orders, reviews, and tickets...')
        for buyer in buyers:
            for _ in range(random.randint(1, 5)): # Each buyer makes 1-5 orders
                product_to_buy = random.choice(products)
                order = Order.objects.create(
                    buyer=buyer,
                    total_price_usd=product_to_buy.price_usd,
                    status=random.choice(['PAID', 'DELIVERED'])
                )
                OrderItem.objects.create(order=order, product=product_to_buy, quantity=1, price_at_purchase_usd=product_to_buy.price_usd)

                # Create a review for some orders
                if random.random() > 0.5:
                    Review.objects.create(
                        product=product_to_buy,
                        user=buyer,
                        order=order,
                        rating=random.randint(3, 5),
                        comment=fake.sentence()
                    )

                # Create a support ticket for some orders
                if random.random() > 0.7:
                    SupportTicket.objects.create(
                        user=buyer,
                        order=order,
                        title=f'Issue with order #{order.id}',
                        priority=random.choice(['LOW', 'MEDIUM', 'HIGH'])
                    )

        self.stdout.write(self.style.SUCCESS('Enhanced database seeding complete!'))
