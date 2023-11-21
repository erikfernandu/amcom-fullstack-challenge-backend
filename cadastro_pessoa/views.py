# -*- coding: utf-8 -*-
from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import VendedoresSerializer, ClientesSerializer #, ComissoesSerializer
from .models import Vendedor, Cliente

# Create your views here.
class VendedoresAPI(APIView):
    def get(self, request, format=None):
        vendedor = Vendedor.objects.all()
        serializer = VendedoresSerializer(vendedor, many=True)
        return Response(serializer.data)

class ClientesAPI(APIView):
    def get(self, request, format=None):
        clientes = Cliente.objects.all()
        serializer = ClientesSerializer(clientes, many=True)
        return Response(serializer.data)

# class ComissoesAPI(APIView):
#     def get(self, request, format=None):
#         comissao = Vendedor.objects.annotate(soma=Coalesce(Sum('venda__produtos__itemvenda__quantidade'), 0))
#         serializer = ComissoesSerializer(comissao, many=True)
#         return Response(serializer.data)
