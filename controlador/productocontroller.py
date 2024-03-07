from app import app, productos,categorias
from flask import Flask,render_template,request,jsonify
import pymongo
import os
from bson.objectid import ObjectId
import base64
from io import BytesIO
 
 
# creo la ruta raiz
@app.route('/')
def inicio():
    listaProductos=productos.find()
    listaP=[]
    
    for p in listaProductos:
        categoria=categorias.find_one({'_id':p['categoria']})
        p['nombreCategoria']=categoria['nombre']
        listaP.append(p)
    
    return render_template("listarProductos.html", productos=listaP)


# /////////////////////////////////////////////////////////

@app.route("/vistaAgregarProducto")
def vistaAgregarProducto():
    listaCategorias=categorias.find()
    print(type(listaCategorias))
    return render_template("fmAgregarProductos.html", categorias=listaCategorias)
    



# /////////////////////////////////////////////////////////

@app.route("/agregarProducto", methods=["POST"])
def agregarProducto():
    mensaje=None
    estado=False
    try:
        codigo= int(request.form["idCodigo"])
        nombre=request.form['idNombre']
        precio=int(request.form['idPrecio'])
        idCategoria=ObjectId(request.form['idCategoria'])
        foto=
        
        producto={
            'codigo':codigo,
            'nombre':nombre,
            'precio':precio,
            'categoria':idCategoria
        }
        
        resultado= productos.insert_one(producto)
        if (resultado.acknowledged):
            idProducto= resultado.inserted_id
            nombreFoto=f"{idProducto}+.jpg"
            # esto guarda la foto en el disco
            foto.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreFoto))
            estado=True
            mensaje='Producto agregado correctamentre.'
        else:
            mensaje='problemas al agregar el producto'
    except pymongo.errors as error:
        mensaje= error
    
    return render_template('fmAgregarProductos.html',estado=estado, mensaje= mensaje)


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
    