-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- Configurar zona horaria
SET timezone = 'America/Bogota';

-- Verificar y crear el usuario si no existe
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'tienda_user') THEN
        CREATE USER tienda_user WITH PASSWORD 'password123';
    END IF;
END
$$;

-- Verificar y crear la base de datos si no existe
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'tienda_db') THEN
        CREATE DATABASE tienda_db OWNER tienda_user;
    END IF;
END
$$;

-- Conceder privilegios
GRANT ALL PRIVILEGES ON DATABASE tienda_db TO tienda_user;

