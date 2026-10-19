-- =====================================================================
-- ESQUEMA DE BASE DE DATOS: HIPOTECA INVERSA CL
-- Sistema de Simulación y Gestión de Hipotecas Inversas en Colombia
-- =====================================================================

-- 1. Tabla de Solicitantes
CREATE TABLE IF NOT EXISTS solicitantes (
    nombre VARCHAR(100) NOT NULL,
    identificacion VARCHAR(20) PRIMARY KEY NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    edad INT NOT NULL
);

-- 2. Tabla de Viviendas
CREATE TABLE IF NOT EXISTS viviendas (
    ciudad VARCHAR(100) NOT NULL,
    barrio VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    identificacion_propietario VARCHAR(20) NOT NULL,
    valor DECIMAL(15,2) NOT NULL,
    PRIMARY KEY (direccion),
    CONSTRAINT fk_solicitante_propietario 
        FOREIGN KEY (identificacion_propietario) 
        REFERENCES solicitantes(identificacion) 
        ON DELETE CASCADE
);

-- 3. Índices de optimización
CREATE INDEX IF NOT EXISTS idx_viviendas_propietario 
    ON viviendas(identificacion_propietario);

-- 4. Datos de prueba iniciales (Seed Data)
INSERT INTO solicitantes (nombre, identificacion, fecha_nacimiento, edad)
VALUES 
    ('Beatriz Elena Montoya', '1022345678', '1953-03-12', 72),
    ('Carlos Andrés Ramírez', '1098765432', '1959-07-25', 66),
    ('Alba Lucía Jaramillo', '1033445566', '1945-11-04', 80)
ON CONFLICT (identificacion) DO NOTHING;

INSERT INTO viviendas (ciudad, barrio, direccion, identificacion_propietario, valor)
VALUES 
    ('Medellín', 'El Poblado', 'Carrera 43A # 1-50', '1022345678', 350000000.00),
    ('Bogotá', 'Chapinero', 'Calle 67 # 7-30', '1098765432', 420000000.00),
    ('Cali', 'Granada', 'Avenida 9N # 14-22', '1033445566', 280000000.00)
ON CONFLICT (direccion) DO NOTHING;
