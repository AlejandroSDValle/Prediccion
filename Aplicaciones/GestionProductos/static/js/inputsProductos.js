const productoInput = document.querySelector("#producto");
const productosPrediccion = document.querySelector("#productosPrediccion");
const listaProductos = document.querySelector("#listaProductos");

let productos = [];
productoInput.addEventListener("input", leerDatos);

function leerDatos(e){
    var valor = productoInput.value;
    if (valor.includes(',')) {
        productos.push(e.target.value.split(",")[0]);
        productoInput.value = '';
        
        document.querySelector("#cantidad").value = productos.length;
        
        const num = parseInt(document.querySelector("#cantidad").value);

        const listaProducto = document.createElement("LI");
        listaProducto.classList.add("list-group-item", "d-flex", "justify-content-between", "align-items-center");
        listaProductos.appendChild(listaProducto);

        const input = document.createElement("INPUT");
        input.setAttribute("type", "hidden");
        input.value = productos[(num)- 1];
        input.setAttribute("name", `product${(num)- 1}`);
        listaProducto.appendChild(input);
        
        const producto = document.createElement("SPAN");
        producto.textContent = productos[(num)- 1];  
        producto.classList.add("me-auto", "nombre-producto");
        listaProducto.appendChild(producto);
        
        const eliminar = document.createElement("SPAN");
        eliminar.classList.add("badge", "bg-danger", "rounded-pill", "eliminar");
        eliminar.style.cursor = "pointer";
        eliminar.textContent = "X";
        listaProducto.appendChild(eliminar);
        
    }

}

listaProductos.addEventListener("click", eliminarProducto);

function eliminarProducto(e){
    if(e.target.classList.contains("eliminar")){
        const nomProducto = e.target.parentElement.querySelector(".nombre-producto").textContent;
        let indice = productos.indexOf(nomProducto);
        if (indice !== -1) {
            productos.splice(indice, 1);
        }
        const elementoLiAEliminar = e.target.parentElement;
        // var elementoLiAEliminar = document.getElementById(posProducto);
        listaProductos.removeChild(elementoLiAEliminar)
        document.querySelector("#cantidad").value = productos.length;
    }
    
}

function cargarLoader(){
    const loader = document.querySelector(".loader");
    loader.style.display = "block";
}