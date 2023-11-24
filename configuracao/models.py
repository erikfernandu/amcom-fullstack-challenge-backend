# -*- coding: utf-8 -*-
from django.db import models
import uuid

# Create your models here.
class ConfDiaSemana(models.Model):

    class Meta:
        verbose_name = 'Configuração'
        verbose_name_plural = 'Configurações'
        ordering = ['dia_da_semana']

    DIAS_DA_SEMANA = [('1', 'Segunda-feira'),('2', 'Terça-feira'),('3', 'Quarta-feira'),('4', 'Quinta-feira'),('5', 'Sexta-feira'),('6', 'Sábado'),('7', 'Domingo')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dia_da_semana = models.CharField(unique=True, max_length=1, choices=DIAS_DA_SEMANA, blank=False, null=False, verbose_name='Dia da semana')
    valor_minimo = models.PositiveIntegerField(blank=True, null=True, verbose_name='Percentual de comissão mínimo')
    valor_maximo = models.PositiveIntegerField(blank=True, null=True, verbose_name='Percentual de comissão máximo')
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dia_da_semana