# -*- coding: utf-8 -*-
from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view
from .models import Venda, Produto
from .serializers import VendaSerializer, ProdutoSerializer

# Create your views here.
class VendaAPI(APIView):
    def get(self, request, pk, format=None):
        venda = Venda.objects.get(id=pk)
        serializer = VendaSerializer(venda, many=False)
        return Response(serializer.data)
    
    # def put(self, request, pk, format=None):
    #     venda = self.get_object(pk)
    #     serializer = VendaSerializer(venda, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def patch(self, request, pk, format=None):
    #     venda = self.get_object(pk)
    #     serializer = VendaSerializer(venda, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        venda = self.get_object(pk)
        venda.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VendasAPI(APIView):
    def get(self, request, format=None):
        venda = Venda.objects.all()
        serializer = VendaSerializer(venda, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = VendaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProdutosAPI(APIView):
    def get(self, request, format=None, *args, **kwargs):
        search = request.query_params.get('search', None)
        if search:
            produto = Produto.objects.filter(descricao__icontains=search)
        else:
            produto = Produto.objects.all()
        serializer = ProdutoSerializer(produto, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)