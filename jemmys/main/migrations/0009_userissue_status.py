# Generated by Django 2.1.5 on 2019-03-11 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20190203_0852'),
    ]

    operations = [
        migrations.AddField(
            model_name='userissue',
            name='status',
            field=models.CharField(choices=[('FR', 'For Review'), ('UR', 'Under Review'), ('R', 'Resolved')], default='FR', max_length=3),
        ),
    ]
