# Generated by Django 4.1.3 on 2022-12-07 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='communication',
            name='title',
        ),
        migrations.AlterField(
            model_name='communication',
            name='description',
            field=models.TextField(verbose_name='comment'),
        ),
    ]
