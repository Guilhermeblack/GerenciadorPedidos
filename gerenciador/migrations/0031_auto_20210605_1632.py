# Generated by Django 3.0.8 on 2021-06-05 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador', '0030_auto_20210515_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produtocad',
            name='quantidade',
            field=models.FloatField(blank=True, default=1, null=True),
        ),
    ]