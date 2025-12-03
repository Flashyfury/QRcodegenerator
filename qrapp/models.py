from django.db import models
from django.contrib.auth.models import User
class QRCodeItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='qrcodes', null=True, blank=True)
    data = models.TextField()
    fg_color = models.CharField(max_length=7, default='#000000')
    bg_color = models.CharField(max_length=7, default='#FFFFFF')
    size = models.PositiveIntegerField(default=300)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    image = models.ImageField(upload_to='qrs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'QR {self.id} - {self.data[:20]}'
