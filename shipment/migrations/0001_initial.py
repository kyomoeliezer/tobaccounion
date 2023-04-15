# Generated by Django 4.0.4 on 2022-05-07 14:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('auths', '0001_initial'),
        ('processing', '0001_initial'),
        ('inventory', '0001_initial'),
        ('market', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=500, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=10, null=True)),
                ('license', models.CharField(blank=True, max_length=500, null=True)),
                ('nida', models.CharField(blank=True, max_length=40, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Driver',
                'verbose_name_plural': 'Drivers',
                'db_table': 'driver',
            },
        ),
        migrations.CreateModel(
            name='GeneralShipment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('shipment_number', models.CharField(blank=True, max_length=50, null=True)),
                ('on_loading', models.BooleanField(default=True)),
                ('on_receiving', models.BooleanField(default=True)),
                ('shipment_date', models.DateTimeField(blank=True, null=True)),
                ('delivery_date', models.DateTimeField(blank=True, null=True)),
                ('shipmet_status', models.CharField(blank=True, choices=[('NOT_STARTED', 'Not Started'), ('PENDING', 'Pending'), ('LOADING', 'Loading'), ('ON_SHIPPING', 'On Shipping'), ('DELIVERED', 'Delivered')], max_length=40, null=True)),
                ('is_closed_transporting', models.BooleanField(default=False)),
                ('is_closed_receiving', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipment.driver')),
                ('from_warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='general_from', to='inventory.warehouse')),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='general_receiver', to='auths.staff')),
                ('to_warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='general_to', to='inventory.warehouse')),
            ],
            options={
                'verbose_name': 'General Shipment',
                'verbose_name_plural': 'General Shipments',
            },
        ),
        migrations.CreateModel(
            name='MarketProcessingShipment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('shipment_number', models.CharField(blank=True, max_length=50, null=True)),
                ('on_loading', models.BooleanField(default=True)),
                ('on_receiving', models.BooleanField(default=True)),
                ('shipment_date', models.DateTimeField(blank=True, null=True)),
                ('delivery_date', models.DateTimeField(blank=True, null=True)),
                ('shipmet_status', models.CharField(blank=True, choices=[('NOT_STARTED', 'Not Started'), ('PENDING', 'Pending'), ('LOADING', 'Loading'), ('ON_SHIPPING', 'On Shipping'), ('DELIVERED', 'Delivered')], max_length=40, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipment.driver')),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.market')),
                ('market_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='market.marketticketrequest')),
                ('personnel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='processing_transpoter', to='auths.staff')),
                ('personnel_receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='processing_receiver', to='auths.staff')),
                ('processing_centre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processing.processingcentre')),
            ],
            options={
                'verbose_name': 'processing Shipment',
                'verbose_name_plural': 'Processing Shipments',
                'db_table': 'market_processing_shipment',
            },
        ),
        migrations.CreateModel(
            name='MarketWarehouseShipment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('shipment_number', models.CharField(blank=True, max_length=50, null=True)),
                ('on_loading', models.BooleanField(default=True)),
                ('on_receiving', models.BooleanField(default=True)),
                ('shipment_date', models.DateTimeField(blank=True, null=True)),
                ('delivery_date', models.DateTimeField(blank=True, null=True)),
                ('shipmet_status', models.CharField(blank=True, choices=[('NOT_STARTED', 'Not Started'), ('PENDING', 'Pending'), ('LOADING', 'Loading'), ('ON_SHIPPING', 'On Shipping'), ('DELIVERED', 'Delivered')], max_length=40, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipment.driver')),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.market')),
                ('market_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='market.marketticketrequest')),
                ('personnel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='market_warehousetranspoter', to='auths.staff')),
                ('personnel_receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='market_warehouse_receiver', to='auths.staff')),
            ],
            options={
                'verbose_name': 'Market Shipment',
                'verbose_name_plural': 'Market Shipments',
                'db_table': 'market_warehouse_shipment',
            },
        ),
        migrations.CreateModel(
            name='SalesShipment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('shipment_number', models.CharField(blank=True, max_length=50, null=True)),
                ('on_loading', models.BooleanField(default=True)),
                ('on_receiving', models.BooleanField(default=True)),
                ('shipment_date', models.DateTimeField(blank=True, null=True)),
                ('delivery_date', models.DateTimeField(blank=True, null=True)),
                ('shipmet_status', models.CharField(blank=True, choices=[('NOT_STARTED', 'Not Started'), ('PENDING', 'Pending'), ('LOADING', 'Loading'), ('ON_SHIPPING', 'On Shipping'), ('DELIVERED', 'Delivered')], max_length=40, null=True)),
                ('sales_location', models.CharField(blank=True, max_length=500, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipment.driver')),
                ('personnel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='on_sales', to='auths.staff')),
                ('processing_centre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processing.processingcentre')),
            ],
            options={
                'verbose_name': 'Sales Shipment',
                'verbose_name_plural': 'Sales Shipments',
                'db_table': 'sales_shipment',
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('track_name', models.CharField(blank=True, max_length=50, null=True)),
                ('reg_number', models.CharField(blank=True, max_length=50, null=True)),
                ('document_number', models.CharField(blank=True, max_length=50, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Track',
                'verbose_name_plural': 'Tracks',
                'db_table': 'track',
            },
        ),
        migrations.CreateModel(
            name='WarehouseProcessingShipment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('shipment_number', models.CharField(blank=True, max_length=50, null=True)),
                ('on_loading', models.BooleanField(default=True)),
                ('on_receiving', models.BooleanField(default=True)),
                ('shipment_date', models.DateTimeField(blank=True, null=True)),
                ('delivery_date', models.DateTimeField(blank=True, null=True)),
                ('shipmet_status', models.CharField(blank=True, choices=[('NOT_STARTED', 'Not Started'), ('PENDING', 'Pending'), ('LOADING', 'Loading'), ('ON_SHIPPING', 'On Shipping'), ('DELIVERED', 'Delivered')], max_length=40, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipment.driver')),
                ('personnel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='warehouse_processing_transpoter', to='auths.staff')),
                ('personnel_receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='warehouse_receiver', to='auths.staff')),
                ('processing_centre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processing.processingcentre')),
                ('track', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipment.track')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.warehouse')),
            ],
            options={
                'verbose_name': 'processing Shipment',
                'verbose_name_plural': 'Processing Shipments',
                'db_table': 'warehouse_processing_shipment',
            },
        ),
        migrations.CreateModel(
            name='WarehouseShipment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('shipment_number', models.CharField(blank=True, max_length=50, null=True)),
                ('on_loading', models.BooleanField(default=True)),
                ('on_receiving', models.BooleanField(default=True)),
                ('shipment_date', models.DateTimeField(blank=True, null=True)),
                ('delivery_date', models.DateTimeField(blank=True, null=True)),
                ('shipmet_status', models.CharField(blank=True, choices=[('NOT_STARTED', 'Not Started'), ('PENDING', 'Pending'), ('LOADING', 'Loading'), ('ON_SHIPPING', 'On Shipping'), ('DELIVERED', 'Delivered')], max_length=40, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipment.driver')),
                ('from_warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouse_bale', to='inventory.warehouse')),
                ('personnel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transpoter', to='auths.staff')),
                ('personnel_receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='auths.staff')),
                ('to_warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.warehouse')),
                ('track', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipment.track')),
            ],
            options={
                'verbose_name': 'WareHouse Shipment',
                'verbose_name_plural': 'Warehouse Shipments',
                'db_table': 'warehouse_shipment',
            },
        ),
        migrations.CreateModel(
            name='WarehouseShipmentBale',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('transport_weight', models.FloatField(blank=True, null=True)),
                ('received_weight', models.FloatField(blank=True, null=True)),
                ('delivery_status', models.CharField(blank=True, choices=[('NORMAL', 'Normal'), ('DESTUCTED', 'DESTRUCTED')], default='', max_length=40, null=True)),
                ('bale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.bale', verbose_name='warehouse_bale')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('shipment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipment.warehouseshipment')),
            ],
            options={
                'verbose_name': 'WarehouseShipmentBale',
                'verbose_name_plural': 'WarehouseShipmentBales',
                'db_table': 'warehouse_shipment_bale',
            },
        ),
        migrations.CreateModel(
            name='WarehouseProcessingShipmentBale',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('transport_weight', models.FloatField(blank=True, null=True)),
                ('received_weight', models.FloatField(blank=True, null=True)),
                ('delivery_status', models.CharField(blank=True, choices=[('NORMAL', 'Normal'), ('DESTUCTED', 'DESTRUCTED')], default='', max_length=40, null=True)),
                ('bale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.bale')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('shipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shipment.warehouseprocessingshipment')),
            ],
            options={
                'verbose_name': 'WarehoseProcessingShipmentBale',
                'verbose_name_plural': 'WarehoseProcessingShipmentBales',
                'db_table': 'warehouse_processing_shipment_bale',
            },
        ),
        migrations.CreateModel(
            name='SalesShipmentBale',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('shipment_bale_weight', models.FloatField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product_bale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processing.productbale', verbose_name='processing_bale')),
                ('sales_shipment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipment.salesshipment')),
            ],
            options={
                'verbose_name': 'SalesShipmentBale',
                'verbose_name_plural': 'SalesShipmentBales',
                'db_table': 'sales_shipment_bale',
            },
        ),
        migrations.AddField(
            model_name='salesshipment',
            name='track',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipment.track'),
        ),
        migrations.CreateModel(
            name='MarketWarehouseShipmentBale',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('transport_weight', models.FloatField(blank=True, null=True)),
                ('received_weight', models.FloatField(blank=True, null=True)),
                ('delivery_status', models.CharField(blank=True, choices=[('NORMAL', 'Normal'), ('DESTUCTED', 'DESTRUCTED')], default='', max_length=40, null=True)),
                ('bale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.bale')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('shipment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipment.marketwarehouseshipment')),
            ],
            options={
                'verbose_name': 'MarketWarehouseShipmentBale',
                'verbose_name_plural': 'MarketWarehouseShipmentBales',
                'db_table': 'market_warehouse_shipment_bale',
            },
        ),
        migrations.AddField(
            model_name='marketwarehouseshipment',
            name='track',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipment.track'),
        ),
        migrations.AddField(
            model_name='marketwarehouseshipment',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.warehouse'),
        ),
        migrations.CreateModel(
            name='MarketProcessingShipmentBale',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('transport_weight', models.FloatField(blank=True, null=True)),
                ('received_weight', models.FloatField(blank=True, null=True)),
                ('delivery_status', models.CharField(blank=True, choices=[('NORMAL', 'Normal'), ('DESTUCTED', 'DESTRUCTED')], default='', max_length=40, null=True)),
                ('bale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.bale', verbose_name='warehouse_bale')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('shipment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipment.marketprocessingshipment')),
            ],
            options={
                'verbose_name': 'Market Processing Shipment bale',
                'verbose_name_plural': 'Market Processing Shipment bales',
                'db_table': 'market_processing_shipment_bale',
            },
        ),
        migrations.AddField(
            model_name='marketprocessingshipment',
            name='track',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipment.track'),
        ),
        migrations.CreateModel(
            name='GeneralShipmentBale',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('transport_weight', models.FloatField(blank=True, null=True)),
                ('receiving_weight', models.FloatField(blank=True, null=True)),
                ('bale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.bale')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('general_shipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shipment.generalshipment')),
                ('shipment_grade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.cropgrade')),
            ],
            options={
                'verbose_name': 'GeneralShipmentBale',
                'verbose_name_plural': 'GeneralShipmentBales',
                'db_table': 'general_shipment_bale',
            },
        ),
        migrations.AddField(
            model_name='generalshipment',
            name='track',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shipment.track'),
        ),
        migrations.AddField(
            model_name='generalshipment',
            name='transporter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='general_transpoter', to='auths.staff'),
        ),
    ]