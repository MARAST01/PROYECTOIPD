
CREATE TABLE calculos (
    id SERIAL PRIMARY KEY,
    operacion VARCHAR(255),
    resultado NUMERIC,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
