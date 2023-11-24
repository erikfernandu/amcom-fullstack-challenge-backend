# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Venda, Produto
from produto.models import Vendedor
from .serializers import ListaVendaSerializer, BaseProdutoSerializer, EnvioDetalheSerializer, RetornoDetalheVendaSerializer, CriarVendaSerializer
from produto.serializers import ComissoesSerializer

# Create your views here.
class VendaAPI(APIView):

    def get(self, request, pk):
        venda = Venda.objects.get(id=pk)
        serializer = EnvioDetalheSerializer(venda, many=False)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            venda = Venda.objects.get(id=pk)
            serializer = RetornoDetalheVendaSerializer(venda, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'mensagem': 'VENDA ATUALIZADA COM SUCESSO!'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Venda.DoesNotExist:
            return Response({"mensagem": "VENDA NÃO ENCONTRADA"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"mensagem": f"ERRO INTERNO DO SERVIDOR: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def patch(self, request, pk, format=None):
    #     venda = self.get_object(pk)
    #     serializer = ListaVendaSerializer(venda, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            venda = Venda.objects.get(id=pk)
            venda.delete()
            return Response({'message': 'VENDA REMOVIDA COM SUCESSO!'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'ERRO DO SERVIDOR': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VendasAPI(APIView):

    def get(self, request):
        venda = Venda.objects.all()
        serializer = ListaVendaSerializer(venda, many=True, read_only=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            serializer = CriarVendaSerializer(data=request.data)
            print('VIEW', serializer)
            if serializer.is_valid():
                serializer.save()
                return Response({'mensagem': 'VENDA REALIZADA COM SUCESSO!'}, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response({"mensagem": serializer.errors}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'ERRO INTERNO DO SERVIDOR': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProdutosAPI(APIView):

    def get(self, request, *args, **kwargs):
        search = request.query_params.get('search', None)
        if search:
            produto = Produto.objects.filter(descricao__icontains=search)
        else:
            produto = Produto.objects.all()
        serializer = BaseProdutoSerializer(produto, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ComissoesAPI(APIView):

    def get(self, request, *args, **kwargs):
        comissao = Vendedor.objects.all().order_by('codigo')
        serializer = ComissoesSerializer(comissao, many=True, context={'start_date': self.request.GET.get('start_date'), 'end_date': self.request.GET.get('end_date')})
        return Response(serializer.data)