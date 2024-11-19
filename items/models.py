from django.db import models
from accounts.models import CustomUser

class Item(models.Model):
    STATUS_CHOICES = (
        ('lost', 'Lost'),
        ('returned', 'Returned'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='lost_items/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='lost')
    date_found = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    returned_to = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='returned_items'
    )

    def __str__(self):
        return self.title

class ItemRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='requests')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reason = models.TextField(help_text='Please explain why this item belongs to you')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    date_requested = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['item', 'user']  # A user can only make one request per item

    def __str__(self):
        return f"{self.user.username}'s request for {self.item.title}"
