# Generated by Django 5.0.1 on 2024-01-06 05:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionProductos', '0005_detalleventa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalleventa',
            name='id_producto_det',
            field=models.ForeignKey(db_column='id_producto_det', on_delete=django.db.models.deletion.CASCADE, to='GestionProductos.producto'),
        ),
        migrations.AlterModelTable(
            name='marca',
            table='cat_marcas',
        ),
    ]
