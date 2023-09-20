from django.contrib import admin
from .models import Lumber, Length, Invitation

# Register your models here.
admin.site.register(Lumber)
admin.site.register(Length)
admin.site.register(Invitation)