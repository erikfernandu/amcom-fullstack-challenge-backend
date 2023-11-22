# -*- coding: utf-8 -*-
from django.db.models import Sum, Q
from rest_framework import serializers
from .models import Produto, Venda, ItemVenda, Vendedor
from decimal import Decimal

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
    total_itens = serializers.SerializerMethodField()
    valor_total = serializers.SerializerMethodField()
    valor_total_comissoes = serializers.SerializerMethodField()
    class Meta:
        model = Venda
        fields = ['id', 'num_notafiscal', 'dataehora', 'cliente', 'vendedor', 'itemvenda_set', 'valor_total', 'total_itens', 'valor_total_comissoes']
    
    def get_total_itens(self, obj):
        total_itens = Venda.objects.filter(id=obj.id).annotate(total_itens=Sum('itemvenda__quantidade')).values('total_itens')[0]['total_itens']
        return total_itens

    def get_valor_total(self, venda):
        produtos_vendidos = ItemVenda.objects.filter(venda=venda)
        valor_total = sum(item.produto.valor * item.quantidade for item in produtos_vendidos if item.produto.valor is not None)
        return valor_total
    
    def get_valor_total_comissoes(self, venda):
        produtos_vendidos = ItemVenda.objects.filter(venda=venda)
        total_comissoes = sum((item.quantidade * item.produto.valor * item.produto.comissao) / 100 for item in produtos_vendidos if item.produto.valor is not None)
        return total_comissoes

class ComissoesSerializer(serializers.ModelSerializer):
    vendas = VendaSerializer(many=True, read_only=True)
    total_vendas = serializers.SerializerMethodField()
    total_comissoes = serializers.SerializerMethodField()

    class Meta:
        model = Vendedor
        fields = ['id', 'codigo', 'nome', 'vendas', 'total_vendas', 'total_comissoes']
    
    def get_total_vendas(self, obj):
        query = Q()
        if self.context.get('start_date'):
            query &= Q(dataehora__gte=self.context.get('start_date'))
        if self.context.get('end_date'):
            query &= Q(dataehora__lte=self.context.get('end_date'))
        vendas = Venda.objects.filter(vendedor=obj).filter(query)
        total_vendas = sum(Decimal(item.produto.valor) * item.quantidade for venda in vendas for item in ItemVenda.objects.filter(venda=venda) if item.produto.valor is not None )
        return total_vendas
    
    def get_total_comissoes(self, obj):
        query = Q()
        if self.context.get('start_date'):
            query &= Q(venda__dataehora__gte=self.context.get('start_date'))
        if self.context.get('end_date'):
            query &= Q(venda__dataehora__lte=self.context.get('end_date'))
        produtos_vendidos = ItemVenda.objects.filter(venda__vendedor=obj).filter(query)
        total_comissoes = sum((item.produto.valor * item.produto.comissao / 100) * item.quantidade for item in produtos_vendidos if item.produto.valor is not None and item.produto.comissao is not None)
        return total_comissoes