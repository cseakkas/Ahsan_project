# Generated by Django 2.2.2 on 2022-10-01 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publisher_app', '0002_auto_20220924_1607'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productlist',
            old_name='discount',
            new_name='perchase_discount',
        ),
        migrations.RemoveField(
            model_name='publisherprofile',
            name='refund_policy',
        ),
        migrations.AddField(
            model_name='productlist',
            name='sale_discount',
            field=models.FloatField(default=0),
        ),
    ]