from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Vendor, PurchaseOrder, Requisition
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusProcurement with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexusprocurement.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Vendor.objects.count() == 0:
            for i in range(10):
                Vendor.objects.create(
                    name=f"Sample Vendor {i+1}",
                    contact_person=f"Sample {i+1}",
                    email=f"demo{i+1}@example.com",
                    phone=f"+91-98765{43210+i}",
                    category=f"Sample {i+1}",
                    rating=round(random.uniform(1000, 50000), 2),
                    status=random.choice(["active", "blacklisted", "pending_approval"]),
                    payment_terms=f"Sample {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Vendor records created'))

        if PurchaseOrder.objects.count() == 0:
            for i in range(10):
                PurchaseOrder.objects.create(
                    po_number=f"Sample {i+1}",
                    vendor_name=f"Sample PurchaseOrder {i+1}",
                    total=round(random.uniform(1000, 50000), 2),
                    status=random.choice(["draft", "submitted", "approved", "received", "cancelled"]),
                    order_date=date.today() - timedelta(days=random.randint(0, 90)),
                    delivery_date=date.today() - timedelta(days=random.randint(0, 90)),
                    items_count=random.randint(1, 100),
                    notes=f"Sample notes for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 PurchaseOrder records created'))

        if Requisition.objects.count() == 0:
            for i in range(10):
                Requisition.objects.create(
                    title=f"Sample Requisition {i+1}",
                    requested_by=f"Sample {i+1}",
                    department=f"Sample {i+1}",
                    estimated_cost=round(random.uniform(1000, 50000), 2),
                    status=random.choice(["draft", "submitted", "approved", "rejected", "ordered"]),
                    priority=random.choice(["low", "medium", "high", "urgent"]),
                    date=date.today() - timedelta(days=random.randint(0, 90)),
                )
            self.stdout.write(self.style.SUCCESS('10 Requisition records created'))
