# Generated by Django 4.0.4 on 2022-05-07 14:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'verbose_name': 'Association',
                'verbose_name_plural': 'Associations',
                'db_table': 'association',
            },
        ),
        migrations.CreateModel(
            name='Farmer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('first_name', models.CharField(blank=True, max_length=500, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=500, null=True)),
                ('last_name', models.CharField(blank=True, max_length=500, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=500, null=True)),
                ('farmer_code', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'verbose_name': 'Farmer',
                'verbose_name_plural': 'Farmers',
                'db_table': 'farmer',
            },
        ),
    ]
