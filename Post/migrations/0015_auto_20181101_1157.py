# Generated by Django 2.1.1 on 2018-11-01 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0014_auto_20181101_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.CharField(max_length=250, unique_for_date='publish'),
        ),
    ]
