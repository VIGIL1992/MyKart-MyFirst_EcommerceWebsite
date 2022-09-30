# Generated by Django 4.1 on 2022-09-19 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='order_total',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Placed', 'Placed'), ('Shipped', 'Shipped'), ('Accepted', 'Accepted'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='New', max_length=50),
        ),
    ]