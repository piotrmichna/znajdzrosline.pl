# Generated by Django 3.1.5 on 2021-02-02 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('botanical', '0002_plantbodytype_plntlibraries'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plntlibraries',
            name='body_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='botanical.plantbodytype'),
        ),
    ]