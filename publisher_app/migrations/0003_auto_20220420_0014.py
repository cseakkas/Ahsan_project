# Generated by Django 2.2.2 on 2022-04-19 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publisher_app', '0002_auto_20220420_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookwritter',
            name='is_editor',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='bookwritter',
            name='is_translator',
            field=models.BooleanField(default=0),
        ),
    ]