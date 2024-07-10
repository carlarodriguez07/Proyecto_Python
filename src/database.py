import mysql.connector

database = mysql.connector.connect(
    host = 'localhost',
    user = 'root', 
    password ='',
    database = 'recetas' 
)

if database.is_connected():
    print('Conexión exitosa a la base de datos')
else:
    print('Error en la conexión')


