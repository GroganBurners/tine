# Generated by Django 2.0.12 on 2019-07-12 13:36

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='images/carousel')),
                ('img_alt', models.CharField(blank=True, max_length=50, null=True, verbose_name='Image alternative text (for screen readers)')),
                ('teaser_text', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=False)),
                ('order', models.PositiveSmallIntegerField()),
                ('use_button', models.BooleanField()),
                ('button_text', models.CharField(max_length=50)),
                ('button_link', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone_number', models.CharField(blank=True, default='353', max_length=16, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('street', models.CharField(blank=True, max_length=200)),
                ('county', models.CharField(blank=True, choices=[('D', 'Dublin'), ('KY', 'Kerry'), ('KE', 'Kildare'), ('KK', 'Kilkenny'), ('L', 'Limerick'), ('OY', 'Offaly'), ('T', 'Tipperary'), ('W', 'Waterford'), ('WX', 'Wexford'), ('WW', 'Wicklow')], default='KK', max_length=30)),
                ('eircode', models.CharField(blank=True, default='R95 XXXX', max_length=12)),
                ('country', models.CharField(blank=True, default='Ireland', max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('cash', models.BooleanField(default=False)),
                ('notes', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'ordering': ['-date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExpenseItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('vat_rate', models.DecimalField(decimal_places=2, default=13.5, max_digits=5)),
                ('quantity', models.DecimalField(decimal_places=2, default=1, max_digits=8)),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='gbs.Expense')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExpenseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='HeroImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='images/carousel')),
                ('img_alt', models.CharField(blank=True, max_length=50, null=True, verbose_name='Image alternative text (for screen readers)')),
                ('teaser_text', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=False)),
                ('use_button', models.BooleanField()),
                ('button_text', models.CharField(max_length=50)),
                ('button_link', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('invoice_id', models.CharField(blank=True, editable=False, max_length=6, null=True, unique=True)),
                ('invoiced', models.BooleanField(default=False)),
                ('draft', models.BooleanField(default=False)),
                ('cash', models.BooleanField(default=False)),
                ('paid_date', models.DateField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gbs.Customer')),
            ],
            options={
                'ordering': ['-date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('vat_rate', models.DecimalField(decimal_places=2, default=13.5, max_digits=5)),
                ('quantity', models.DecimalField(decimal_places=2, default=1, max_digits=8)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='gbs.Invoice')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('gas_service', 'Gas Service'), ('gas_combi_service', 'Gas Combi/Condensing Boiler Service'), ('gas_fire', 'Gas Fire Service'), ('gas_service_fire', 'Gas Boiler and Fire service together'), ('gas_install', 'Gas Install'), ('oil_service', 'Oil Service'), ('oil_combi_service', 'Oil Combi/Condensing Service'), ('oil_install', 'Oil Install'), ('repair_call_out', 'Repair Call Out Fee (First Hour)'), ('ber', 'Building Energy Rating')], max_length=30)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=6)),
                ('summer_offer', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone_number', models.CharField(blank=True, default='353', max_length=16, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('street', models.CharField(blank=True, max_length=200)),
                ('county', models.CharField(blank=True, choices=[('D', 'Dublin'), ('KY', 'Kerry'), ('KE', 'Kildare'), ('KK', 'Kilkenny'), ('L', 'Limerick'), ('OY', 'Offaly'), ('T', 'Tipperary'), ('W', 'Waterford'), ('WX', 'Wexford'), ('WW', 'Wicklow')], default='KK', max_length=30)),
                ('eircode', models.CharField(blank=True, default='R95 XXXX', max_length=12)),
                ('country', models.CharField(blank=True, default='Ireland', max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='expense',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gbs.Supplier'),
        ),
        migrations.AddField(
            model_name='expense',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gbs.ExpenseType'),
        ),
    ]
