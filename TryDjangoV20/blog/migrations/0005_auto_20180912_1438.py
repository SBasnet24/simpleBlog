# Generated by Django 2.0.7 on 2018-09-12 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20180903_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='userblog',
            name='height_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userblog',
            name='image',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to='', width_field='width_field'),
        ),
        migrations.AddField(
            model_name='userblog',
            name='width_field',
            field=models.IntegerField(default=0),
        ),
    ]