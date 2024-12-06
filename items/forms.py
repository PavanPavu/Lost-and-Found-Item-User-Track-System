from django import forms
from .models import Item, ItemRequest

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        # fields = ['title', 'description']
        fields = ['title', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ItemRequestForm(forms.ModelForm):
    class Meta:
        model = ItemRequest
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4}),
        }

class ItemFilterForm(forms.Form):
    STATUS_CHOICES = (
        ('', 'All'),
        ('lost', 'Lost'),
        ('returned', 'Returned'),
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)

class RequestFilterForm(forms.Form):
    STATUS_CHOICES = (
        ('', 'All'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)