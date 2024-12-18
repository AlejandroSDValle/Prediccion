from django.shortcuts import render, redirect
from .models import Producto, Marca, DetalleVenta
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

from .funciones import obtener_productos_ordenados, obtener_ultimas_n_dias, obtener_ultimos_n_meses, obtener_mes_con_mas_ventas, prediccionProducto

def home(request):
    masVendidos = obtener_productos_ordenados('-Cantidad')
    menosVendidos = obtener_productos_ordenados('Cantidad')
    pocoStock = Producto.objects.filter(stock_producto__lt=5).order_by('stock_producto')

    return render(request, "home.html",{
        "masVendidos": masVendidos,
        "menosVendidos": menosVendidos,
        "pocoStock": pocoStock
    })

def venta(request):
    productos = Producto.objects.all()
    return render(request, "ventaProducto.html",{
        "productos": productos
    })
    

def ventaProducto(request):
    producto = request.POST["producto"]
    cantidad = int(request.POST["cantidad"], 0)
    partes = producto.split(" - ")
    if not producto:
        messages.warning(request, "El producto no fue proporcionado.")
        return redirect('venta')  # Redirigir a la página venta

    try:
        marcaId = Marca.objects.get(nombre_marca=partes[1]).id_marca
        producto = Producto.objects.get(nombre_producto=partes[0], id_marca_producto=marcaId)
    except (Marca.DoesNotExist, Producto.DoesNotExist):
         messages.warning(request, "El producto o la marca no existen.")
         return redirect('venta')
    
    stock = producto.stock_producto - cantidad
    if stock < 0:
        messages.warning(request, f"No hay suficiente stock para realizar la venta. Stock actual: {stock + cantidad}")
        return redirect('venta')  # Redirigir a la página anterior o a donde sea necesario
    
    fecha_hoy = datetime.today().date()
    fecha_hoy_formateada = fecha_hoy.strftime('%Y-%m-%d')
    detVenta = DetalleVenta.objects.create(
        id_producto_det= producto,
        cantidad= cantidad,
        fecha= fecha_hoy_formateada
    )
    producto.stock_producto = stock
    producto.save()
    messages.success(request, "Producto vendido correctamente.")
    return redirect('venta')

def compra(request):
    productos = Producto.objects.all()
    return render(request, "AddProduct.html",{
        "productos": productos
    })

def compraProducto(request):
    producto = request.POST["producto"]
    cantidad = int(request.POST["cantidad"], 0)
    partes = producto.split(" - ")

    if not producto:
        messages.warning(request, "El producto no fue proporcionado.")
        return redirect('compra')  
    
    try:
        marcaId = Marca.objects.get(nombre_marca=partes[1]).id_marca
        producto = Producto.objects.get(nombre_producto=partes[0], id_marca_producto=marcaId)
    except (Marca.DoesNotExist, Producto.DoesNotExist):
         messages.warning(request, "El producto o la marca no existen.")
         return redirect('compra')
    
    marcaId = Marca.objects.get(nombre_marca=partes[1]).id_marca
    producto = Producto.objects.get(nombre_producto=partes[0], id_marca_producto=marcaId)

    stock = producto.stock_producto + cantidad
    producto.stock_producto = stock
    producto.save()
    messages.success(request, "Producto actualizado Correctamente")
    return redirect('compra')

def prediccion(request):
    productos = Producto.objects.all()
    return render(request, "prediccion.html",{
        "productos": productos
    })

def APIPrediccion(request):

    datos_post = {}
    context = {
        "mesVentasPasado": [],
        "mesVentasCurso": [],
        "UltimoYear": [],
        "ultimasSemana": []
    }
    resultadosPrediccion = []
    stocks = []

    for key, value in request.POST.items():
            # Agrega la clave y el valor al diccionario
            if key != "csrfmiddlewaretoken":
                datos_post[key] = value
            
    if(datos_post["cantidad"]):
        del datos_post["cantidad"]
    if datos_post["producto"] == "":
        del datos_post["producto"]
            
    for clave, valor in datos_post.items():
        if(not(len(valor.strip()) == 0)):
            
            producto_nombre, marca_nombre = valor.split(" - ")
            productos_encontrados = Producto.objects.filter(nombre_producto__icontains=producto_nombre).count()

            
            if(productos_encontrados ):
            
                # Obtener las ventas de cada día del producto ingresado para la predicción
                ventas = DetalleVenta.objects.filter(
                    id_producto_det__nombre_producto=producto_nombre,
                    id_producto_det__id_marca_producto__nombre_marca=marca_nombre
                ).values('fecha').annotate(cantidad_total=Sum('cantidad')).order_by('fecha')

                cantidad_registros = ventas.count()


                if(cantidad_registros < 31 ):
                    nuevo_resultado = {valor: "No hay suficientes datos"}
                    resultadosPrediccion.append(nuevo_resultado)
                else:
                    resultadoPrediccion = prediccionProducto(ventas)
                    nuevo_resultado = {valor: resultadoPrediccion}
                    resultadosPrediccion.append(nuevo_resultado)

                # Obtener el stock del producto
                try:
                    marca = Marca.objects.get(nombre_marca=marca_nombre)
                    producto = Producto.objects.get(nombre_producto=producto_nombre, id_marca_producto=marca)
                    stock_producto = producto.stock_producto
                    stocks.append(stock_producto)
                except ObjectDoesNotExist:
                    # Manejar el caso en el que no se encuentra el registro
                    messages.warning(request, "Algun producto de los que ingreso no existe.")
                    return redirect("prediccion")


                # Consulta para traer el mes con más ventas del año pasado
                mesVentasPasado = obtener_mes_con_mas_ventas(producto_nombre, marca_nombre, datetime.now().year - 1)
                context["mesVentasPasado"].append(mesVentasPasado)

                # Consulta para traer el mes con más ventas del año en curso
                mesVentasCurso = obtener_mes_con_mas_ventas(producto_nombre, marca_nombre, datetime.now().year)
                context["mesVentasCurso"].append(mesVentasCurso)

                # Consulta para los últimos 12 meses
                UltimoYear = obtener_ultimos_n_meses(producto_nombre, marca_nombre, 12)
                context["UltimoYear"].append(UltimoYear)

                # Ventas en los últimos 15 días
                ultimasSemana = obtener_ultimas_n_dias(producto_nombre, marca_nombre, 15)
                context["ultimasSemana"].append(ultimasSemana)
            else:
                messages.warning(request, "Algun producto de los que ingreso no existe.")
                return redirect("prediccion")
        else:
            messages.warning(request, "Ingreso un producto vacio intente nuevamente.")
            return redirect("prediccion")

    return render(request, "ResultadoPrediccion.html",{
        "productos": datos_post,
        "datos": context,
        "resultadosPrediccion": resultadosPrediccion,
        "stocks": stocks
    })
