# Generated by Django 4.0.4 on 2022-05-20 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0007_bale_verifiedvalue'),
    ]

    operations = [
        migrations.AddField(
            model_name='bale',
            name='shipmentvalue',
            field=models.FloatField(null=True, verbose_name='shipmentvalue  Value, mzigo unatoka, transport weight mara grade price'),
        ),
    ]
