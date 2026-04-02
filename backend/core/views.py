import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Vendor, PurchaseOrder, Requisition


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['vendor_count'] = Vendor.objects.count()
    ctx['vendor_active'] = Vendor.objects.filter(status='active').count()
    ctx['vendor_blacklisted'] = Vendor.objects.filter(status='blacklisted').count()
    ctx['vendor_pending_approval'] = Vendor.objects.filter(status='pending_approval').count()
    ctx['vendor_total_rating'] = Vendor.objects.aggregate(t=Sum('rating'))['t'] or 0
    ctx['purchaseorder_count'] = PurchaseOrder.objects.count()
    ctx['purchaseorder_draft'] = PurchaseOrder.objects.filter(status='draft').count()
    ctx['purchaseorder_submitted'] = PurchaseOrder.objects.filter(status='submitted').count()
    ctx['purchaseorder_approved'] = PurchaseOrder.objects.filter(status='approved').count()
    ctx['purchaseorder_total_total'] = PurchaseOrder.objects.aggregate(t=Sum('total'))['t'] or 0
    ctx['requisition_count'] = Requisition.objects.count()
    ctx['requisition_draft'] = Requisition.objects.filter(status='draft').count()
    ctx['requisition_submitted'] = Requisition.objects.filter(status='submitted').count()
    ctx['requisition_approved'] = Requisition.objects.filter(status='approved').count()
    ctx['requisition_total_estimated_cost'] = Requisition.objects.aggregate(t=Sum('estimated_cost'))['t'] or 0
    ctx['recent'] = Vendor.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def vendor_list(request):
    qs = Vendor.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'vendor_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def vendor_create(request):
    if request.method == 'POST':
        obj = Vendor()
        obj.name = request.POST.get('name', '')
        obj.contact_person = request.POST.get('contact_person', '')
        obj.email = request.POST.get('email', '')
        obj.phone = request.POST.get('phone', '')
        obj.category = request.POST.get('category', '')
        obj.rating = request.POST.get('rating') or 0
        obj.status = request.POST.get('status', '')
        obj.payment_terms = request.POST.get('payment_terms', '')
        obj.save()
        return redirect('/vendors/')
    return render(request, 'vendor_form.html', {'editing': False})


@login_required
def vendor_edit(request, pk):
    obj = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.contact_person = request.POST.get('contact_person', '')
        obj.email = request.POST.get('email', '')
        obj.phone = request.POST.get('phone', '')
        obj.category = request.POST.get('category', '')
        obj.rating = request.POST.get('rating') or 0
        obj.status = request.POST.get('status', '')
        obj.payment_terms = request.POST.get('payment_terms', '')
        obj.save()
        return redirect('/vendors/')
    return render(request, 'vendor_form.html', {'record': obj, 'editing': True})


@login_required
def vendor_delete(request, pk):
    obj = get_object_or_404(Vendor, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/vendors/')


@login_required
def purchaseorder_list(request):
    qs = PurchaseOrder.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(po_number__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'purchaseorder_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def purchaseorder_create(request):
    if request.method == 'POST':
        obj = PurchaseOrder()
        obj.po_number = request.POST.get('po_number', '')
        obj.vendor_name = request.POST.get('vendor_name', '')
        obj.total = request.POST.get('total') or 0
        obj.status = request.POST.get('status', '')
        obj.order_date = request.POST.get('order_date') or None
        obj.delivery_date = request.POST.get('delivery_date') or None
        obj.items_count = request.POST.get('items_count') or 0
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/purchaseorders/')
    return render(request, 'purchaseorder_form.html', {'editing': False})


@login_required
def purchaseorder_edit(request, pk):
    obj = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        obj.po_number = request.POST.get('po_number', '')
        obj.vendor_name = request.POST.get('vendor_name', '')
        obj.total = request.POST.get('total') or 0
        obj.status = request.POST.get('status', '')
        obj.order_date = request.POST.get('order_date') or None
        obj.delivery_date = request.POST.get('delivery_date') or None
        obj.items_count = request.POST.get('items_count') or 0
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/purchaseorders/')
    return render(request, 'purchaseorder_form.html', {'record': obj, 'editing': True})


@login_required
def purchaseorder_delete(request, pk):
    obj = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/purchaseorders/')


@login_required
def requisition_list(request):
    qs = Requisition.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'requisition_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def requisition_create(request):
    if request.method == 'POST':
        obj = Requisition()
        obj.title = request.POST.get('title', '')
        obj.requested_by = request.POST.get('requested_by', '')
        obj.department = request.POST.get('department', '')
        obj.estimated_cost = request.POST.get('estimated_cost') or 0
        obj.status = request.POST.get('status', '')
        obj.priority = request.POST.get('priority', '')
        obj.date = request.POST.get('date') or None
        obj.save()
        return redirect('/requisitions/')
    return render(request, 'requisition_form.html', {'editing': False})


@login_required
def requisition_edit(request, pk):
    obj = get_object_or_404(Requisition, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '')
        obj.requested_by = request.POST.get('requested_by', '')
        obj.department = request.POST.get('department', '')
        obj.estimated_cost = request.POST.get('estimated_cost') or 0
        obj.status = request.POST.get('status', '')
        obj.priority = request.POST.get('priority', '')
        obj.date = request.POST.get('date') or None
        obj.save()
        return redirect('/requisitions/')
    return render(request, 'requisition_form.html', {'record': obj, 'editing': True})


@login_required
def requisition_delete(request, pk):
    obj = get_object_or_404(Requisition, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/requisitions/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['vendor_count'] = Vendor.objects.count()
    data['purchaseorder_count'] = PurchaseOrder.objects.count()
    data['requisition_count'] = Requisition.objects.count()
    return JsonResponse(data)
