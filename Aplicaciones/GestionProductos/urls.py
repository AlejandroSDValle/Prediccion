from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('compra/', views.compra, name="compra"),
    path('compraProducto/', views.compraProducto, name="compraProducto"),
    path('venta/', views.venta, name="venta"),
    path('ventaProducto/', views.ventaProducto, name="ventaProducto"),  
    path('prediccion/', views.prediccion, name="prediccion"), 
    path('APIPrediccion/', views.APIPrediccion, name="APIPrediccion"), 
]

