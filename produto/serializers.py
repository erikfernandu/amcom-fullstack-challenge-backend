# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Produto, Venda

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'codigo', 'descricao', 'valor', 'comissao']

class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = ['id', 'num_notafiscal', 'dataehora', 'cliente', 'vendedor', 'produtos', 'itemvenda_set', 'valor_total']

class VendasSerializer(serializers.ModelSerializer):
    cliente = serializers.CharField(source='cliente.nome', read_only=True)
    vendedor = serializers.CharField(source='vendedor.nome', read_only=True)
    dataehora = serializers.DateTimeField(format='%d/%m/%Y - %H:%M:%S', read_only=True)
    valor_total = serializers.DecimalField(max_digits=9, decimal_places=2, localize=True)
    class Meta:
        model = Venda
        fields = ['id', 'num_notafiscal', 'dataehora', 'cliente', 'vendedor', 'produtos', 'itemvenda_set', 'valor_total']

class ComissoesSerializer(serializers.ModelSerializer):
    # vendedor = serializers.CharField(source='vendedor.nome', read_only=True)
    class Meta:
        model = Venda
        fields = ['vendedor_id', 'valor_total']