# Generated by Django 4.1 on 2022-08-15 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0004_brand'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='category.brand'),
            preserve_default=False,
        ),
    ]