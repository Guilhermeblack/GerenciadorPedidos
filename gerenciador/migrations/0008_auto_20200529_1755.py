# Generated by Django 3.0.6 on 2020-05-29 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador', '0007_auto_20200529_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produtocad',
            name='tipo',
            field=models.CharField(choices=[('A', 'Alimento'), ('B', 'Bebida')], max_length=1),
        ),
    ]
