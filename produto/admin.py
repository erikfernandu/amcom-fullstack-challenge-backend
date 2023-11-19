# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Produto, Venda, ItemVenda

# Register your models here.
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descricao', 'valor', 'comissao']

class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 1
    min_num = 1

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ['num_notafiscal', 'cliente', 'vendedor', 'total_venda', 'total_comissao', 'dataehora']
    inlines = [ItemVendaInline]

    def total_venda(self, obj):
        return sum(item.produto.valor * item.quantidade for item in obj.itemvenda_set.all())
    total_venda.short_description = 'Total das vendas'

    def total_comissao(self, obj):
        return sum(item.produto.comissao * (item.produto.valor * item.quantidade) /100 for item in obj.itemvenda_set.all())
    total_comissao.short_description = 'Total das comissões'
