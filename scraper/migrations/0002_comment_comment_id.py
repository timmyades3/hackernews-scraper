# Generated by Django 5.1.5 on 2025-01-29 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
