# Generated by Django 4.1.7 on 2023-03-06 10:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Preke',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pavadinimas', models.CharField(max_length=100, verbose_name='Pavadinimas')),
                ('kaina', models.FloatField(verbose_name='Kaina')),
                ('aprasymas', models.TextField(blank=True, help_text='LEGO aprasymas', max_length=1000, null=True, verbose_name='Aprašymas')),
                ('nuotrauka', models.ImageField(null=True, upload_to='nuotraukos', verbose_name='Nuotrauka')),
            ],
            options={
                'verbose_name': 'Preke',
                'verbose_name_plural': 'Prekes',
            },
        ),
        migrations.CreateModel(
            name='Uzsakymas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('uzsakymo_numeris', models.CharField(max_length=150, null=True, verbose_name='Uzsakymo numeris')),
                ('status', models.CharField(blank=True, choices=[('p', 'Patvirtinta'), ('v', 'Vykdoma'), ('a', 'Atsaukta'), ('i', 'Ivykdyta')], default='p', help_text='Statusas', max_length=1)),
                ('preke_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='eshop.preke', verbose_name='Preke_id')),
                ('vartotojas', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Uzsakymas',
                'verbose_name_plural': 'Uzsakymai',
            },
        ),
        migrations.CreateModel(
            name='Uzsakymo_eilute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kiekis', models.IntegerField(verbose_name='Kiekis')),
                ('preke', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='eshop.preke')),
                ('uzsakymas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eilutes', to='eshop.uzsakymas')),
            ],
            options={
                'verbose_name': 'Uzsakymo eilute',
                'verbose_name_plural': 'Uzsakymo eilutes',
            },
        ),
        migrations.CreateModel(
            name='Siuntimas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adresas', models.CharField(max_length=200, verbose_name='Adresas')),
                ('miestas', models.CharField(max_length=100, verbose_name='Miestas')),
                ('telefonas', models.IntegerField(verbose_name='Telefonas')),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('uzsakymas', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='eshop.uzsakymas')),
            ],
            options={
                'verbose_name': 'Siuntimas',
                'verbose_name_plural': 'Siuntimai',
            },
        ),
        migrations.CreateModel(
            name='Profilis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nuotrauka', models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
