from app import app, productos,categorias,usuarios
from flask import Flask,render_template,request,jsonify
import pymongo
import os
from bson.objectid import ObjectId
import base64
from io import BytesIO
from pymongo.errors import PyMongoError

 
 
# creo la ruta raiz
@app.route('/')
def inicio():
    listaProductos=productos.find()
    listaP=[]
    print(listaP)
    
    for p in listaProductos:
        categoria=categorias.find_one({'_id':ObjectId(p['categoria'])})
        if p['categoria'] == categoria['_id']:
           p['categoria'] = categoria['nombre']
           listaP.append(p)
    
    return render_template("login.html", productos=listaP, MostrarProductos=listaProductos)

#///////////////////Login/////////////////////////

@app.route('/datosLogin', methods=["POST"])
def TablaProductos():
    estado = False
    mensaje2 = ''

    emailLogin = request.form["correo"]
    password = request.form["contraseña"]
    user=usuarios.find()
    

    for u in user:
        if u['correo'] == emailLogin and u['contraseña'] == password:
            estado = True
            mensaje2 = f'Bienvenido {u["nombre"]}'
            break  # Termina el bucle si encuentra coincidencia

    if estado:
        return render_template('listarProductos.html', mensaje2=mensaje2)
    else:
        mensaje2 = 'Correo o contraseña incorrectos'
        return render_template('login.html', mensaje2=mensaje2)
        
        


# /////////////////////////////////////////////////////////

@app.route("/vistaAgregarProducto")
def vistaAgregarProducto():
    listaCategorias=categorias.find()
    print(type(listaCategorias))
    return render_template("fmAgregarProductos.html", categorias=listaCategorias,)
    



# /////////////////////////////////////////////////////////

@app.route("/agregarProducto", methods=["POST"])
def agregarProducto():
    mensaje=None
    estado=False
    try:
        codigo =int(request.form["codigo"]) 
        nombre = request.form["nombre"]
        precio = int(request.form["precio"])
        idCategoria = request.form["categoria"]
        foto =request.files["fileFoto"]
        
        producto={
            'codigo':codigo,
            'nombre':nombre,
            'precio':precio,
            'categoria':ObjectId(idCategoria)
        }
        
        resultado= productos.insert_one(producto)
        if (resultado.acknowledged):
            idProducto= ObjectId(resultado.inserted_id)
            nombreFoto=f"{idProducto}.jpg"
            # esto guarda la foto en el disco
            foto.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreFoto))
            estado=True
            mensaje='Producto agregado correctamentre.'
        else:
            mensaje='problemas al agregar el producto'
        
        return render_template('listarProductos.html',estado=estado, mensaje= mensaje)
    except PyMongoError as error:
        mensaje= error
    
    


# /////////////////////////////////////////////////////////

# @app.route('/agregarProductoJson')
# def agregarProductoJson():
#     estado=False
#     mensaje=None
#     resultado= productos.insert_one(producto)
#     if (resultado.acknowledged):
#         rutaImagen=f"{os.path.join(app.config["UPLOAD_FOLDER"])}/{ producto['_id']}.jpg"   
#         estado=True
#         mensaje='Producto agregado correctamentre.'
#     else:
#         mensaje='problemas al agregar el producto'
    