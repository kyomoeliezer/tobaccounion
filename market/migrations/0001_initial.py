# Generated by Django 4.0.4 on 2022-05-07 14:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('association', '0002_initial'),
        ('core', '0001_initial'),
        ('inventory', '0001_initial'),
        ('auths', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('market_name', models.CharField(blank=True, max_length=500, null=True)),
                ('market_code', models.CharField(blank=True, max_length=500, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.region')),
            ],
            options={
                'verbose_name': 'Market',
                'verbose_name_plural': 'Markets',
                'db_table': 'market',
            },
        ),
        migrations.CreateModel(
            name='MarketTicketRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('ticket_request_name', models.CharField(blank=True, max_length=500, null=True)),
                ('number_of_tickets', models.IntegerField(blank=True, null=True)),
                ('sales_date', models.DateField(blank=True, null=True)),
                ('print_request_status', models.CharField(choices=[('PRINTED', 'Printed'), ('NOT_PRINTED', 'Not Printed')], default='Not Allocated', max_length=500)),
                ('on_pre_buying', models.BooleanField(default=True)),
                ('on_buying', models.BooleanField(default=True)),
                ('sales_number', models.IntegerField(blank=True, null=True)),
                ('mobile_clerk', models.CharField(blank=True, max_length=40, null=True, verbose_name='Mobile Clerk for PDF only ')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('market', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='market.market')),
                ('personnel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auths.staff')),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.season')),
                ('society', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='association.association')),
            ],
            options={
                'verbose_name': 'MarketTicketRequest',
                'verbose_name_plural': 'MarketTicketRequests',
                'db_table': 'market_ticket_request',
            },
        ),
        migrations.CreateModel(
            name='PrintRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('request_name', models.CharField(blank=True, max_length=500, null=True)),
                ('number_of_tickets', models.IntegerField(blank=True, null=True)),
                ('ticket_file', models.CharField(blank=True, max_length=500, null=True)),
                ('initial_ticket', models.IntegerField(blank=True, null=True)),
                ('last_ticket', models.IntegerField(blank=True, null=True)),
                ('print_request_status', models.CharField(choices=[('PRINTED', 'Printed'), ('NOT_PRINTED', 'Not Printed')], default='NOT_PRINTED', max_length=500)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'PrintRequest',
                'verbose_name_plural': 'PrintRequests',
                'db_table': 'print_request',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('ticket_number', models.CharField(blank=True, max_length=50, null=True)),
                ('qr_code', models.CharField(blank=True, max_length=500, null=True)),
                ('bar_code', models.CharField(blank=True, max_length=500, null=True)),
                ('rotated_bar_code', models.CharField(blank=True, max_length=500, null=True)),
                ('is_printed', models.BooleanField(default=False)),
                ('is_used', models.BooleanField(default=False)),
                ('no', models.IntegerField(blank=True, null=True, verbose_name='This is just a Ticket no but in interger format,used for ticket release')),
                ('Use_status', models.CharField(choices=[('INITIAL_MARKET', 'Initial Market')], default='INITIAL_MARKET', max_length=200)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('print_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='market.printrequest')),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
                'db_table': 'ticket',
            },
        ),
        migrations.CreateModel(
            name='PrintRequestTicket',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('print_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.printrequest')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.ticket')),
            ],
            options={
                'verbose_name': 'PrintRequestTicket',
                'verbose_name_plural': 'PrintRequestTickets',
                'db_table': 'print_request_ticket',
            },
        ),
        migrations.CreateModel(
            name='Pcn',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('no', models.IntegerField()),
                ('pcn_no', models.CharField(max_length=20, verbose_name='Pcn no')),
                ('is_data_verified', models.BooleanField(default=False, verbose_name='The farmer have verified the data?,1-YES,0-Not yet')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('nill', models.CharField(max_length=30, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('data_verification_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Verified_by', to=settings.AUTH_USER_MODEL)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='market.marketticketrequest')),
            ],
            options={
                'verbose_name': 'PCN',
                'verbose_name_plural': 'PCNs',
                'db_table': 'pcn',
            },
        ),
        migrations.CreateModel(
            name='MarketTiket',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('market_ticket_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='market.marketticketrequest')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.ticket')),
            ],
            options={
                'verbose_name': 'MarketTiket',
                'verbose_name_plural': 'MarketTikets',
                'db_table': 'market_ticket',
            },
        ),
        migrations.CreateModel(
            name='MarketTicketRequestPersonnel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('market_ticket_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='market.marketticketrequest')),
                ('personnel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auths.staff')),
            ],
            options={
                'verbose_name': 'Buyer Market',
                'verbose_name_plural': 'Buyer Markets',
                'db_table': 'market_ticket_request_personnel',
            },
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('full_name', models.CharField(blank=True, max_length=50, null=True)),
                ('buyer_code', models.CharField(blank=True, max_length=500, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Buyer',
                'verbose_name_plural': 'Buyers',
                'db_table': 'buyer',
            },
        ),
        migrations.CreateModel(
            name='Bale',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('primary_weight', models.FloatField(blank=True, null=True)),
                ('current_weight', models.FloatField(blank=True, null=True)),
                ('buyer_code', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.CharField(max_length=50, null=True)),
                ('remarks', models.CharField(max_length=50, null=True, verbose_name='Remarks / comments ')),
                ('price', models.FloatField(null=True, verbose_name='Price')),
                ('value', models.FloatField(null=True, verbose_name='Value')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('current_grade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_grade', to='core.cropgrade')),
                ('farmer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='association.farmer')),
                ('grade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='crop_grade', to='core.cropgrade')),
                ('in_house_grade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.inhousegrade')),
                ('market_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='market.marketticketrequest')),
                ('pcn', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='market.pcn')),
                ('ticket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='market.ticket', verbose_name='ticket')),
                ('verified_grade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='verified_grade', to='core.cropgrade')),
                ('warehouse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.warehouse', verbose_name='warehouse')),
            ],
            options={
                'verbose_name': 'Bale',
                'verbose_name_plural': 'Bales',
                'db_table': 'bale',
            },
        ),
    ]
