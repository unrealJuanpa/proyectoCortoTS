import sqlite3

# Creamos una conexión a la base de datos
conn = sqlite3.connect('BD.db')
conn.execute('''
             CREATE TABLE mediciones
             (
                 id INT AUTO_INCREMENT,
                 frecuencia FLOAT NOT NULL,
                 duracion FLOAT NOT NULL,
                 intensidad FLOAT NOT NULL,
                 escuchado INT NOT NULL,
                 createdAt DATETIME,
                 updatedAt DATETIME,
                 PRIMARY KEY(id)
             );
             ''')

# Guardamos los cambios
conn.commit()
# Cerramos la conexion
conn.close()
