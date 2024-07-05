from flask import Flask  # Importamos el framework Flask
from flask import render_template, request, redirect, url_for, flash  # Importamos el render para mostrar todos los templates
from flaskext.mysql import MySQL  # Importamos para conectarnos a la BD
from datetime import datetime  # Nos permitirá darle el nombre a la foto
import os  # Nos permite acceder a los archivos
from flask import send_from_directory  # Acceso a las carpetas
from werkzeug.utils import secure_filename 

app = Flask(__name__)  # Creando la app

mysql = MySQL()
# app.config['MYSQL_DATABASE_HOST']='http://127.0.0.1/' #Creamos la refencia al localhost
app.config['MYSQL_DATABASE_HOST'] = 'localhost'  # Creamos la refencia al localhost
app.config['MYSQL_DATABASE_USER'] = 'root'  # El user que viene por defecto
app.config['MYSQL_DATABASE_PASSWORD'] = '123456'  # Se puede omitir si no hay contraseña definida
app.config['MYSQL_DATABASE_DB'] = 'sistemadocentes'  # nombre de la DB
mysql.init_app(app)  # Creamos la conexion con la DB

CARPETA = os.path.join('uploads')  # Referencia a la carpeta
app.config['CARPETA'] = CARPETA  # Indicamos que vamos a guardar esta ruta de la carpeta

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)

@app.route('/')  # Hacemos el ruteo para que el user entre en la raiz
def index():
    sql = "SELECT * FROM `sistemadocentes`.`docentes`;"
    conn = mysql.connect()  # Se conecta a la conexión mysql.init_app(app)
    cursor = conn.cursor()  # Almacenaremos lo que ejecutamos
    cursor.execute(sql)  # Ejecutamos la sentencia SQL

    docentes = cursor.fetchall()  # Traemos toda la información
    print(docentes)  # Imprimimos los datos en la terminal

    conn.commit()  # Cerramos la conexión

    return render_template('docentes/index.html', docentes=docentes)  # Identifica la carpeta y el archivo html

@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT foto FROM `sistemadocentes`.`docentes` WHERE id=%s", id)
    fila = cursor.fetchone()

    if fila:
        nombre_foto = fila[0]
        if nombre_foto != 'default_foto.jpg':
            try:
                os.remove(os.path.join(app.config['CARPETA'], nombre_foto))
            except FileNotFoundError:
                pass  # Opcionalmente puedes manejar el caso de archivo no encontrado aquí

        cursor.execute("DELETE FROM `sistemadocentes`.`docentes` WHERE id=%s", (id,))
        conn.commit()

    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    # sql = "SELECT * FROM `sistemaempleados`.`empleados` WHERE id=%s;"
    conn = mysql.connect()  # Se conecta a la conexion de mysql.init_app(app)
    cursor = conn.cursor()  # almacenamos lo que ejecutamos
    cursor.execute("SELECT * FROM `sistemadocentes`.`docentes` WHERE id=%s;", (id,))  # Ejecutamos la sentencia SQL
    docentes = cursor.fetchall()
    conn.commit()  # Cerramos la conexion
    print(docentes)
    return render_template('docentes/edit.html', docentes=docentes)

@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _dni = request.form['txtDni']
    _correo = request.form['txtCorreo']
    _materia= request.form['txtMateria']
    _foto = request.files['txtFoto']
    id = request.form['txtID']
    print(_nombre)
    sql = "UPDATE `sistemadocentes`.`docentes` SET `nombre`=%s, `apellido`=%s,`dni`=%s,`correo`=%s, `materia`=%s WHERE id=%s;"
    datos = (_nombre,_apellido,_dni, _correo, _materia, id)

    conn = mysql.connect()  # Se conecta a la conexión mysql.init_app(app)
    cursor = conn.cursor()  # Almacenaremos lo que ejecutamos

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")  # Años horas minutos y segundos

    if _foto.filename != '':
        nuevoNombreFoto = tiempo + _foto.filename  # Concatena el nombre
        _foto.save("uploads/" + nuevoNombreFoto)  # Lo guarda en la carpeta

        cursor.execute("SELECT foto FROM `sistemadocentes`.`docentes` WHERE id=%s", id)  # Buscamos la foto
        fila = cursor.fetchall()  # Traemos toda la información

        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))  # Ese valor seleccionado se encuentra en la posición 0 y la fila 0
        cursor.execute("UPDATE `sistemadocentes`.`docentes` SET foto=%s WHERE id=%s", (nuevoNombreFoto, id))  # Buscamos la foto

    cursor.execute(sql, datos)
    conn.commit()  # Cerramos la conexión

    return redirect('/')

@app.route('/create')
def create():
    return render_template('docentes/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")  # Año, horas, minutos y segundos
    
    # Inicializamos nuevoNombreFoto con un valor predeterminado
    nuevoNombreFoto = 'default_foto.jpg'  # Puedes elegir un nombre por defecto o dejarlo vacío según tu necesidad
    
    if _foto.filename != '':
        nuevoNombreFoto = tiempo + '_' + secure_filename(_foto.filename)
        _foto.save(os.path.join(app.config['CARPETA'], nuevoNombreFoto))
    
    sql = "INSERT INTO `sistemadocentes`.`docentes` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    datos = (_nombre, _correo, nuevoNombreFoto)
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    
    return redirect('/')

# Línea requerida para que se pueda empezar a ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)  # Corremos la app en modo debug