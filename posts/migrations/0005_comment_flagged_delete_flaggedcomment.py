# Generated by Django 5.1.6 on 2025-03-02 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_flaggedcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='flagged',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='FlaggedComment',
        ),
    ]
