# Generated by Django 3.2 on 2021-04-27 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configure', '0012_alter_ssd_m2_drive_volume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='powersupply',
            name='link',
            field=models.URLField(null=True, unique=True),
        ),
    ]