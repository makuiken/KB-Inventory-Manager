from django.contrib import admin
from .models import Lumber, Length, Invitation, Sale, ChangeLog

# Register your models here.
admin.site.register(Lumber)
admin.site.register(Length)
admin.site.register(Invitation)
admin.site.register(Sale)
admin.site.register(ChangeLog)