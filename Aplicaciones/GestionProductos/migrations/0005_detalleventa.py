# Generated by Django 5.0.1 on 2024-01-06 03:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionProductos', '0004_alter_producto_id_producto'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id_det_venta', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.SmallIntegerField()),
                ('fecha', models.DateField()),
                ('id_producto_det', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GestionProductos.producto')),
            ],
            options={
                'db_table': 'det_venta',
            },
        ),
    ]
