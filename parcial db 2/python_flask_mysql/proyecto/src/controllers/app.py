from flask import Flask, render_template, redirect, url_for, request, jsonify
import sys
import os

# Add the parent directory to the system path to import the models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import Models.database as db

app = Flask(__name__, template_folder='../View/templates', static_folder='../View/static')

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/registrado', methods=['POST'])
def registrado():
    if request.method == 'POST':
        # Obtener datos del formulario de registro
        nombre = request.form['nombre']
        correo = request.form['correo']
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']

        conn = db.database
        cursor = conn.cursor()

        try:
            # Insertar usuario en la base de datos
            cursor.execute("INSERT INTO usuario (nom, cro, usu, cnt) VALUES (%s, %s, %s, %s)", (nombre, correo, usuario, contrasena))
            conn.commit()
            cursor.close()

        except Exception as e:
            # Manejar errores, por ejemplo, redirigir a una página de error
            print(f"Error al insertar usuario en la base de datos: {e}")
            return redirect(url_for('error'))

    # Si se accede a esta ruta de manera directa sin enviar datos, redireccionar a la página principal
    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        # Obtener datos del formulario de login
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        conn = db.database
        cursor = conn.cursor()

        # Verificar si el usuario y contraseña coinciden con los almacenados en la base de datos
        cursor.execute("SELECT * FROM usuario WHERE cro = %s AND cnt = %s", (correo, contrasena))
        user = cursor.fetchone()

        if user:
            # Si las credenciales son válidas, redireccionar a la página de registro
            return redirect(url_for('iniciado'))
        else:
            # Si las credenciales son inválidas, redireccionar a la página principal
            return redirect(url_for('home'))
        
        cursor.close()
    else:
        # Si se accede a esta ruta de manera directa sin enviar datos, redireccionar a la página principal
        return redirect(url_for('home'))

@app.route('/iniciado')
def iniciado():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    return redirect(url_for('register_page'))

@app.route('/register_page')
def register_page():
    return render_template('register.html')

@app.route('/consultas', methods=['POST'])
def consultas():
    return redirect(url_for('consultas_page'))

@app.route('/consultas_page')
def consultas_page():
    conn = db.database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Proveedores")
    proveedores = cursor.fetchall()
    cursor.execute("SELECT * FROM Articulos")
    articulos = cursor.fetchall()
    cursor.close()
    return render_template('consultas.html', proveedores=proveedores, articulos=articulos)


@app.route('/registerPROV', methods=['POST'])
def registerPROV():
    return redirect(url_for('registerProv_page'))

@app.route('/registerProv_page')
def registerProv_page():
    return render_template('registerProv.html')

@app.route('/registrarArticulo', methods=['POST'])
def registrarArticulo():
    return redirect(url_for('registerArt_page'))

@app.route('/registerArt_page')
def registerArt_page():
    return render_template('articulos.html')

@app.route('/houme', methods=['POST'])
def houme():
    return redirect(url_for('home'))

@app.route('/obtenerProveedores')
def obtenerProveedores():
    conn = db.database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Proveedores")
    proveedores = cursor.fetchall()
    cursor.close()
    proveedores_dict = [{'idprov': p[0], 'nomprov': p[1]} for p in proveedores]
    return jsonify(proveedores_dict)

@app.route('/registrarDatosProv', methods=['POST'])
def registrarDatosProv():
    nomprov = request.form['nomprov']
    telefonos = request.form.getlist('telprov[]')

    conn = db.database
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO Proveedores (nomprov) VALUES (%s)", (nomprov,))
        idprov = cursor.lastrowid

        for telefono in telefonos:
            cursor.execute("INSERT INTO Proveedores_Telefonos (idprov, telprov) VALUES (%s, %s)", (idprov, telefono))

        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()

    return redirect(url_for('registerProv_page'))


@app.route('/registrarDatosArticulo', methods=['POST'])
def registrarDatosArticulo():
    # Obtener los datos del formulario
    nomarticulo = request.form['nomart']
    precio = request.form['precio']
    proveedores = request.form.getlist('proveedor[]')

    conn = db.database
    cursor = conn.cursor()

    try:
        # Insertar el artículo en la tabla de Articulos
        cursor.execute("INSERT INTO Articulos (nomart) VALUES (%s)", (nomarticulo,))
        codarticulo = cursor.lastrowid

        # Insertar los proveedores asociados al artículo en Articulos_Proveedores
        for proveedor_id in proveedores:
            cursor.execute("INSERT INTO Articulos_Proveedores (codart, idprov, precio) VALUES (%s, %s, %s)", (codarticulo, proveedor_id, precio))

        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()

    # Redirigir a la página de registro de artículo
    return redirect(url_for('registerArt_page'))



if __name__ == '__main__':
    app.run(debug=True)
