# Generated by Django 3.2 on 2021-04-21 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nlp_api', '0003_auto_20210422_0054'),
    ]

    operations = [
        migrations.AddField(
            model_name='qacahce',
            name='question',
            field=models.CharField(default='none', max_length=255),
        ),
        migrations.AlterField(
            model_name='qacahce',
            name='text_hash',
            field=models.CharField(default='none', max_length=12),
        ),
    ]
