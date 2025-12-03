from django.contrib import admin
from .models import QRCodeItem
@admin.register(QRCodeItem)
class QRCodeItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'data', 'created_at')
    list_filter = ('created_at', 'user')
