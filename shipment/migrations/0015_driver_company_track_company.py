# Generated by Django 4.0.5 on 2023-03-21 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipment', '0014_transportcompany'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='shipment.transportcompany'),
        ),
        migrations.AddField(
            model_name='track',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='shipment.transportcompany'),
        ),
    ]
