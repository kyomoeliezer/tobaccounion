# Generated by Django 4.0.5 on 2023-03-14 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipment', '0011_remove_generalshipmentreceivedbales_is_sent_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalshipment',
            name='is_sent_email',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
