# Generated by Django 2.2.2 on 2022-04-19 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publisher_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookwritter',
            name='is_editor',
            field=models.BooleanField(default=1),
        ),
        migrations.AddField(
            model_name='bookwritter',
            name='is_translator',
            field=models.BooleanField(default=1),
        ),
        migrations.AddField(
            model_name='bookwritter',
            name='is_wirter',
            field=models.BooleanField(default=1),
        ),
    ]