# Generated by Django 5.1.1 on 2025-03-22 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisers', '0003_maliciousclick'),
    ]

    operations = [
        migrations.RenameField(
            model_name='maliciousclick',
            old_name='timestamp',
            new_name='clicked_at',
        ),
        migrations.RemoveField(
            model_name='maliciousclick',
            name='result',
        ),
    ]
