# -*- coding: utf-8 -*-
from django.db import models
import uuid

# Create your models here.
class Vendedor(models.Model):

    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'
        ordering = ['nome']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=60, blank=False, null=False, verbose_name='Nome do vendedor')
    email = models.EmailField(blank=True, null=True, verbose_name='Endereço de E-mail')
    telefone = models.TextField(max_length=14, verbose_name='Telefone')
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class Cliente(models.Model):

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=60, blank=False, null=False, verbose_name='Nome do cliente')
    email = models.EmailField(blank=True, null=True, verbose_name='Endereço de E-mail')
    telefone = models.TextField(max_length=14, verbose_name='Telefone')
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.nome