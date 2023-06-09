# Generated by Django 4.0.5 on 2022-06-25 12:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0005_rename_s_special_inhousegrade_is_special'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('association', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('dated', models.DateField()),
                ('accountno', models.CharField(max_length=20, verbose_name='Account Number')),
                ('bank_name', models.CharField(max_length=20, verbose_name='Bank name')),
                ('accountname', models.CharField(max_length=20, verbose_name='Account Name')),
                ('amount', models.FloatField(verbose_name='Amount Paid')),
                ('desc', models.TextField(blank=True, null=True)),
                ('receipt', models.ImageField(null=True, upload_to='receipt', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'PNG', 'JPG', 'jpg', 'pdf'])])),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.season')),
                ('society', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='association.association')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
