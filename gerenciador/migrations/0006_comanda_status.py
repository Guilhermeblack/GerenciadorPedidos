# Generated by Django 3.0.8 on 2020-10-17 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador', '0005_auto_20201012_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='comanda',
            name='status',
            field=models.CharField(choices=[('A', 'Aberto'), ('F', 'Fechado')], default='A', max_length=1),
        ),
    ]
