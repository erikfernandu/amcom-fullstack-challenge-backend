# -*- coding: utf-8 -*-
from django.db import models
import uuid

# Create your models here.

class ConfDiaSemana(models.Model):

    class Meta:
        verbose_name = 'Configuração'
        verbose_name_plural = 'Configurações'
        ordering = ['dia_da_semana']

    DIAS_DA_SEMANA = [('1', 'Domingo'),('2', 'Segunda-feira'),('3', 'Terça-feira'),('4', 'Quarta-feira'),('5', 'Quinta-feira'),('6', 'Sexta-feira'),('7', 'Sábado')]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dia_da_semana = models.CharField(unique=True, max_length=1, choices=DIAS_DA_SEMANA, blank=False, null=False, verbose_name='Dia da semana')
    valor_minimo = models.PositiveIntegerField(blank=True, null=True, verbose_name='Percentual de comissão mínimo')
    valor_maximo = models.PositiveIntegerField(blank=True, null=True, verbose_name='Percentual de comissão máximo')
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)