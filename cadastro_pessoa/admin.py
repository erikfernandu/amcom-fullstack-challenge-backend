# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Cliente, Vendedor

# Register your models here.
@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'telefone']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'telefone']