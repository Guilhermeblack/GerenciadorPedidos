# Generated by Django 3.0.8 on 2021-02-24 22:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador', '0014_auto_20210124_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagamentos',
            name='formapg',
            field=models.CharField(choices=[('C', 'Cartão'), ('P', 'Pix'), ('D', 'Dinheiro')], default='D', max_length=1),
        ),
        migrations.AddField(
            model_name='produtocad',
            name='Insumos',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gerenciador.Produtocad'),
        ),
    ]
