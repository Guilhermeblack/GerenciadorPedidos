# Generated by Django 3.0.6 on 2020-05-27 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador', '0002_auto_20200527_1717'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caixa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(default='cheff', max_length=50)),
                ('senha', models.CharField(max_length=50)),
                ('senha_rep', models.CharField(max_length=50)),
            ],
            options={
                'permissions': [('fechar_comanda', 'fechar a comanda'), ('ver_feed', 'visualizar o feed')],
            },
        ),
    ]