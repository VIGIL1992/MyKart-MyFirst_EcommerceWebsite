# Generated by Django 4.1 on 2022-09-13 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
