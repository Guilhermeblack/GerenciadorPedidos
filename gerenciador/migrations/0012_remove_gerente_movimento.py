# Generated by Django 3.0.8 on 2020-08-18 01:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador', '0011_auto_20200817_2218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gerente',
            name='movimento',
        ),
    ]
