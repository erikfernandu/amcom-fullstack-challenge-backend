# -*- coding: utf-8 -*-
from django.db.models import Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from .models import Vendedor, Cliente
from produto.models import Venda, ItemVenda
from .serializers import VendedorSerializer, ClienteSerializer

# Create your views here.
class VendedorAPI(APIView):
    def get(self, request, pk, format=None):
        vendedor = self.get_object(pk)
        serializer = VendedorSerializer(vendedor)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        vendedor = self.get_object(pk)
        serializer = VendedorSerializer(vendedor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        vendedor = self.get_object(pk)
        serializer = VendedorSerializer(vendedor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        vendedor = self.get_object(pk)
        vendedor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Vendedor.objects.get(pk=pk)
        except Vendedor.DoesNotExist:
            raise NotFound("Vendedor não encontrado")

class VendedoresAPI(APIView):
    def get(self, request, format=None):
        vendedores = Vendedor.objects.annotate(total_comissao=Count('venda__itemvenda__quantidade')).values('id', 'nome', 'email', 'telefone', 'total_comissao')
        print(vendedores)
        serializer = VendedorSerializer(vendedores, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = VendedorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClienteAPI(APIView):
    def get(self, request, pk, format=None):
        cliente = self.get_object(pk)
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        cliente = self.get_object(pk)
        serializer = ClienteSerializer(cliente, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        cliente = self.get_object(pk)
        serializer = ClienteSerializer(cliente, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        cliente = self.get_object(pk)
        cliente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Cliente.objects.get(pk=pk)
        except Cliente.DoesNotExist:
            raise NotFound("Cliente não encontrado")

class ClientesAPI(APIView):

    def post(self, request, format=None):
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)