# Generated by Django 3.0.5 on 2020-05-04 02:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comanda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pedidos', models.TextField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Cozinha',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('senha', models.CharField(max_length=255)),
                ('senha_rep', models.CharField(max_length=255)),
            ],
            options={
                'permissions': [('pedido_pronto', 'pedido pronto'), ('ver_feed', 'visualizar o feed')],
            },
        ),
        migrations.CreateModel(
            name='Garçom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('fazer_pedido', 'incluir pedido'), ('pedido_entregue', 'pedido foi entregue'), ('ver_feed', 'visualizar o feed'), ('abrir_comanda', 'abrir uma nova comanda')],
            },
        ),
        migrations.CreateModel(
            name='Gerente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('senha', models.CharField(max_length=255)),
                ('senha_rep', models.CharField(max_length=255)),
            ],
            options={
                'permissions': [('fazer_pedido', 'incluir pedido'), ('ver_feed', 'visualizar o feed'), ('iniciar_movimento', 'iniciar o movimento'), ('fechar_comanda', 'fechar a comanda'), ('abrir_comanda', 'abrir uma nova comanda')],
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco', models.FloatField()),
                ('comanda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gerenciador.Comanda')),
            ],
        ),
    ]
