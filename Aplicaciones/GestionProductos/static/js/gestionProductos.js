const formularioVC = document.getElementById('formularioVC');

if (formularioVC) {
    formularioVC.addEventListener('submit', validarForm);
}

const formulario = document.getElementById('formulario');

if (formulario) {
    formulario.addEventListener('submit', validarProducto);
}

function validarForm(e){
    e.preventDefault();

    var productoInput = document.getElementById("producto").value;
    var cantidadInput = document.getElementById("cantidad").value;

    const regex = /^(\w+(\.|\/)?\s?)+\s-\s(\w+(\.|\/)?\s?)+$/
    if (productoInput.trim() === '' || cantidadInput.trim() === '') {
        alert("Por favor, complete todos los campos.");
        
        return; 
    }
    
    if(!regex.test(productoInput)){
        alert("Ingrese el producto de la forma (Producto - Marca)");
        return;
    }
    if(cantidadInput <= 0){
        alert("La cantidad tiene que se mayor a 0");
        return;
    }
   
    this.submit(); 
}

function validarProducto(e){
    e.preventDefault();
   
    var productoInput = document.getElementById("producto").value;
    if(productos.length < 1){
        const regex = /^(\w+(\.|\/)?\s?)+\s-\s(\w+(\.|\/)?\s?)+$/
        if (productoInput.trim() === '') {
            alert("Por favor, complete todos los campos.");
            
            return; 
        }
        
        if(!regex.test(productoInput)){
            alert("Ingrese el producto de la forma (Producto - Marca)");
            return;
        }
    }
    
    this.submit(); 
}

