# Generated by Django 2.0.7 on 2018-08-31 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainlogin', '0002_auto_20180831_0608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customusermodel',
            name='user',
        ),
        migrations.DeleteModel(
            name='CustomUserModel',
        ),
    ]
