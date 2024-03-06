from flask import Flask
import pymongo

# crear aplicacio
app =Flask(__name__)

app.config["UPLOAD_FOLDER"]="./static/imagenes"


# crear conexion
miConexion=pymongo.MongoClient('mongodb://localhost:27017')

# creo la bese de datos y la coleccion productos
baseDatos=miConexion['GestionProductos']
productos=baseDatos['productos']


# importo la carpeta llamada controlador y su archivo que esta en mi proyecto
from controlador.productocontroller import *

# arranco la aplicacion
if __name__=='__main__':
    app.run(port=5000, debug=True)