from django.contrib import admin
from .models import Produto, Venda, ItemVenda

# Register your models here.
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descricao', 'valor', 'comissao']

class ItemVendaInline(admin.TabularInline):
    model = ItemVenda

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    inlines = [ItemVendaInline]