# proyecto_final
proyecto final de dataset covid-19


proyecto final de dataset covid-19

primero, necesitara una base de datos para empezar el proyecto aqui se las proporciono

CREATE DATABASE IF NOT EXISTS Covid_19;

-- Seleccionar la base de datos 
USE Covid_19;

-- Crear la tabla para almacenar imágenes 
CREATE TABLE datos_covid 
( id INT PRIMARY KEY AUTO_INCREMENT, tipo VARCHAR(20), -- Tipo de imagen (COVID, Normal, Opacidad, Viral Pneumonia, etc.) 
imagen LONGBLOB, -- Almacena la imagen como un objeto binario grande 
fuente VARCHAR(255), -- Fuente de la imagen (por ejemplo, RSNA, Kaggle, GitHub) 
CONSTRAINT fk_tipo CHECK (tipo IN ('COVID', 'Normal', 'Opacidad', 'Viral Pneumonia')), -- Asegura que el tipo sea uno de los especificados 
CONSTRAINT fk_fuente CHECK (fuente IN ('PadChest', 'GitHub', 'Kaggle', 'SIRM', 'RSNA', 'Chest X-Ray Images')), -- Asegura que la fuente sea una de las especificadas 
UNIQUE (tipo, fuente) -- Asegura que no haya duplicados de la misma imagen ); 
CREATE TABLE usuarios 
( id INT AUTO_INCREMENT PRIMARY KEY, 
correo VARCHAR(255) NOT NULL, 
contrasena VARCHAR(255) NOT NULL ); 
INSERT INTO usuarios (correo, contrasena) VALUES ('test@example.com', 'TestPassword123');

select * from datos_covid, usuarios;

Despues haber creado la base de datos en mysql cambiar el archivo conexion_mysql.py a tus credenciales de la base de datos

y pones a funcionar el codigo te pedira un login con el query que proporcione puedes ver cual es el correo y contraseña de prueba

los botones son intuitivos para agregar u editar simplemente haz clic en los campos que estan en blanco y poder registras tant el dato "tipo" y "fuente"

para edita o eliminar tienes que seleccionar un elemento de la tabla es decir hacer click en alguna fila y luego apretar el boton editar y si desea borrar el mismo proceso pero con el boton borrar

eso es todo.
