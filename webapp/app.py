from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import os
from datetime import datetime

# TODO: Configurar la aplicación Flask
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'clave-por-defecto-cambiar')

# TODO: Configurar la URL de la API
API_URL = os.getenv('API_URL', 'http://api:8000')

@app.route('/')
def index():
    # TODO: Implementar página principal
    # Obtener productos destacados de la API
    try:
        response = requests.get(f"{API_URL}/api/v1/products/featured")
        response.raise_for_status()
        products = response.json()
    except requests.exceptions.RequestException as e:
        flash(f"Error al conectar con la API: {e}", "danger")
        products = []
        
    return render_template('index.html', products=products)

@app.route('/products')
def products():
    # TODO: Implementar página de productos
    # Obtener lista de productos de la API
    try:
        response = requests.get(f"{API_URL}/api/v1/products")
        response.raise_for_status()
        products = response.json()
    except requests.exceptions.RequestException as e:
        flash(f"Error al conectar con la API: {e}", "danger")
        products = []
        
    return render_template('products.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # TODO: Implementar lógica de login
        # Enviar datos a la API de autenticación
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            response = requests.post(f"{API_URL}/api/v1/auth/login", json={"username": username, "password": password})
            response.raise_for_status()
            
            user_data = response.json()
            session['logged_in'] = True
            session['user_id'] = user_data.get('user_id')
            session['username'] = user_data.get('username')
            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for('index'))
            
        except requests.exceptions.HTTPError as e:
            flash(f"Error de inicio de sesión: {response.json().get('detail')}", "danger")
        except requests.exceptions.RequestException as e:
            flash(f"Error al conectar con la API: {e}", "danger")
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # TODO: Implementar lógica de registro
        # Enviar datos a la API de registro
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        try:
            response = requests.post(f"{API_URL}/api/v1/auth/register", json={"username": username, "password": password, "email": email})
            response.raise_for_status()
            flash("Registro exitoso. Por favor, inicie sesión.", "success")
            return redirect(url_for('login'))
        except requests.exceptions.HTTPError as e:
            flash(f"Error de registro: {response.json().get('detail')}", "danger")
        except requests.exceptions.RequestException as e:
            flash(f"Error al conectar con la API: {e}", "danger")
            
    return render_template('register.html')

@app.route('/cart')
def cart():
    # TODO: Implementar página del carrito
    # Obtener carrito del usuario de la API
    
    if not is_logged_in():
        flash("Por favor, inicie sesión para ver su carrito.", "warning")
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    try:
        response = api_request(f"/api/v1/users/{user_id}/cart")
        response.raise_for_status()
        cart_items = response.json().get('items', [])
    except requests.exceptions.RequestException as e:
        flash(f"Error al obtener el carrito: {e}", "danger")
        cart_items = []
        
    return render_template('cart.html', cart_items=cart_items)

@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # TODO: Implementar agregar producto al carrito
    # Enviar request a la API
    
    if not is_logged_in():
        flash("Por favor, inicie sesión para agregar productos al carrito.", "warning")
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    quantity = int(request.form.get('quantity', 1))
    
    try:
        response = api_request(f"/api/v1/users/{user_id}/cart/add", method='POST', data={"product_id": product_id, "quantity": quantity})
        response.raise_for_status()
        flash("Producto agregado al carrito exitosamente.", "success")
    except requests.exceptions.RequestException as e:
        flash(f"Error al agregar producto al carrito: {e}", "danger")

    return redirect(url_for('products'))

@app.route('/logout')
def logout():
    # TODO: Implementar logout
    # Limpiar sesión
    session.clear()
    flash("Has cerrado sesión exitosamente.", "info")
    return redirect(url_for('index'))

# TODO: Función helper para hacer requests a la API
def api_request(endpoint, method='GET', data=None, headers=None):
    # TODO: Implementar función para hacer requests a la API
    url = f"{API_URL}{endpoint}"
    
    if method == 'POST':
        return requests.post(url, json=data, headers=headers)
    elif method == 'PUT':
        return requests.put(url, json=data, headers=headers)
    elif method == 'DELETE':
        return requests.delete(url, headers=headers)
    else: # GET
        return requests.get(url, headers=headers)

# TODO: Función para verificar si el usuario está logueado
def is_logged_in():
    # TODO: Verificar si hay sesión activa
    return session.get('logged_in') == True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)