# Generated by Django 3.0 on 2019-12-18 02:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anno', '0004_video_step_ids'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='step_ids',
            new_name='action_ids',
        ),
    ]
