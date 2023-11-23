# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Vendedor, Cliente

# Create your serializers here.
class VendedoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = ['id', 'nome']

class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome']
