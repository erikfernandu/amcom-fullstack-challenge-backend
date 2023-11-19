# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Vendedor, Cliente

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = ['id', 'nome', 'email', 'telefone', 'total_comissao']
    total_comissao = serializers.DecimalField(max_digits=10, decimal_places=2)

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'email', 'telefone']