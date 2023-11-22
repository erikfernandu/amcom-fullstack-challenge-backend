# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import VendedoresSerializer, ClientesSerializer
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
