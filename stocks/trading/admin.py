from django.contrib import admin
from .models import Position, Transaction, Balance

# Register your models here.
admin.site.register(Position)   #new
admin.site.register(Transaction)
admin.site.register(Balance)