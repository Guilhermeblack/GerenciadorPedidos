# Generated by Django 3.0.8 on 2020-10-12 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador', '0004_auto_20201012_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='produtosPed',
            field=models.ManyToManyField(blank=True, related_name='produto', to='gerenciador.Produtocad'),
        ),
    ]
