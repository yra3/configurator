# Generated by Django 3.2 on 2021-04-27 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configure', '0010_auto_20210428_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ssd',
            name='drive_volume',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
