from flask import Flask, render_template, redirect, url_for, request, jsonify
import sys
import os

# Add the parent directory to the system path to import the models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import Models.database as db

app = Flask(__name__, template_folder='../View')


@app.route('/')
def home():
    return render_template('index.html')

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
    return render_template('consultas.html')

@app.route('/registerPROV', methods=['POST'])
def registerPROV():
    return redirect(url_for('registerProv_page'))

@app.route('/registerProv_page')
def registerProv_page():
    return render_template('registerProv.html')

@app.route('/registrarArticulo', methods=['POST'])
def registrarArticulo():
    return redirect(url_for('registerArt_page'))

#####
@app.route('/consulta_a_resultado')
def consulta_a_resultado():
    conn = db.database
    cursor = conn.cursor()
    cursor.execute("SELECT Proveedores.nomprov FROM Proveedores JOIN Articulos_Proveedores ON Proveedores.idprov = Articulos_Proveedores.idprov WHERE Articulos_Proveedores.codart = 1;")
    nombres_proveedores = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return jsonify(nombres_proveedores)

@app.route('/consulta_b_resultado')
def consulta_b_resultado():
    conn = db.database
    cursor = conn.cursor()
    cursor.execute("SELECT Articulos.nomart FROM Articulos JOIN Articulos_Proveedores ON Articulos.codart = Articulos_Proveedores.codart WHERE Articulos_Proveedores.idprov = 10;")
    nombres_articulos = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return jsonify(nombres_articulos)

@app.route('/consulta_c_resultado')
def consulta_c_resultado():
    conn = db.database
    cursor = conn.cursor()
    cursor.execute("SELECT idprov, nomprov FROM Proveedores;")
    proveedores = [{'idprov': row[0], 'nomprov': row[1]} for row in cursor.fetchall()]
    cursor.close()
    return jsonify(proveedores)

@app.route('/consulta_d_resultado')
def consulta_d_resultado():
    conn = db.database
    cursor = conn.cursor()
    cursor.execute("SELECT Articulos.codart, Articulos.nomart, Proveedores.nomprov FROM Articulos JOIN Articulos_Proveedores ON Articulos.codart = Articulos_Proveedores.codart JOIN Proveedores ON Articulos_Proveedores.idprov = Proveedores.idprov;")
    articulos_proveedores = [{'codart': row[0], 'nomart': row[1], 'nomprov': row[2]} for row in cursor.fetchall()]
    cursor.close()
    return jsonify(articulos_proveedores)


####

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



@app.route('/registerArt_page')
def registerArt_page():
    return render_template('articulos.html')

@app.route('/houme', methods=['POST'])
def houme():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
