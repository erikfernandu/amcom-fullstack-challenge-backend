# -*- coding: utf-8 -*-
from django.test import TestCase
from .models import Vendedor, Cliente

# Create your tests here.
class VendedorModelTest(TestCase):
    def teste_vendedor_criar(self):
        vendedor = Vendedor.objects.create(
            nome="João",
            email="joao@example.com",
            telefone="123456789"
        )
        self.assertEqual(vendedor.nome, "João")
        self.assertEqual(vendedor.email, "joao@example.com")
        self.assertEqual(vendedor.telefone, "123456789")

    def teste_vendedor_atualizacao_timestamp(self):
        vendedor = Vendedor.objects.create(
            nome="Maria",
            telefone="987654321"
        )
        timestamp_antes = vendedor.timestamp
        vendedor.nome = "Maria Silva"
        vendedor.save()
        self.assertNotEqual(timestamp_antes, vendedor.timestamp)

    def teste_vendedor_str_representation(self):
        vendedor = Vendedor.objects.create(
            nome="José",
            telefone="555-1234"
        )
        self.assertEqual(str(vendedor), "José")
    
    def test_vendedor_criar_sem_email(self):
        vendedor = Vendedor.objects.create(
            nome="Ana",
            telefone="987654321"
        )
        self.assertIsNone(vendedor.email)

    def test_vendedor_telefone_max_length(self):
        with self.assertRaises(Exception) as context:
            Vendedor.objects.create(
                nome="Carlos",
                telefone="1234567890123456"
            )
        self.assertTrue("value too long" in str(context.exception))

    def test_vendedor_nome_nao_pode_ser_vazio(self):
        with self.assertRaises(Exception) as context:
            Vendedor.objects.create(
                nome="",
                telefone="987654321"
            )
        self.assertTrue("nome" in str(context.exception))

    def test_vendedor_email_deve_ser_valido(self):
        with self.assertRaises(Exception) as context:
            Vendedor.objects.create(
                nome="Laura",
                email="email_invalido",
                telefone="987654321"
            )
        self.assertTrue("Enter a valid email address" in str(context.exception))
    
class ClienteModelTest(TestCase):
    def test_cliente_criar(self):
        cliente = Cliente.objects.create(
            nome="Maria",
            email="maria@example.com",
            telefone="123456789"
        )
        self.assertEqual(cliente.nome, "Maria")
        self.assertEqual(cliente.email, "maria@example.com")
        self.assertEqual(cliente.telefone, "123456789")

    def test_cliente_atualizacao_timestamp(self):
        cliente = Cliente.objects.create(nome="João", telefone="987654321")
        timestamp_antes = cliente.timestamp
        cliente.nome = "João Silva"
        cliente.save()
        self.assertNotEqual(timestamp_antes, cliente.timestamp)

    def test_clientet_str_representation(self):
        cliente = Cliente.objects.create(nome="Ana", telefone="555-1234")
        self.assertEqual(str(cliente), "Ana")

    def test_cliente_criar_sem_email(self):
        cliente = Cliente.objects.create(
            nome="Carlos",
            telefone="987654321"
        )
        self.assertIsNone(cliente.email)

    def test_cliente_telefone_max_length(self):
        with self.assertRaises(Exception) as context:
            Cliente.objects.create(
                nome="Lucas",
                telefone="1234567890123456"
            )
        self.assertTrue("value too long" in str(context.exception))

    def test_cliente_nome_nao_pode_ser_vazio(self):
        with self.assertRaises(Exception) as context:
            Cliente.objects.create(
                nome="",
                telefone="987654321"
            )
        self.assertTrue("nome" in str(context.exception))

    def test_cliente_email_deve_ser_valido(self):
        with self.assertRaises(Exception) as context:
            Cliente.objects.create(
                nome="Laura",
                email="email_invalido",
                telefone="987654321"
            )
        self.assertTrue("Enter a valid email address" in str(context.exception))