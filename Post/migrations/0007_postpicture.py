# Generated by Django 2.1.1 on 2018-10-29 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0006_post_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, upload_to='blog/post_pics')),
                ('postid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Post.Post')),
            ],
        ),
    ]
