# Generated by Django 3.2.8 on 2021-10-13 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0004_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='status',
            field=models.CharField(choices=[('Enabled', 'Enabled'), ('Disabled', 'Disabled')], default='Disabled', max_length=8),
        ),
    ]