from django.test import TestCase
from configuracao.models import ConfDiaSemana

# Create your tests here.
class ConfDiaSemanaModelTest(TestCase):
    def test_confdiasemana_criar(self):
        configuracao = ConfDiaSemana.objects.create(
            dia_da_semana='1',
            valor_minimo=5,
            valor_maximo=10
        )
        self.assertEqual(configuracao.dia_da_semana, '1')
        self.assertEqual(configuracao.valor_minimo, 5)
        self.assertEqual(configuracao.valor_maximo, 10)

    def test_confdiasemana_str_representation(self):
        configuracao = ConfDiaSemana.objects.create(
            dia_da_semana='2',
            valor_minimo=7,
            valor_maximo=15
        )
        self.assertEqual(str(configuracao), 'Terça-feira')

    def test_confdiasemana_criar_sem_valores_minimo_maximo(self):
        configuracao = ConfDiaSemana.objects.create(
            dia_da_semana='3'
        )
        self.assertIsNone(configuracao.valor_minimo)
        self.assertIsNone(configuracao.valor_maximo)

    def test_confdiasemana_criar_duplicata(self):
        ConfDiaSemana.objects.create(
            dia_da_semana='4',
            valor_minimo=3,
            valor_maximo=8
        )
        with self.assertRaises(Exception) as context:
            ConfDiaSemana.objects.create(
                dia_da_semana='4',
                valor_minimo=5,
                valor_maximo=10
            )
        self.assertTrue("unique constraint" in str(context.exception))

    def test_confdiasemana_valor_minimo_deve_ser_positivo(self):
        with self.assertRaises(Exception) as context:
            ConfDiaSemana.objects.create(
                dia_da_semana='5',
                valor_minimo=-5,
                valor_maximo=10
            )
        self.assertTrue("Ensure this value is greater than or equal to 0" in str(context.exception))
