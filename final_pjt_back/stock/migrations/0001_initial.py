# Generated by Django 4.2.8 on 2024-05-23 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockList',
            fields=[
                ('ticker', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('ticker_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('opening_price', models.IntegerField()),
                ('highest_price', models.IntegerField()),
                ('lowest_price', models.IntegerField()),
                ('closing_price', models.IntegerField()),
                ('volume', models.IntegerField()),
                ('fluctuation_rate', models.FloatField()),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock', to='stock.stocklist')),
            ],
        ),
    ]