# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Produto, Venda, ItemVenda, Cliente, Vendedor

# Create your tests here.
class ProdutoModelTest(TestCase):

    def test_criar_produto(self):
        produto = Produto.objects.create(
            codigo="ABC123",
            descricao="Produto ABC",
            valor=25.50,
            comissao=5
        )
        self.assertEqual(produto.codigo, "ABC123")
        self.assertEqual(produto.descricao, "Produto ABC")
        self.assertEqual(produto.valor, 25.50)
        self.assertEqual(produto.comissao, 5)

    def test_valor_comissao_max(self):
        produto = Produto.objects.create(
            codigo="XYZ789",
            descricao="Produto XYZ",
            valor=15.75,
            comissao=10
        )
        self.assertEqual(produto.comissao, 10)

    def test_valor_comissao_fora_do_intervalo(self):
        with self.assertRaises(ValidationError):
            Produto.objects.create(
                codigo="123XYZ",
                descricao="Produto 123",
                valor=30.00,
                comissao=15
            )

    def test_criar_produto_sem_descricao(self):
        produto = Produto.objects.create(
            codigo="DEF456",
            valor=19.99
        )
        self.assertIsNone(produto.descricao)

class VendaModelTest(TestCase):

    def setUp(self):
        self.cliente = Cliente.objects.create(nome="Cliente Teste", telefone="123456789")
        self.vendedor = Vendedor.objects.create(nome="Vendedor Teste", telefone="987654321")

    def test_criar_venda(self):
        venda = Venda.objects.create(
            num_notafiscal=123,
            cliente=self.cliente,
            vendedor=self.vendedor
        )
        self.assertEqual(venda.num_notafiscal, 123)
        self.assertEqual(venda.cliente, self.cliente)
        self.assertEqual(venda.vendedor, self.vendedor)

    def test_criar_venda_sem_cliente(self):
        with self.assertRaises(ValueError):
            Venda.objects.create(
                num_notafiscal=456,
                vendedor=self.vendedor
            )

    def test_criar_venda_sem_vendedor(self):
        with self.assertRaises(ValueError):
            Venda.objects.create(
                num_notafiscal=789,
                cliente=self.cliente
            )

class ItemVendaModelTest(TestCase):
    
    def setUp(self):
        self.produto = Produto.objects.create(
            codigo="ABC123",
            descricao="Produto ABC",
            valor=25.50,
            comissao=5
        )
        self.cliente = Cliente.objects.create(nome="Cliente Teste", telefone="123456789")
        self.vendedor = Vendedor.objects.create(nome="Vendedor Teste", telefone="987654321")
        self.venda = Venda.objects.create(
            num_notafiscal=123,
            cliente=self.cliente,
            vendedor=self.vendedor
        )

    def test_criar_item_venda(self):
        item_venda = ItemVenda.objects.create(
            venda=self.venda,
            produto=self.produto,
            quantidade=2
        )
        self.assertEqual(item_venda.venda, self.venda)
        self.assertEqual(item_venda.produto, self.produto)
        self.assertEqual(item_venda.quantidade, 2)

    def test_criar_item_venda_sem_quantidade(self):
        with self.assertRaises(ValueError):
            ItemVenda.objects.create(
                venda=self.venda,
                produto=self.produto
            )