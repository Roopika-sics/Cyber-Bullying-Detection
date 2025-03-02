# Generated by Django 5.1.6 on 2025-03-02 11:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_remove_post_likes_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlaggedComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flagged_by', models.CharField(max_length=100)),
                ('reviewed', models.BooleanField(default=False)),
                ('reviewed_at', models.DateTimeField(blank=True, null=True)),
                ('comment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='flagged', to='posts.comment')),
            ],
        ),
    ]
