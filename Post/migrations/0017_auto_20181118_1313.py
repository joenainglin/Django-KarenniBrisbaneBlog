# Generated by Django 2.1.1 on 2018-11-18 03:13

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0016_auto_20181108_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=tinymce.models.HTMLField(verbose_name='Content'),
        ),
    ]
