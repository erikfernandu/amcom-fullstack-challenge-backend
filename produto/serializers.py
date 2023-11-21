# -*- coding: utf-8 -*-
from django.db.models import Sum, F, Value, ExpressionWrapper, fields
from django.db.models.functions import Coalesce
from rest_framework import serializers
from .models import Produto, Venda, ItemVenda, Vendedor

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['codigo', 'descricao', 'valor', 'comissao']

class ItemVendaSerializer(serializers.ModelSerializer):
    produto = ProdutoSerializer(read_only=True)
    class Meta:
        model = ItemVenda
        fields = ['produto', 'quantidade']

class VendaSerializer(serializers.ModelSerializer):
    cliente = serializers.CharField(source='cliente.nome', read_only=True)
    vendedor = serializers.CharField(source='vendedor.nome', read_only=True)
    dataehora = serializers.DateTimeField(format='%d/%m/%Y - %H:%M:%S', read_only=True)
    itemvenda_set = ItemVendaSerializer(many=True)
    valor_total = serializers.DecimalField(max_digits=9, decimal_places=2, localize=True)
    total_itens = serializers.SerializerMethodField()
    class Meta:
        model = Venda
        fields = ['id', 'num_notafiscal', 'dataehora', 'cliente', 'vendedor', 'itemvenda_set', 'valor_total', 'total_itens']
    
    def get_total_itens(self, obj):
        total = Venda.objects.filter(id=obj.id).annotate(total_itens=Sum('itemvenda__quantidade')).values('total_itens')[0]['total_itens']
        return total

class ComissoesSerializer(serializers.ModelSerializer):
    vendas = VendaSerializer(many=True, read_only=True)
    total_vendas = serializers.SerializerMethodField()
    total_comissoes = serializers.SerializerMethodField()

    class Meta:
        model = Vendedor
        fields = ['id', 'codigo', 'nome', 'total_vendas', 'total_comissoes']
    
    def get_total_vendas(self, obj):
        vendas = Venda.objects.filter(vendedor=obj)
        total_vendas = sum(venda.valor_total for venda in vendas if venda.valor_total is not None)
        return total_vendas
    
    def get_total_comissoes(self, obj):
        produtos_vendidos = ItemVenda.objects.filter(venda__vendedor=obj)
        total_comissoes = sum((item.produto.valor * item.produto.comissao / 100) * item.quantidade for item in produtos_vendidos if item.produto.valor is not None and item.produto.comissao is not None)
        return total_comissoes