# Generated by Django 4.0.4 on 2022-06-25 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0008_bale_shipmentvalue'),
    ]

    operations = [
        migrations.AddField(
            model_name='bale',
            name='is_mannual',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
