for(ultimosMeses in UltimoYear){
  if(UltimoYear[ultimosMeses].length !== 0){
    
    let VentasUltimoYear = UltimoYear[ultimosMeses];
    let fechas = VentasUltimoYear.map(fecha => `${obtenerNombreMes(fecha.Mes)} del ${fecha.Anio}`)
    let cantidad = VentasUltimoYear.map(fecha => fecha.Cantidad)
      let elementoCanvas = `UltimoYear${llaves[ultimosMeses]}`;
      const ctx1 = document.getElementById(elementoCanvas);
      new Chart(ctx1, {
        type: 'bar',
        data: {
          labels: fechas.reverse(),
          datasets: [{
            label: 'Ventas por Mes',
            data: cantidad.reverse(),
            backgroundColor: [
              '#ea580c',
              '#84cc16',
              '#22d3ee',
              '#a855f7',
              '#ef4444',
              '#14b8a6',
              '#db2777',
              '#e11d48',
              '#7e22ce'
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
    }else{
      let buscarCanvas = `${llaves[ultimosMeses]}1`;
      const grafica = document.getElementById(buscarCanvas);
      grafica.innerHTML = "No hay datos necesarios para mostrar una grafica"
    }
}


for(key in ultimasSemana){
  let VentasUltimasSemenas = ultimasSemana[key];
  let fechasS = VentasUltimasSemenas.map(fecha => fecha.fecha)
  let cantidadS = VentasUltimasSemenas.map(fecha => fecha.Cantidad)
  let elementoCanvas = `ultimasSemana${llaves[key]}`;
  const ctx2 = document.getElementById(elementoCanvas);
  new Chart(ctx2, {
    type: 'bar',
    data: {
      labels: fechasS.reverse(),
      datasets: [{
        label: 'Ventas por Dia',
        data: cantidadS.reverse(),
        backgroundColor: [
          '#ea580c',
          '#84cc16',
          '#22d3ee',
          '#a855f7',
          '#ef4444',
          '#14b8a6',
          '#db2777',
          '#e11d48',
          '#7e22ce'
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
}

// mesVentasCurso
// mesVentasPasado
for(key in mesVentasCurso){
  if(mesVentasCurso[key].length !== 0 || mesVentasPasado[key].length !== 0){
    let fechaMesPasado, fechaMesActual, cantidadMesPasado, cantidadMesActual;
    if(mesVentasPasado[0].length === 0){
      fechaMesPasado = "No hay datos del Año Pasado"
      cantidadMesPasado = 0;
    }else{
      fechaMesPasado = obtenerNombreMes(mesVentasPasado[0][0].Mes) + " del " + mesVentasPasado[0][0].Anio + " con " + mesVentasPasado[0][0].Cantidad + " ventas";
      cantidadMesPasado = mesVentasPasado[0][0].Cantidad;
    }
    if(mesVentasCurso[0].length === 0){
      fechaMesActual = "No hay datos del Año Actual"
      cantidadMesActual = 0;
    }else{
      fechaMesActual = obtenerNombreMes(mesVentasCurso[0][0].Mes) + " del " + mesVentasCurso[0][0].Anio + " con " + mesVentasCurso[0][0].Cantidad + " ventas";
      cantidadMesActual = mesVentasCurso[0][0].Cantidad;
    }
    
    let elementoCanvas = `mesVentas${llaves[key]}`;
    const ctx = document.getElementById(elementoCanvas);
      new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: [fechaMesPasado, fechaMesActual],
          datasets: [{
            label: 'Ventas',
            data: [cantidadMesPasado, cantidadMesActual],
            backgroundColor: [
              '#ea580c',
              '#84cc16',
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
  }else{
    let buscarCanvas = `${llaves[key]}3`;
      const grafica = document.getElementById(buscarCanvas);
      grafica.innerHTML = "No hay datos necesarios para mostrar una grafica";
  }
}

function obtenerNombreMes(numeroMes) {
  const meses = {
    1: 'Enero',
    2: 'Febrero',
    3: 'Marzo',
    4: 'Abril',
    5: 'Mayo',
    6: 'Junio',
    7: 'Julio',
    8: 'Agosto',
    9: 'Septiembre',
    10: 'Octubre',
    11: 'Noviembre',
    12: 'Diciembre'
  };
    
  // Verificar si el número de mes es válido
  if (meses[numeroMes]) {
    return meses[numeroMes];
  } else {
    return 'Mes inválido';
  }
}


//Mostrar resultados de predicciones y compras
for(key in prediccion){
  let prediccionProduct = prediccion[key];
  let varElemento = `prediccion${llaves[key]}`;
  const elemento = document.getElementById(varElemento);
  const llave = `${llaves[key]}`;
  const valorLlave = productos[llave];

  if (prediccionProduct[valorLlave] === 'No hay suficientes datos') {
    elemento.innerHTML = "No hay suficientes ventas para realizar una prediccion";
  } else {
    if(prediccionProduct[valorLlave] <= 0 ){
      elemento.innerHTML = 0;
    }else{
      elemento.innerHTML = Math.floor(prediccionProduct[valorLlave]);
    }
  }
}


for(key in compras){
  let prediccionProduct = prediccion[key];
  let comprasProduct = compras[key];
  let varElemento = `compra${llaves[key]}`;
  const elemento = document.getElementById(varElemento);

  const llave = `${llaves[key]}`;
  const valorLlave = productos[llave];

  if (prediccionProduct[valorLlave] === 'No hay suficientes datos') {
    elemento.innerHTML = "No hay suficientes ventas para calcular una compra";
  } else {
    const valorPrediccion = Math.floor(prediccionProduct[valorLlave]) - comprasProduct;
    if(valorPrediccion <= 0 ){
      elemento.innerHTML = 0;
    }else{
      elemento.innerHTML = valorPrediccion;
    }
  }
}
