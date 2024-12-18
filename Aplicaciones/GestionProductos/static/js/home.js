function graficar(data, canvasId, titulo) {
  if (data.length > 0) {
      let productos = data.map(producto => `${producto.nombre_marca} ${producto.nombre_producto}`);
      let cantidades = data.map(producto => producto.Cantidad);

      const ctx = document.getElementById(canvasId);
      new Chart(ctx, {
          type: 'bar',
          data: {
              labels: productos,
              datasets: [{
                  label: titulo,
                  data: cantidades,
                  backgroundColor: [
                      '#ea580c',
                      '#84cc16',
                      '#22d3ee',
                      '#a855f7',
                      '#ef4444',
                  ],
                  borderWidth: 1
              }]
          },
          options: {
              scales: {
                  y: {
                      beginAtZero: true
                  }
              }
          }
      });
  } else {
      const grafica = document.getElementById(canvasId);
      grafica.innerHTML = "No hay datos necesarios para mostrar una gráfica";
  }
}

graficar(masVendidos, 'masVendidos', 'Productos más Vendidos');
graficar(menosVendidos, 'menosVendidos', 'Productos menos Vendidos');
        