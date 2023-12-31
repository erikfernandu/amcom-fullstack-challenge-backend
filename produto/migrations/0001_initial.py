# Generated by Django 4.2.7 on 2023-11-30 13:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cadastro_pessoa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemVenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(default=1)),
                ('comissao', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
            ],
            options={
                'verbose_name': 'Item da venda',
                'verbose_name_plural': 'Itens da Venda',
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('codigo', models.CharField(max_length=10, verbose_name='Código do produto')),
                ('descricao', models.CharField(blank=True, max_length=80, null=True, verbose_name='Descrição do produto')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor unitário')),
                ('comissao', models.PositiveIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='Percentual de comissão')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'ordering': ['codigo'],
            },
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('num_notafiscal', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Nota fiscal')),
                ('dataehora', models.DateTimeField(verbose_name='Data e hora')),
                ('update', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastro_pessoa.cliente')),
                ('produtos', models.ManyToManyField(through='produto.ItemVenda', to='produto.produto', verbose_name='Produtos')),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastro_pessoa.vendedor')),
            ],
            options={
                'verbose_name': 'Venda',
                'verbose_name_plural': 'Vendas',
                'ordering': ['num_notafiscal'],
            },
        ),
        migrations.AddField(
            model_name='itemvenda',
            name='produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produto.produto'),
        ),
        migrations.AddField(
            model_name='itemvenda',
            name='venda',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produto.venda'),
        ),
    ]
