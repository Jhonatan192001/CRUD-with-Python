from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pyodbc

# Configuración de la conexión
SQL_SERVER = "nombre de servidor"
SQL_DATABASE = "nombre de la base de datos "
SQL_USERNAME = "usuario"
SQL_PASSWORD = "contraseña"

# Establecer la conexión
conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};UID={SQL_USERNAME};PWD={SQL_PASSWORD}"
)
cursor = conn.cursor()
ID_ALUMNO = " "

# función para mostrar datos en la tabla
def mostrarDatos(nombre="", sexo="", calificacion=""):
    query = "SELECT id, nombre FROM alumnos WHERE 1=1"
    params = []
    
    if nombre:
        query += " AND nombre LIKE ?"
        params.append(f"%{nombre}%")
    if sexo:
        query += " AND sexo LIKE ?"
        params.append(sexo)
    if calificacion:
        query += " AND calificacion LIKE ?"
        params.append(calificacion)
    
    try:
        registros = table.get_children()
        for registro in registros:
            table.delete(registro)

        cursor.execute(query, params)
        for row in cursor.fetchall():
            table.insert('', 'end', text=str(row[0]), values=row[1])
    except pyodbc.Error as e:
        messagebox.showerror(message="Error al conectarse a SQL Server: " + str(e))

# función para crear un registro
def crearRegistro():
    if nombre.get() and sexo.get() and calificacion.get():
        try:
            query = "INSERT INTO alumnos (nombre, sexo, calificacion) VALUES (?, ?, ?)"
            params = (nombre.get(), sexo.get(), calificacion.get())
            cursor.execute(query, params)
            conn.commit()
            nombre.delete(0, END)
            sexo.delete(0, END)
            calificacion.delete(0, END)
            mostrarDatos()
        except pyodbc.Error as e:
            messagebox.showerror(message="Error al conectarse a SQL Server: " + str(e))
    else:
        messagebox.showerror(message="Los campos no están completos")

# función para seleccionar un registro
def dobleClickTabla(event):
    global ID_ALUMNO
    ID_ALUMNO = str(table.item(table.selection())["text"])
    query = "SELECT nombre, sexo, calificacion FROM alumnos WHERE id = ?"
    
    cursor.execute(query, (ID_ALUMNO,))
    row = cursor.fetchone()
    
    if row: 
        nombre.delete(0, END)
        nombre.insert(0, row[0])
        sexo.delete(0, END)
        sexo.insert(0, row[1])
        calificacion.delete(0, END)
        calificacion.insert(0, row[2])
        crear["state"] = "disabled"
        editar["state"] = "normal"
        borrar["state"] = "normal"

# funcion para actualizar un registro
def editarRegistro():
    global ID_ALUMNO
    if nombre.get() and sexo.get() and calificacion.get():
        try:
            query = "UPDATE alumnos SET nombre = ?, sexo = ?, calificacion = ? WHERE id = ? "
            params = (nombre.get(), sexo.get(), calificacion.get(), ID_ALUMNO)
            cursor.execute(query, params)
            conn.commit()
            nombre.delete(0, END)
            sexo.delete(0, END)
            calificacion.delete(0, END)
            mostrarDatos()
            crear["state"] = "normal"
            editar["state"] = "disabled"
            borrar["state"] = "disabled"
            ID_ALUMNO = " "
        except pyodbc.Error as e:
            messagebox.showerror(message="Error al conectarse a SQL Server: " + str(e))
    else:
        messagebox.showerror(message="Los campos no están completos")

# función para eliminar un registro
def borrarRegistro():
    global ID_ALUMNO
    try: 
        query = "DELETE FROM alumnos WHERE id = ?"
        cursor.execute(query, (ID_ALUMNO),)
        conn.commit()
        nombre.delete(0, END)
        sexo.delete(0, END)
        calificacion.delete(0, END)
        mostrarDatos()
        crear["state"] = "normal"
        editar["state"] = "disabled"
        borrar["state"] = "disabled"
        ID_ALUMNO = ""
    except pyodbc.Error as e:
            messagebox.showerror(message="Error al conectarse a SQL Server: " + str(e))

# función para buscar un registro
def buscarRegistro():
    mostrarDatos(buscarnombre.get(), buscarsexo.get(), buscarcalificacion.get())

# Configuración de la ventana principal
ventana=Tk()
ventana.title("Gestión de Alumnos")

# Configuración de la tabla
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

Label(ventana,text="Calificación").grid(row=4, column=0)
calificacion = Entry(ventana)
calificacion.grid(row=4, column=1, sticky=W+E)

# Campos de búsqueda
Label(ventana, text="Buscar por nombre").grid(row=8, column=0)
buscarnombre = Entry(ventana)
buscarnombre.grid(row=8, column=1, sticky=W+E)

Label(ventana,text="Buscar por sexo").grid(row=9, column=0)
buscarsexo = Entry(ventana)
buscarsexo.grid(row=9, column=1, sticky=W+E)

Label(ventana,text="Buscar por Calificación").grid(row=10, column=0)
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