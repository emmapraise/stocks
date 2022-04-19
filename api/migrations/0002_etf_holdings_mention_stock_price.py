# Generated by Django 3.2.12 on 2022-04-02 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Etf_holdings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etf_id', models.IntegerField()),
                ('holding_id', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('shares', models.IntegerField()),
                ('weight', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Stock_price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('open', models.DecimalField(decimal_places=2, max_digits=10)),
                ('high', models.DecimalField(decimal_places=2, max_digits=10)),
                ('low', models.DecimalField(decimal_places=2, max_digits=10)),
                ('close', models.DecimalField(decimal_places=2, max_digits=10)),
                ('volume', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.stock')),
            ],
        ),
        migrations.CreateModel(
            name='Mention',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField()),
                ('source', models.CharField(max_length=200)),
                ('url', models.URLField()),
                ('stock_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.stock')),
            ],
        ),
    ]
