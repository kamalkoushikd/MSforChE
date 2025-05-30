# Generated by Django 4.2.19 on 2025-03-08 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atomic_number', models.IntegerField(unique=True)),
                ('period', models.IntegerField()),
                ('group', models.IntegerField(blank=True, null=True)),
                ('density', models.FloatField(blank=True, null=True)),
                ('boiling_point', models.FloatField(blank=True, null=True)),
                ('melting_point', models.FloatField(blank=True, null=True)),
                ('heat_capacity', models.FloatField(blank=True, null=True)),
                ('symbol', models.CharField(max_length=3, unique=True)),
                ('phase', models.CharField(default='Unknown', max_length=10)),
                ('electron_configuration', models.CharField(blank=True, max_length=100, null=True)),
                ('electron_configuration_semantic', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
