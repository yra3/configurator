# Generated by Django 3.2 on 2021-05-02 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configure', '0014_auto_20210428_0248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cooler',
            name='power_dissipation',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='cpu',
            name='heat_dissipation_tdp',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='cpu',
            name='maximum_frequency_of_ram',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='cpu',
            name='minimum_frequency_of_ram',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='gpu',
            name='maximum_power_consumption',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='hard25',
            name='hdd_capacity',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='hard35',
            name='hdd_capacity',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='motherboard',
            name='maximum_memory',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='motherboard',
            name='maximum_memory_frequency',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='motherboard',
            name='minimum_memory_frequency',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='motherboard',
            name='number_of_memory_slots',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='powersupply',
            name='power_nominal',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ram',
            name='clock_frequency',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ram',
            name='number_of_modules_included',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ram',
            name='the_volume_of_one_memory_module',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ssd',
            name='drive_volume',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ssd_m2',
            name='drive_volume',
            field=models.IntegerField(null=True),
        ),
    ]
