# Generated by Django 2.2.2 on 2022-06-24 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publisher_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCategoryWiseBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('book_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='publisher_app.BookList')),
                ('subcategory_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='publisher_app.MastarSubCategory')),
            ],
            options={
                'verbose_name': 'Sub Category Wise Book',
                'verbose_name_plural': 'Sub Category Wise Books',
                'db_table': 'sub_category_wise_book',
            },
        ),
    ]
