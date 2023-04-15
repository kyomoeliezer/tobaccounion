# Generated by Django 4.0.5 on 2022-06-25 13:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='is_canceled',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='receipt',
            field=models.ImageField(null=True, upload_to='receipt/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'PNG', 'JPG', 'jpg', 'pdf'])]),
        ),
    ]