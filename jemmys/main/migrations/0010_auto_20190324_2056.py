# Generated by Django 2.1.7 on 2019-03-24 17:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_userissue_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
