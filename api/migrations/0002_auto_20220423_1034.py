# Generated by Django 3.2.12 on 2022-04-23 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mention',
            old_name='stock_id',
            new_name='stock',
        ),
        migrations.RenameField(
            model_name='stock_price',
            old_name='stock_id',
            new_name='stock',
        ),
    ]
