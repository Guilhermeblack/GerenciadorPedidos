# Generated by Django 3.0.8 on 2021-03-07 22:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador', '0017_auto_20210307_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='produtocad',
            name='cardapio',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='produtocad',
            name='insumos',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gerenciador.Produtocad'),
        ),
        migrations.CreateModel(
            name='insumos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantidade_prod', models.FloatField(default=0.0)),
                ('insumo_prod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='insumo_prod', to='gerenciador.Produtocad')),
                ('produto_prod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='produto_prod', to='gerenciador.Produtocad')),
            ],
        ),
    ]