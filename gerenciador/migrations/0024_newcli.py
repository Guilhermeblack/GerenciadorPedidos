# Generated by Django 3.0.8 on 2021-05-09 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador', '0023_auto_20210509_1254'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newcli',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=40)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=30)),
            ],
        ),
    ]
