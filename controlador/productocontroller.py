from app import app, productos
from flask import Flask,render_template
 
 
# creo la ruta raiz
@app.route('/')
def inicio():
    return render_template("listarProductos.html")


