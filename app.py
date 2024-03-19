from flask import Flask
import pymongo


# crear aplicacio
app =Flask(__name__)

app.config["UPLOAD_FOLDER"]="./static/imagenes"


# crear conexion
miConexion=pymongo.MongoClient('mongodb+srv://Andrew:6yRZzkGdCsFPGPs0@cluster0.qj0gkdd.mongodb.net/')

# creo la bese de datos y la coleccion productos
baseDatos=miConexion['GestionProductos']
productos=baseDatos['productos']
categorias=baseDatos['categorias']
usuarios=baseDatos['usuarios']



# importo la carpeta llamada controlador y al archivo que contiene
from controlador.productocontroller import *

# arranco la aplicacion
if __name__=='__main__':
    app.run(port=3000, debug=True)