# -*- coding: utf-8 -*-
from django.db.models import Prefetch
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view
from .models import Produto, Venda, ItemVenda
from .serializers import ProdutoSerializer, VendaSerializer, VendasSerializer, ComissoesSerializer

# Create your views here.
class ProdutoAPI(APIView):
    def get(self, request, pk, format=None):
        produto = self.get_object(pk)
        serializer = ProdutoSerializer(produto)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProdutoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, format=None):
        produto = self.get_object(pk)
        serializer = ProdutoSerializer(produto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        produto = self.get_object(pk)
        serializer = ProdutoSerializer(produto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        produto = self.get_object(pk)
        produto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Produto.objects.get(pk=pk)
        except Produto.DoesNotExist:
            raise NotFound("Produto não encontrado")

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
class VendaAPI(APIView):
    def get(self, request, pk, format=None):
        venda = self.get_object(pk)
        serializer = VendaSerializer(venda)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        venda = self.get_object(pk)
        serializer = VendaSerializer(venda, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        venda = self.get_object(pk)
        serializer = VendaSerializer(venda, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        venda = self.get_object(pk)
        venda.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Venda.objects.get(pk=pk)
        except Venda.DoesNotExist:
            raise NotFound("Venda não encontrado")

class VendasAPI(APIView):
    def get(self, request, format=None):
        venda = Venda.objects.all()
        serializer = VendasSerializer(venda, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = VendasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComissoesAPI(APIView):
    def get(self, request, format=None):
        comissao = Venda.objects.values('vendedor_id', 'vendedor__nome').annotate(valor_total=Sum('valor_total'))
        print(comissao)
        serializer = ComissoesSerializer(comissao, many=True)
        return Response(serializer.data)