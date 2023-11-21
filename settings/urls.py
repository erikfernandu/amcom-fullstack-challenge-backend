"""
URL configuration for settings project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from produto.views import VendaAPI, VendasAPI, ProdutosAPI
from cadastro_pessoa.views import VendedoresAPI, ClientesAPI #, ComissoesAPI
from produto.views import ComissoesAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/vendedor/<uuid:pk>/', VendedorAPI.as_view(), name='vendedor'),
    path('api/vendedores/', VendedoresAPI.as_view(), name='vendedores'),
    # path('api/cliente/<uuid:pk>/', ClienteAPI.as_view(), name='cliente'),
    path('api/clientes/', ClientesAPI.as_view(), name='clientes'),

    path('api/produtos/', ProdutosAPI.as_view(), name='produtos'),
    path('api/venda/<uuid:pk>/', VendaAPI.as_view(), name='venda'),
    path('api/vendas/', VendasAPI.as_view(), name='vendas'),
    path('api/comissoes/', ComissoesAPI.as_view(), name='comissoes'),

]
