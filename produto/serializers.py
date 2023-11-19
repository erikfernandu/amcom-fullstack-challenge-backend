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
        fields = ['id', 'num_notafiscal', 'dataehora', 'cliente', 'vendedor', 'produtos']