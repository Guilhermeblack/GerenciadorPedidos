# Generated by Django 3.0.8 on 2021-05-13 22:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador', '0028_auto_20210512_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='comanda',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gerenciador.Newcli'),
        ),
        migrations.AlterField(
            model_name='newcli',
            name='loja',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gerenciador.Loja'),
        ),
    ]
