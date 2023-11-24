# -*- coding: utf-8 -*-
from django.db.models import Sum, Q
from rest_framework import serializers
from .models import Produto, Venda, ItemVenda, Vendedor
from decimal import Decimal

# Create your serializers here.
class BaseProdutoSerializer(serializers.ModelSerializer):

    class Meta:
        abstract = True
        model = Produto
        fields = ['id', 'codigo', 'descricao', 'valor']

class BaseItemVendaSerializer(serializers.ModelSerializer):

    class Meta:
        abstract = True
        model = ItemVenda
        fields = ['produto', 'quantidade', 'comissao']

class DetalheItemVendaSerializer(BaseItemVendaSerializer):
    produto = BaseProdutoSerializer()

class BaseVendaSerializer(serializers.ModelSerializer):
    
    class Meta:
        abstract = True
        model = Venda
        fields = ['id', 'num_notafiscal', 'dataehora', 'cliente', 'vendedor', 'itemvenda_set']

    def get_valor_total(self, venda):
        produtos_vendidos = ItemVenda.objects.filter(venda=venda)
        valor_total = sum(item.produto.valor * item.quantidade for item in produtos_vendidos if item.produto.valor is not None)
        return valor_total

class ListaVendaSerializer(BaseVendaSerializer):
    cliente = serializers.CharField(source='cliente.nome')
    vendedor = serializers.CharField(source='vendedor.nome')
    itemvenda_set = DetalheItemVendaSerializer(many=True)
    total_itens = serializers.SerializerMethodField()
    valor_total = serializers.SerializerMethodField()
    valor_total_comissoes = serializers.SerializerMethodField()

    class Meta:
        model = Venda
        fields = ['id', 'num_notafiscal', 'dataehora', 'cliente', 'vendedor', 'itemvenda_set', 'valor_total', 'total_itens', 'valor_total_comissoes']

    def get_total_itens(self, obj):
        total_itens = Venda.objects.filter(id=obj.id).annotate(total_itens=Sum('itemvenda__quantidade')).values('total_itens')[0]['total_itens']
        return total_itens
    
    def get_valor_total_comissoes(self, venda):
        produtos_vendidos = ItemVenda.objects.filter(venda=venda)
        total_comissoes = sum((item.quantidade * item.produto.valor * item.comissao) / 100 for item in produtos_vendidos if item.produto.valor is not None)
        return total_comissoes

class EnvioDetalheSerializer(BaseVendaSerializer):
    dataehora = serializers.DateTimeField(format='%Y-%m-%dT%H:%M')
    itemvenda_set = DetalheItemVendaSerializer(many=True)
    valor_total = serializers.SerializerMethodField()

    class Meta:
        model = Venda
        fields = ['id', 'num_notafiscal', 'dataehora', 'cliente', 'vendedor', 'itemvenda_set', 'valor_total']

class RetornoDetalheVendaSerializer(BaseVendaSerializer):
    itemvenda_set = BaseItemVendaSerializer(many=True)

    def update(self, instance, validated_data):
        itens_venda_data = validated_data.pop('itemvenda_set', None)
        instance.num_notafiscal = validated_data.get('num_notafiscal', instance.num_notafiscal)
        instance.dataehora = validated_data.get('datatehora', instance.dataehora)
        instance.cliente = validated_data.get('cliente', instance.cliente)
        instance.vendedor = validated_data.get('vendedor', instance.vendedor)
        instance.save()
        print('SERIALIZER', itens_venda_data)
        if itens_venda_data is not None:
            instance.itemvenda_set.all().delete()
            for item_data in itens_venda_data:
                produto = item_data['produto']
                quantidade = item_data['quantidade']
                ItemVenda.objects.update_or_create(venda=instance, produto=produto, quantidade=quantidade)
        return instance

class CriarItemVendaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemVenda
        fields = ['produto', 'quantidade']

class CriarVendaSerializer(serializers.ModelSerializer):
    itemvenda_set = CriarItemVendaSerializer(many=True)

    class Meta:
        model = Venda
        fields = ['id', 'num_notafiscal', 'dataehora', 'cliente', 'vendedor', 'itemvenda_set']
    
    def create(self, validated_data):
        itens_venda_data = validated_data.pop('itemvenda_set')
        venda = Venda.objects.create(**validated_data)
        for item_data in itens_venda_data:
            produto_id = item_data.pop('produto')
            ItemVenda.objects.create(venda=venda, produto=produto_id, **item_data)
        return venda

class ComissoesSerializer(serializers.ModelSerializer):
    vendas = ListaVendaSerializer(many=True, read_only=True)
    total_vendas = serializers.SerializerMethodField()
    total_comissoes = serializers.SerializerMethodField()

    class Meta:
        model = Vendedor
        fields = ['id', 'codigo', 'nome', 'vendas', 'total_vendas', 'total_comissoes']

    def get_total_vendas(self, vendedor):
        query = Q()
        if self.context.get('start_date'):
            query &= Q(dataehora__gte=self.context.get('start_date'))
        if self.context.get('end_date'):
            query &= Q(dataehora__lte=self.context.get('end_date'))
        vendas = Venda.objects.filter(vendedor=vendedor).filter(query)
        total_vendas = sum(Decimal(item.produto.valor) * item.quantidade for venda in vendas for item in ItemVenda.objects.filter(venda=venda) if item.produto.valor is not None )
        return total_vendas

    def get_total_comissoes(self, vendedor):
        query = Q()
        if self.context.get('start_date') is not None:
            query &= Q(venda__dataehora__gte=self.context.get('start_date'))
        if self.context.get('end_date') is not None:
            query &= Q(venda__dataehora__lte=self.context.get('end_date'))
        produtos_vendidos = ItemVenda.objects.filter(venda__vendedor=vendedor).filter(query)
        total_comissoes = sum((item.produto.valor * item.comissao / 100) * item.quantidade for item in produtos_vendidos if item.produto.valor is not None and item.produto.comissao is not None)
        return total_comissoes
