import tkinter as tk

from crud import CRUD
from vehiculo import Vehiculo
from propietario import Propietario
from base_datos import BaseDatos



#Aca creo la base de datos


base_datos = BaseDatos()



# Esta es la ventana principal


root = tk.Tk()

root.title("Sistema de Gestión")

root.geometry("400x300")



# Aca le pongo el titulo


titulo = tk.Label(
    root,
    text="Sistema de Gestión",
    font=("Arial", 20, "bold")
)

titulo.pack(pady=30)


# 
# Aca abro el crud de vehiculos
# 

def abrir_vehiculos():

    ventana = tk.Toplevel(root)

    ventana.title("Vehículos")

    ventana.geometry("400x350")

    CRUD(
        ventana,
        Vehiculo,
        base_datos
    )


# Abro el crud propietarios


def abrir_propietarios():

    ventana = tk.Toplevel(root)

    ventana.title("Propietarios")

    ventana.geometry("400x350")

    CRUD(
        ventana,
        Propietario,
        base_datos
    )


# Aca estan los botones

boton_vehiculos = tk.Button(
    root,
    text="Gestionar Vehículos",
    width=25,
    command=abrir_vehiculos
)

boton_vehiculos.pack(pady=10)


boton_propietarios = tk.Button(
    root,
    text="Gestionar Propietarios",
    width=25,
    command=abrir_propietarios
)

boton_propietarios.pack(pady=10)


# aca inicio el Tkinter

root.mainloop()