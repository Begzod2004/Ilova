# Generated by Django 4.1.3 on 2022-12-07 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0007_alter_communication_lat_cord_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communication',
            name='status',
            field=models.CharField(choices=[('prosess', 'prosess'), ('cancelled', 'cancelled'), ('finished', 'finished')], default='prosess', max_length=20),
        ),
    ]