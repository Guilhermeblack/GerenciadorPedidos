# Generated by Django 3.2.12 on 2022-04-05 23:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador', '0034_alter_comanda_n_mesa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gerente',
            name='loja',
        ),
    ]
