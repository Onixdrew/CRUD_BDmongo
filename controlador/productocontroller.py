from app import app, productos,categorias,usuarios
from flask import render_template,request,jsonify,redirect
import yagmail
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
    # password2='eadtgrufikokctph'
    estado = False
    mensaje2 = ''
    emailLogin = request.form["correo"]
    password = request.form["contraseña"]
    user=usuarios.find()
    Productos=productos.find()

    try:
        for u in user:
            converContraseña= str(u['contraseña'])
            if u['correo'] == emailLogin and converContraseña == password:
                # Se intenta probar con con un correo y contarseña real, además se agregan a la coleccion
                # usuarios de la base de datos en mongo atlas para ponder acceder a la aplicacion, porque
                # las en nuevas actualizaciones de google no aparece la opcion de crear contraseña de aplicacion mencionada
                # en las guia de apoyo. 
                estado = True
                mensaje2 = f'Bienvenid@ {u["nombre"]}'
                email=yagmail.SMTP(emailLogin, password, encoding='UTF-8')
                asunto='Reporte ingreso al sistema'
                mensaje=f'Me permito informar que el usuario <b>{u['nombre']}</b> ha ingresado al sistema'
                email.send(to=emailLogin, subject=asunto, contents=mensaje)
                break  
    
        if estado:
            
            return render_template('listarProductos.html', mensaje2=mensaje2, Productos=Productos)
        else:
            mensaje2 = 'Correo o contraseña incorrectos'
            
    except PyMongoError as error:
        mensaje2=error
        
    return render_template('login.html', mensaje2=mensaje2)
        
        


# /////////////////////////////////////////////////////////

@app.route("/vistaAgregarProducto")
def vistaAgregarProducto():
    listaCategorias=categorias.find()
    return render_template("fmAgregarProductos.html", categorias=listaCategorias,)
    



# /////////////////////////////////////////////////////////

@app.route("/agregarProducto", methods=["POST"])
def agregarProducto():
    mensaje=None
    estado=False
    listaCategorias=categorias.find()
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
        Productos=productos.find()
        if (resultado.acknowledged):
            idProducto= ObjectId(resultado.inserted_id)
            nombreFoto=f"{idProducto}.jpg"
            # esto guarda la foto en el disco
            foto.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreFoto))
            estado=True
            mensaje='Producto agregado correctamentre.'
        else:
            mensaje='problemas al agregar el producto'
        
        return render_template('listarProductos.html',estado=estado, mensaje= mensaje, Productos=Productos, categorias=listaCategorias)
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
    
#     else:
#         mensaje='problemas al agregar el producto'
    
