# Generated by Django 4.0.4 on 2022-05-11 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_bale_verification_by_bale_verification_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='is_used',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
