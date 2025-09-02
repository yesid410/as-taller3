// TODO: Agregar funcionalidad JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // TODO: Inicializar componentes cuando cargue la página
    console.log("DOM cargado y listo.");

    // Escuchar clics en botones de "Agregar al Carrito"
    document.querySelectorAll('.add-to-cart-form').forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const productId = this.dataset.productId;
            addToCart(productId);
        });
    });
});

/**
 * Función para agregar productos al carrito con AJAX.
 * @param {number} productId El ID del producto a agregar.
 */
// TODO: Función para agregar productos al carrito con AJAX
async function addToCart(productId) {
    try {
        const response = await fetch(`/add-to-cart/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ quantity: 1 }) // Se podría ajustar la cantidad
        });

        if (response.ok) {
            const data = await response.json();
            alert("Producto agregado al carrito exitosamente!");
            // Opcional: actualizar el icono del carrito u otro elemento de la UI
        } else {
            const errorData = await response.json();
            alert(`Error al agregar al carrito: ${errorData.message}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert("Ocurrió un error al intentar agregar el producto.");
    }
}

/**
 * Función para actualizar la cantidad de un item en el carrito.
 * @param {number} itemId El ID del item del carrito.
 * @param {number} quantity La nueva cantidad.
 */
// TODO: Función para actualizar cantidad en el carrito
async function updateCartQuantity(itemId, quantity) {
    try {
        const response = await fetch(`/cart/update/${itemId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ quantity: quantity })
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log("Cantidad actualizada exitosamente:", data);
            // Actualizar la interfaz de usuario para reflejar el cambio
        } else {
            const errorData = await response.json();
            console.error('Error al actualizar la cantidad:', errorData);
            alert(`Error al actualizar la cantidad: ${errorData.message}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert("Ocurrió un error al actualizar la cantidad.");
    }
}

/**
 * Función para remover items del carrito.
 * @param {number} itemId El ID del item a remover.
 */
// TODO: Función para remover items del carrito
async function removeFromCart(itemId) {
    try {
        const response = await fetch(`/cart/remove/${itemId}`, {
            method: 'POST'
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Item eliminado del carrito:", data);
            // Eliminar el elemento de la interfaz de usuario
            document.querySelector(`#cart-item-${itemId}`).remove();
        } else {
            const errorData = await response.json();
            console.error('Error al remover el item:', errorData);
            alert(`Error al remover el item: ${errorData.message}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert("Ocurrió un error al intentar eliminar el item del carrito.");
    }
}