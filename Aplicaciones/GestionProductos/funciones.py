from .models import  DetalleVenta
from django.db.models import Sum, F
from django.db.models.functions import ExtractYear, ExtractMonth
from datetime import datetime, timedelta

#Librerias de prediccion
import pandas as pd
import statsmodels.api as sm
from pmdarima import auto_arima


def prediccionProducto(datos):
    df_ventas = pd.DataFrame(datos)

    df_ventas.fecha = pd.to_datetime(df_ventas.fecha, dayfirst=True);
    df_ventas.set_index("fecha", inplace=True);
    #asignar una frecuencia en este caso 'd' es dato diario lunes a domingo
    df_ventas = df_ventas.asfreq('d');
    # Obtener la fecha y hora actual
    fecha_actual = datetime.now();
    #completa el df de la primera fecha obtenida de la bd hasta la fecha actual y rellena los valores faltantes a 0
    df_ventas = df_ventas.reindex(pd.date_range(start=df_ventas.index.min(), end=fecha_actual, freq='d'));
    # Rellenar los NaN con cero para los días que no son domingos
    df_ventas = df_ventas.fillna(0)

    modelo_arima = auto_arima(df_ventas['cantidad_total'],
          start_p=0,
          start_q=0,
          max_p=5,
           max_q=5,
           seasonal=True,
           m=12,
           trace=True)
    order = modelo_arima.order
    seasonal_order = modelo_arima.seasonal_order
    model_sarima = sm.tsa.statespace.SARIMAX(df_ventas['cantidad_total'],
                                          order=order,               # Parámetros ARIMA (p, d, q)
                                          seasonal_order=seasonal_order,  # Parámetros estacionales (P, D, Q, s)
                                          trend='c')    
    result_sarima = model_sarima.fit()
    fecha_actual = datetime.now()
    # Calcular la fecha final que sea una semana después
    fecha_final = fecha_actual + timedelta(days=7)
    predicciones = result_sarima.predict(start=fecha_actual, end=fecha_final)

    #Suma las predicciones que realizo dando total de la prediccion en una semana
    suma_predicciones = predicciones.sum()

    return suma_predicciones

def obtener_productos_ordenados(ordering):
    return list(
        DetalleVenta.objects
        .values(
            'id_producto_det__nombre_producto',
            'id_producto_det__id_marca_producto__nombre_marca'
        )
        .annotate(
            Cantidad=Sum('cantidad'),
            nombre_producto=F('id_producto_det__nombre_producto'),
            nombre_marca=F('id_producto_det__id_marca_producto__nombre_marca')
        )
        .order_by(ordering)
        .values('nombre_producto', 'nombre_marca', 'Cantidad')[:5]
    )

def obtener_mes_con_mas_ventas(producto_nombre, marca_nombre, year):
    return list(
        DetalleVenta.objects
        .filter(
            id_producto_det__nombre_producto=producto_nombre,
            id_producto_det__id_marca_producto__nombre_marca=marca_nombre,
            fecha__year=year
        )
        .annotate(
            Anio=ExtractYear('fecha'),
            Mes=ExtractMonth('fecha'),
            nombre_producto=F('id_producto_det__nombre_producto'),
            nombre_marca=F('id_producto_det__id_marca_producto__nombre_marca')
        )
        .values('Anio', 'Mes', 'nombre_producto', 'nombre_marca')
        .annotate(Cantidad=Sum('cantidad'))
        .order_by('-Anio', '-Cantidad')
    )[:1]

def obtener_ultimos_n_meses(producto_nombre, marca_nombre, n):
    return list(
        DetalleVenta.objects
        .filter(
            id_producto_det__nombre_producto=producto_nombre,
            id_producto_det__id_marca_producto__nombre_marca=marca_nombre
        )
        .annotate(
            Anio=ExtractYear('fecha'),
            Mes=ExtractMonth('fecha'),
            nombre_producto=F('id_producto_det__nombre_producto'),
            nombre_marca=F('id_producto_det__id_marca_producto__nombre_marca')
        )
        .values('Anio', 'Mes', 'nombre_producto', 'nombre_marca')
        .annotate(Cantidad=Sum('cantidad'))
        .order_by('-Anio', '-Mes')
    )[:n]

def obtener_ultimas_n_dias(producto_nombre, marca_nombre, n):
    fecha_fin = datetime.now().date()
    fecha_inicio = fecha_fin - timedelta(days=n)
    ultimasSemana = list(
        DetalleVenta.objects
        .filter(
            id_producto_det__nombre_producto=producto_nombre,
            id_producto_det__id_marca_producto__nombre_marca=marca_nombre,
            fecha__range=(fecha_inicio, fecha_fin)
        )
        .values('fecha')
        .annotate(Cantidad=Sum('cantidad'))
    )

    fechas_rango = [fecha_fin - timedelta(days=i) for i in range(n + 1)]
    fechas_generadas = [{'fecha': fecha, 'Cantidad': 0} for fecha in fechas_rango if fecha not in [venta['fecha'] for venta in ultimasSemana]]
    ultimasSemana.extend(fechas_generadas)
    ultimasSemana.sort(key=lambda x: x['fecha'], reverse=True)
    resultados = ultimasSemana[:n]
    for resultado in resultados:
        resultado['fecha'] = resultado['fecha'].strftime('%Y-%m-%d')
    return resultados