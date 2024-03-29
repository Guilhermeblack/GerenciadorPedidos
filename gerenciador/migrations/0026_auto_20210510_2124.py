# Generated by Django 3.0.8 on 2021-05-11 00:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gerenciador', '0025_auto_20210509_1634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gerente',
            name='loja',
        ),
        migrations.RemoveField(
            model_name='newcli',
            name='Email',
        ),
        migrations.RemoveField(
            model_name='newcli',
            name='Nome',
        ),
        migrations.RemoveField(
            model_name='newcli',
            name='Senha',
        ),
        migrations.RemoveField(
            model_name='newcli',
            name='Sobrenome',
        ),
        migrations.AddField(
            model_name='newcli',
            name='loja',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='new_loja', to='gerenciador.Loja'),
        ),
        migrations.AddField(
            model_name='newcli',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='newcli',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
