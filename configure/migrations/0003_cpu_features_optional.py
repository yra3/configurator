# Generated by Django 3.2 on 2021-04-27 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configure', '0002_auto_20210427_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpu',
            name='features_optional',
            field=models.CharField(max_length=100, null=True),
        ),
    ]