from django.db import models

class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nombre_marca = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return f"{self.nombre_marca} - {self.id_marca}"

    class Meta:
        # Nombre personalizado para la tabla en la base de datos
        db_table = 'cat_marcas'

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    id_marca_producto = models.ForeignKey(Marca, on_delete=models.CASCADE)
    nombre_producto = models.CharField(max_length=20)
    precio_venta = models.DecimalField(max_digits=4, decimal_places=2)
    stock_producto = models.SmallIntegerField()

    def __str__(self) -> str:
        return f"{self.nombre_producto}"

    class Meta:
        db_table = 'cat_productos'

class DetalleVenta(models.Model):
    id_det_venta = models.AutoField(primary_key=True)
    id_producto_det = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto_det')
    cantidad = models.SmallIntegerField()
    fecha = models.DateField()

    class Meta:
        db_table = 'det_venta'