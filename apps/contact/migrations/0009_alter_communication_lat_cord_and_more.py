# Generated by Django 4.1.3 on 2022-12-07 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0008_alter_communication_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communication',
            name='lat_cord',
            field=models.DecimalField(decimal_places=7, max_digits=10),
        ),
        migrations.AlterField(
            model_name='communication',
            name='long_cord',
            field=models.DecimalField(decimal_places=7, max_digits=10),
        ),
    ]