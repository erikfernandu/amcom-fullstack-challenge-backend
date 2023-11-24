# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from cadastro_pessoa.models import Cliente, Vendedor
from configuracao.models import ConfDiaSemana
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
    dataehora = models.DateTimeField(verbose_name='Data e hora')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, verbose_name='Produtos', through='ItemVenda')
    update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.num_notafiscal}'
    
    def save(self, *args, **kwargs):
        for item_venda in self.itemvenda_set.all():
            item_venda.save()
        super().save(*args, **kwargs)

class ItemVenda(models.Model):

    class Meta:
        verbose_name = 'Item da venda'
        verbose_name_plural = 'Itens da Venda'

    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1, blank=False, null=False)
    comissao = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, null=True)

    def save(self, *args, **kwargs):
        conf_dia_semana = ConfDiaSemana.objects.get(dia_da_semana=self.venda.dataehora.weekday()+1)
        percentual_minimo = conf_dia_semana.valor_minimo
        percentual_maximo = conf_dia_semana.valor_maximo
        if self.produto.comissao < percentual_minimo:
            self.comissao = percentual_minimo
        elif self.produto.comissao > percentual_maximo:
            self.comissao = percentual_maximo
        else:
            self.comissao = self.produto.comissao
        super().save(*args, **kwargs)