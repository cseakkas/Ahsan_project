# Generated by Django 2.2.2 on 2022-10-01 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publisher_app', '0003_auto_20221001_2148'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productlist',
            old_name='perchase_discount',
            new_name='purchase_discount',
        ),
    ]
