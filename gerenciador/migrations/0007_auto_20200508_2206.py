# Generated by Django 3.0.5 on 2020-05-09 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador', '0006_auto_20200508_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comanda',
            name='nome',
            field=models.TextField(max_length=50),
        ),
        migrations.AlterField(
            model_name='comanda',
            name='pedidos',
            field=models.TextField(max_length=255),
        ),
        migrations.AlterField(
            model_name='comanda',
            name='total',
            field=models.FloatField(max_length=6),
        ),
    ]
