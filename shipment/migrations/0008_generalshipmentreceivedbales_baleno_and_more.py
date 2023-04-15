# Generated by Django 4.0.5 on 2022-09-15 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0011_alter_bale_mn_market_alter_bale_mn_society'),
        ('shipment', '0007_generalshipmentreceivedbales'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalshipmentreceivedbales',
            name='baleno',
            field=models.CharField(max_length=300, null=True, verbose_name='Bale no'),
        ),
        migrations.AddField(
            model_name='generalshipmentreceivedbales',
            name='general_shipmentno',
            field=models.CharField(max_length=300, null=True, verbose_name='general_shipment no'),
        ),
        migrations.AddField(
            model_name='generalshipmentreceivedbales',
            name='in_house_gradeno',
            field=models.CharField(max_length=300, null=True, verbose_name='in_house_grade name'),
        ),
        migrations.AddField(
            model_name='generalshipmentreceivedbales',
            name='truckno',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='generalshipmentreceivedbales',
            name='bale',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='market.bale'),
        ),
        migrations.AlterField(
            model_name='generalshipmentreceivedbales',
            name='general_shipment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shipment.generalshipment'),
        ),
    ]
