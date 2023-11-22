# -*- coding: utf-8 -*-
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Venda, Produto
from produto.models import Vendedor
from .serializers import VendaSerializer, ProdutoSerializer, NovaVendaSerializer
from produto.serializers import ComissoesSerializer
from datetime import datetime

# Create your views here.
class VendaAPI(APIView):
    def get(self, request, pk):
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
    
    def delete(self, request, pk):
        try:
            venda = Venda.objects.get(id=pk)
            venda.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(f'Erro ao excluir venda: {str(e)}')

class VendasAPI(APIView):
    def get(self, request):
        venda = Venda.objects.all()
        serializer = VendaSerializer(venda, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            serializer = NovaVendaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Venda finalizada com sucesso!'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}) #, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProdutosAPI(APIView):
    def get(self, request, *args, **kwargs):
        search = request.query_params.get('search', None)
        if search:
            produto = Produto.objects.filter(descricao__icontains=search)
        else:
            produto = Produto.objects.all()
        serializer = ProdutoSerializer(produto, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ComissoesAPI(APIView):
    def get(self, request, *args, **kwargs):
        comissao = Vendedor.objects.all().order_by('codigo')
        serializer = ComissoesSerializer(comissao, many=True, context={'start_date': self.request.GET.get('start_date'), 'end_date': self.request.GET.get('end_date')})
        return Response(serializer.data)