# Generated by Django 4.0.3 on 2022-04-04 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_team_team_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='board',
            field=models.FileField(upload_to='images'),
        ),
    ]