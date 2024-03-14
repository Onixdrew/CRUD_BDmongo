from app import app, productos,categorias,usuarios
from flask import render_template,request,jsonify,redirect
import yagmail
import os
from bson.objectid import ObjectId
import base64
from io import BytesIO
from pymongo.errors import PyMongoError
import threading
 
 
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
    #contraseña de onix7kingdom@gmail.com
    # password='eadtgrufikokctph'
    estado = False
    mensaje = ''
    emailLogin = request.form["correo"]
    password = request.form["contraseña"]
    user=usuarios.find()
    Productos=productos.find()
    listCategorias=categorias.find()

    try:
        for u in user:
            converContraseña= str(u['contraseña'])
            if u['correo'] == emailLogin and converContraseña == password:
           
                estado = True
                mensaje = f'Bienvenid@ {u["nombre"]}'
             
                #////////// Enviar correo///////////////
             
                email=yagmail.SMTP(emailLogin, password, encoding='UTF-8')
                asunto='Reporte ingreso al sistema'
                mensaje=f'Me permito informar que el usuario <b>{u['nombre']}</b> ha ingresado al sistema'
                email.send(to='cesarmcuellar@gmail.com', subject=asunto, contents=mensaje)

                # ////////////// Enviar correo con thread para enviar en eparalelo/////////////
                
                # def enviarCorreo(email=None, destinatario=None, asunto=None, mensajeCorreo=None):
                #     email.send(to=emailLogin, subject=asunto, contents=mensaje)
                
                # la funcion thread permite realizar operaciones en paralelo, resive una funcion a realizar y los argumentos
                # thread=threading,thread(target=enviarCorreo, args=(email,emailLogin,asunto,mensajeCorreo))
                # thread.start()
             
                break  
    
        if estado:
            
            return render_template('listarProductos.html', mensaje=mensaje, Productos=Productos, listCategorias=listCategorias)
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
    listCategorias=categorias.find()
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
        
        return render_template('listarProductos.html',estado=estado, mensaje= mensaje, Productos=Productos, listCategorias=listCategorias)
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
    
