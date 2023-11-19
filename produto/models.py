# -*- coding: utf-8 -*-
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator, MaxValueValidator
from cadastro_pessoa.models import Cliente, Vendedor
import uuid

# Create your models here.
class Produto(models.Model):

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['codigo']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=10, blank=False, null=False, verbose_name='Código do produto')
    descricao = models.CharField(max_length=80, blank=True, null=True, verbose_name='Descrição do produto')
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, verbose_name='Valor unitário')
    comissao = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, null=True, verbose_name='Percentual de comissão')
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.descricao

class Venda(models.Model):

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['num_notafiscal']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    num_notafiscal = models.IntegerField(validators=[MinValueValidator(0)], blank=False, null=False, verbose_name='Nota fiscal')
    dataehora = models.DateTimeField(auto_now_add=True, verbose_name='Data e hora')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, verbose_name='Produtos', through='ItemVenda')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Valor Total')
    update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.num_notafiscal}'

class ItemVenda(models.Model):

    class Meta:
        verbose_name = 'Item da venda'
        verbose_name_plural = 'Itens da Venda'

    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1, blank=False, null=False)
    