-- Conectar a la base de datos recién creada
\c tienda_db;

-- TODO: Definir las tablas del sistema

-- Tabla de usuarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de productos
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de carritos
CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Tabla de items del carrito
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Otorgar permisos al usuario
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tienda_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO tienda_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO tienda_user;

-- Asegurar que los privilegios futuros también se otorguen
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO tienda_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO tienda_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO tienda_user;

-- Insertar datos de prueba
INSERT INTO users (username, email, password_hash) VALUES
('ana', 'ana@email.com', 'hash1'),
('juan', 'juan@email.com', 'hash2');

INSERT INTO products (name, description, price, stock, image_url) VALUES
('Shampoo Nutritivo', 'Shampoo para cabello seco y maltratado', 25000.00, 30, 'https://ejemplo.com/shampoo.jpg'),
('Acondicionador Reparador', 'Acondicionador con keratina', 27000.00, 25, 'https://ejemplo.com/acondicionador.jpg');