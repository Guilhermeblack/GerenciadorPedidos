# Generated by Django 3.0.6 on 2020-05-27 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador', '0004_auto_20200527_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comanda',
            name='n_mesa',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]