# Generated by Django 3.2 on 2021-05-02 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configure', '0022_alter_motherboard_features_optional'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpu',
            name='features_optional',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
