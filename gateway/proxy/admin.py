from django.contrib import admin
from .models import RequestLog, APIKey

# Register your models here.

admin.site.register(RequestLog)
admin.site.register(APIKey)
