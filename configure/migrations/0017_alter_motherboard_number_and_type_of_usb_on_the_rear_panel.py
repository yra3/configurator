# Generated by Django 3.2 on 2021-05-02 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configure', '0016_auto_20210502_0607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motherboard',
            name='number_and_type_of_usb_on_the_rear_panel',
            field=models.CharField(max_length=200, null=True),
        ),
    ]