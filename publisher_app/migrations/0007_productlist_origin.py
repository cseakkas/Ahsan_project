# Generated by Django 2.2.2 on 2022-10-01 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publisher_app', '0006_productlist_product_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='productlist',
            name='origin',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
