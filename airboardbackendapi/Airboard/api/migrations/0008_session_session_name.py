# Generated by Django 4.0.3 on 2022-04-05 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_session_end_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='session_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
