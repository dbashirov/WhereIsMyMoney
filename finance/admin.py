from django import forms
from django.contrib import admin
from .models import Currency, Wallet, Category, Operation
from .forms import OperationCreateForm

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user",)

class OperationAdmin(admin.ModelAdmin):
    form = OperationCreateForm

admin.site.register(Currency)
admin.site.register(Wallet)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Operation, OperationAdmin)
