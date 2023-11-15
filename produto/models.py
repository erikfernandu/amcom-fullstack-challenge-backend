# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from cadastro_pessoa.models import Cliente, Vendedor
import uuid

# Create your models here.
class Produto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=10, blank=False, null=False, verbose_name='Código do produto')
    descricao = models.CharField(max_length=80, blank=True, null=True, verbose_name='Descrição do produto')
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, verbose_name='Valor unitário')
    comissao = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, null=True, verbose_name='Percentual de comissão')
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.descricao

class Venda(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    num_notafiscal = models.IntegerField(validators=[MinValueValidator(0)], blank=False, null=False)
    dataehora = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, verbose_name='Produtos', through='ItemVenda')
    update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return '%d' %(self.num_notafiscal)

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1, blank=False, null=False)