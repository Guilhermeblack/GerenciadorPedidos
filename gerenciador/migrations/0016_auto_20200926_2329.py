# Generated by Django 3.0.8 on 2020-09-27 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador', '0015_auto_20200924_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='produtosPed',
            field=models.ManyToManyField(related_name='produto', to='gerenciador.Produtocad'),
        ),
    ]