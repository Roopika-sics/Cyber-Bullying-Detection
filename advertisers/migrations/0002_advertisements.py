# Generated by Django 5.1.1 on 2025-03-21 15:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('link', models.URLField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='advertisements/')),
                ('advertisement_type', models.CharField(choices=[('lifestyle', 'Life Style'), ('food_cooking', 'Food and Cooking'), ('electronics_appliances', 'Electronics and Home Appliances')], default='lifestyle', max_length=30)),
                ('advertiser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisers.advertiser')),
            ],
        ),
    ]
