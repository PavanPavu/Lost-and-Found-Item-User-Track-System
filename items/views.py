from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Item, ItemRequest
from .forms import ItemForm, ItemRequestForm, ItemFilterForm, RequestFilterForm
from django.db import transaction
from django.urls import reverse

def is_admin(user):
    return user.role == 'admin'

# Admin Views
@login_required
@user_passes_test(is_admin)
def admin_items_list(request):
    form = ItemFilterForm(request.GET)
    items = Item.objects.all().order_by('-date_found')
    
    if form.is_valid() and form.cleaned_data['status']:
        items = items.filter(status=form.cleaned_data['status'])
    
    return render(request, 'items/admin_items_list.html', {
        'items': items,
        'form': form
    })

@login_required
@user_passes_test(is_admin)
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item created successfully!')
            return redirect('admin_items_list')
    else:
        form = ItemForm()
    
    return render(request, 'items/item_form.html', {
        'form': form,
        'title': 'Add New Item'
    })

@login_required
@user_passes_test(is_admin)
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('admin_items_list')
    else:
        form = ItemForm(instance=item)
    
    return render(request, 'items/item_form.html', {
        'form': form,
        'title': 'Edit Item',
        'item': item
    })

@login_required
@user_passes_test(is_admin)
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('admin_items_list')
    return render(request, 'items/item_confirm_delete.html', {'item': item})

@login_required
@user_passes_test(is_admin)
def item_requests_list(request, pk):
    item = get_object_or_404(Item, pk=pk)
    form = RequestFilterForm(request.GET)
    requests = item.requests.all().order_by('-date_requested')
    
    if form.is_valid() and form.cleaned_data['status']:
        requests = requests.filter(status=form.cleaned_data['status'])
    
    return render(request, 'items/item_requests_list.html', {
        'item': item,
        'requests': requests,
        'form': form
    })

@login_required
@user_passes_test(is_admin)
def request_action(request, pk, action):
    item_request = get_object_or_404(ItemRequest, pk=pk)
    
    if item_request.item.status == 'returned':
        messages.error(request, 'This item has already been returned!')
        return redirect('item_requests_list', pk=item_request.item.pk)
    
    with transaction.atomic():
        if action == 'approve':
            item_request.status = 'approved'
            item_request.item.status = 'returned'
            item_request.item.returned_to = item_request.user
            item_request.item.save()
            # Reject all other pending requests
            ItemRequest.objects.filter(item=item_request.item, status='pending').exclude(pk=pk).update(status='rejected')
        elif action == 'reject':
            item_request.status = 'rejected'
        
        item_request.save()
        messages.success(request, f'Request {action}d successfully!')
    
    return redirect('item_requests_list', pk=item_request.item.pk)

# User Views
@login_required
def user_items_list(request):
    form = ItemFilterForm(request.GET)
    items = Item.objects.all().order_by('-date_found')
    
    if form.is_valid() and form.cleaned_data['status']:
        items = items.filter(status=form.cleaned_data['status'])
    
    user_requests = {}
    for req in ItemRequest.objects.filter(user=request.user):
        user_requests[req.item_id] = req.get_status_display()
    
    return render(request, 'items/user_items_list.html', {
        'items': items,
        'form': form,
        'user_requests': user_requests
    })

@login_required
def item_request_create(request, pk):
    item = get_object_or_404(Item, pk=pk)
    
    if item.status == 'returned':
        messages.error(request, 'This item has already been returned!')
        return redirect('user_items_list')
    
    if ItemRequest.objects.filter(item=item, user=request.user).exists():
        messages.error(request, 'You have already submitted a request for this item!')
        return redirect('user_items_list')
    
    if request.method == 'POST':
        form = ItemRequestForm(request.POST)
        if form.is_valid():
            item_request = form.save(commit=False)
            item_request.item = item
            item_request.user = request.user
            item_request.save()
            messages.success(request, 'Your request has been submitted successfully!')
            return redirect('user_items_list')
    else:
        form = ItemRequestForm()
    
    return render(request, 'items/item_request_form.html', {
        'form': form,
        'item': item
    })

@login_required
def user_requests_list(request):
    form = RequestFilterForm(request.GET)
    requests = ItemRequest.objects.filter(user=request.user).order_by('-date_requested')
    
    if form.is_valid() and form.cleaned_data['status']:
        requests = requests.filter(status=form.cleaned_data['status'])
    
    return render(request, 'items/user_requests_list.html', {
        'requests': requests,
        'form': form
    })
