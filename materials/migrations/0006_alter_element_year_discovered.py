# Generated by Django 4.2.19 on 2025-03-09 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0005_alter_element_year_discovered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='element',
            name='year_discovered',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
