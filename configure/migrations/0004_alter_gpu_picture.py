# Generated by Django 3.2 on 2021-04-27 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configure', '0003_cpu_features_optional'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpu',
            name='picture',
            field=models.URLField(null=True),
        ),
    ]
