from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymongo
import pymongo.errors
from bson.objectid import ObjectId

# Configuracion de la conexion a MongoDB
MONGO_HOST = "localhost"
MONGO_PORT = "27017"
MONGO_TIME_OFF = 1000

MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"
MONGO_BASE_DATOS = "escuela"
MONGO_COLLECTION = "alumnos"

# CONEXION A BD ESCUELA
cliente = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIME_OFF)
baseDatos = cliente[MONGO_BASE_DATOS]
coleccion = baseDatos[MONGO_COLLECTION]
ID_ALUMNO = " "

# funcion para mostrar datos en la tabla
def mostrarDatos(nombre="", sexo="", calificacion=""):
    objetoBuscar = {}
    if nombre:
        objetoBuscar["nombre"] = nombre
    if sexo:
        objetoBuscar["sexo"] = sexo
    if calificacion:
        objetoBuscar["calificacion"] = calificacion
    
    try:
        registros = table.get_children()
        for registro in registros:
            table.delete(registro)
        for documento in coleccion.find(objetoBuscar):
            table.insert('', 'end', text=str(documento["_id"]),values=documento["nombre"])
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        messagebox.showerror(message="Tiempo excedido: " + str(errorTiempo))
    except pymongo.errors.ConnectionFailure as errorConexion:
        messagebox.showerror(message="Fallo al conectarse a MongoDB: " + str(errorConexion))

# funcion para crear un registro
def crearRegistro():
    if nombre.get() and sexo.get() and calificacion.get():
        try:
            documento = {"nombre": nombre.get(), "sexo": sexo.get(), "calificacion": calificacion.get()}
            coleccion.insert_one(documento)
            nombre.delete(0, END)
            sexo.delete(0, END)
            calificacion.delete(0, END)
            mostrarDatos()
        except pymongo.errors.ConnectionFailure as error:
            messagebox.showerror(message="Fallo al conectarse a MongoDB: " + str(error))
    else:
        messagebox.showerror(message="Los campos no estan completos")

# funcion para seleccionar un registro
def dobleClickTabla(event):
    global ID_ALUMNO
    ID_ALUMNO = str(table.item(table.selection())["text"])
    documento = coleccion.find_one({"_id": ObjectId(ID_ALUMNO)})
    nombre.delete(0, END)
    nombre.insert(0, documento["nombre"])
    sexo.delete(0, END)
    sexo.insert(0, documento["sexo"])
    calificacion.delete(0, END)
    calificacion.insert(0, documento["calificacion"])
    crear["state"] = "disabled"
    editar["state"] = "normal"
    borrar["state"] = "normal"

# funcion para actualizar un registro
def editarRegistro():
    global ID_ALUMNO
    if nombre.get() and sexo.get() and calificacion.get():
        try:
            coleccion.update_one({"_id": ObjectId(ID_ALUMNO)}, {"$set":{
                "nombre": nombre.get(),
                "sexo": sexo.get(),
                "calificacion": calificacion.get(),
            }})
            nombre.delete(0, END)
            sexo.delete(0, END)
            calificacion.delete(0, END)
            mostrarDatos()
            crear["state"] = "normal"
            editar["state"] = "disabled"
            borrar["state"] = "disabled"
            ID_ALUMNO = " "
        except pymongo.errors.ConnectionFailure as error:
            messagebox.showerror(message="Fallo al conectarse a MongoDB: " + str(error))
    else:
        messagebox.showerror(message="Los campos no estan completos")

# funcion para eliminar un registro
def borrarRegistro():
    global ID_ALUMNO
    try: 
        coleccion.delete_one({"_id": ObjectId(ID_ALUMNO)})
        nombre.delete(0, END)
        sexo.delete(0, END)
        calificacion.delete(0, END)
        mostrarDatos()
        crear["state"] = "normal"
        editar["state"] = "disabled"
        borrar["state"] = "disabled"
        ID_ALUMNO = ""
    except pymongo.errors.ConnectionFailure as error:
        messagebox.showerror(message="Fallo al conectarse a MongoDB: " + str(error))

# funcion para buscar un registro
def buscarRegistro():
    mostrarDatos(buscarnombre.get(), buscarsexo.get(), buscarcalificacion.get())

# Configuracion de la ventana principal
ventana=Tk()
ventana.title("Gestión de Alumnos")

# Configuracion de la tabla
table=ttk.Treeview(ventana, columns=("nombre"))
table.grid(row=1, column=0, columnspan=2)
table.heading("#0",text="ID")
table.heading("#1",text="NOMBRE")
table.bind("<Double-Button-1>", dobleClickTabla)

# Campos de entrada
Label(ventana, text="Nombre").grid(row=2, column=0)
nombre = Entry(ventana)
nombre.grid(row=2, column=1, sticky=W+E)
nombre.focus()

Label(ventana,text="Sexo").grid(row=3, column=0)
sexo = Entry(ventana)
sexo.grid(row=3, column=1, sticky=W+E)

Label(ventana,text="Calificacion").grid(row=4, column=0)
calificacion = Entry(ventana)
calificacion.grid(row=4, column=1, sticky=W+E)

# Campos de búsqueda
Label(ventana, text="Buscar por nombre").grid(row=8, column=0)
buscarnombre = Entry(ventana)
buscarnombre.grid(row=8, column=1, sticky=W+E)

Label(ventana,text="Buscar por sexo").grid(row=9, column=0)
buscarsexo = Entry(ventana)
buscarsexo.grid(row=9, column=1, sticky=W+E)

Label(ventana,text="Buscar por Calificacion").grid(row=10, column=0)
buscarcalificacion = Entry(ventana)
buscarcalificacion.grid(row=10, column=1, sticky=W+E)

# Botones de acciones
crear = Button(ventana, text="Crear alumno", command=crearRegistro, bg="green", fg="white")
crear.grid(row=5,columnspan=2, sticky=W+E)

editar = Button(ventana, text="Editar alumno", command=editarRegistro, bg="yellow")
editar.grid(row=6,columnspan=2, sticky=W+E)
editar["state"]="disabled"

borrar = Button(ventana, text="Eliminar alumno", command=borrarRegistro, bg="red")
borrar.grid(row=7,columnspan=2, sticky=W+E)
borrar["state"]="disabled"

buscar = Button(ventana, text="Buscar alumnos", command=buscarRegistro, bg="blue")
buscar.grid(row=11,columnspan=2, sticky=W+E)

# Mostrar datos al inicio
mostrarDatos()

# Ejecutar la ventana principal
ventana.mainloop()