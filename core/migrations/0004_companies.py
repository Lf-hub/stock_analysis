# Generated by Django 4.2.6 on 2024-01-19 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_assets_asset_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('slug', models.CharField(max_length=10, verbose_name='Ticker')),
                ('is_active', models.BooleanField(default=True, verbose_name='Está Ativo?')),
            ],
            options={
                'verbose_name': 'Empresa',
            },
        ),
    ]
