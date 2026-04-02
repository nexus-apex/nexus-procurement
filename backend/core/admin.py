from django.contrib import admin
from .models import Vendor, PurchaseOrder, Requisition

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ["name", "contact_person", "email", "phone", "category", "created_at"]
    list_filter = ["status"]
    search_fields = ["name", "contact_person", "email"]

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ["po_number", "vendor_name", "total", "status", "order_date", "created_at"]
    list_filter = ["status"]
    search_fields = ["po_number", "vendor_name"]

@admin.register(Requisition)
class RequisitionAdmin(admin.ModelAdmin):
    list_display = ["title", "requested_by", "department", "estimated_cost", "status", "created_at"]
    list_filter = ["status", "priority"]
    search_fields = ["title", "requested_by", "department"]
