# Generated by Django 4.0.4 on 2022-06-25 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0009_bale_is_mannual'),
    ]

    operations = [
        migrations.AddField(
            model_name='bale',
            name='mn_market',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='bale',
            name='mn_society',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
