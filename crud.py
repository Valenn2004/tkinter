import tkinter as tk
from tkinter import messagebox


class CRUD:

    def __init__(self, root, entidad, base_datos):

        self.root = root
        self.entidad = entidad
        self.base_datos = base_datos

        self.entradas = {}
        self.id_seleccionado = None

        # Aca va el ttulo

        titulo = tk.Label(
            root,
            text=f"CRUD de {entidad.__name__}",
            font=("Arial", 18, "bold")
        )

        titulo.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=15
        )

        # -Campos

        for i, campo in enumerate(entidad.campos, start=1):

            nombre = entidad.nombres_campos[campo]

            etiqueta = tk.Label(
                root,
                text=nombre
            )

            etiqueta.grid(
                row=i,
                column=0,
                padx=10,
                pady=5,
                sticky="e"
            )

            entrada = tk.Entry(root)

            entrada.grid(
                row=i,
                column=1,
                padx=10,
                pady=5
            )

            # Guardo el entry
            self.entradas[campo] = entrada

        # Aca los botones

        fila_botones = len(entidad.campos) + 1

        boton_agregar = tk.Button(
            root,
            text="Agregar",
            width=12,
            command=self.agregar
        )

        boton_agregar.grid(
            row=fila_botones,
            column=0,
            padx=5,
            pady=10
        )

        boton_modificar = tk.Button(
            root,
            text="Modificar",
            width=12,
            command=self.modificar
        )

        boton_modificar.grid(
            row=fila_botones,
            column=1,
            padx=5,
            pady=10
        )

        boton_eliminar = tk.Button(
            root,
            text="Eliminar",
            width=12,
            command=self.eliminar
        )

        boton_eliminar.grid(
            row=fila_botones + 1,
            column=0,
            padx=5,
            pady=5
        )

        boton_limpiar = tk.Button(
            root,
            text="Limpiar",
            width=12,
            command=self.limpiar
        )

        boton_limpiar.grid(
            row=fila_botones + 1,
            column=1,
            padx=5,
            pady=5
        )

        boton_mostrar = tk.Button(
            root,
            text="Mostrar registros",
            width=20,
            command=self.mostrar
        )

        boton_mostrar.grid(
            row=fila_botones + 2,
            column=0,
            columnspan=2,
            pady=10
        )

    # Aca obtengo los datos

    def obtener_datos(self):

        datos = []

        for campo in self.entidad.campos:

            valor = self.entradas[campo].get()

            datos.append(valor)

        return datos

    # Aca esta "agregar"

    def agregar(self):

        datos = self.obtener_datos()

        # Verificar que no haya campos vacíos
        if any(valor == "" for valor in datos):

            messagebox.showwarning(
                "Advertencia",
                "Todos los campos son obligatorios."
            )

            return

        self.base_datos.insertar(
            self.entidad.tabla,
            self.entidad.campos,
            datos
        )

        messagebox.showinfo(
            "Éxito",
            "Registro agregado correctamente."
        )

        self.limpiar()

    # Aca muestro

    def mostrar(self):

        datos = self.base_datos.consultar(
            self.entidad.tabla
        )

        # Nueva ventana
        ventana = tk.Toplevel(self.root)

        ventana.title(
            f"Registros - {self.entidad.__name__}"
        )

        ventana.geometry("600x400")

        # Encabezados
        encabezados = ["ID"]

        for campo in self.entidad.campos:

            encabezados.append(
                self.entidad.nombres_campos[campo]
            )

        # Mostrar encabezados
        for columna, encabezado in enumerate(encabezados):

            tk.Label(
                ventana,
                text=encabezado,
                font=("Arial", 10, "bold"),
                borderwidth=1,
                relief="solid",
                padx=10,
                pady=5
            ).grid(
                row=0,
                column=columna,
                sticky="nsew"
            )

        # Mostrar registros
        for fila, registro in enumerate(datos, start=1):

            for columna, valor in enumerate(registro):

                etiqueta = tk.Label(
                    ventana,
                    text=valor,
                    borderwidth=1,
                    relief="solid",
                    padx=10,
                    pady=5
                )

                etiqueta.grid(
                    row=fila,
                    column=columna,
                    sticky="nsew"
                )

                # Permitir seleccionar el registro
                etiqueta.bind(
                    "<Button-1>",
                    lambda evento, registro=registro:
                    self.seleccionar(registro)
                )

    # Seleccion de un registro

    def seleccionar(self, registro):

        # El primer elemento es el ID
        self.id_seleccionado = registro[0]

        # Cargamos los datos en los Entry
        for i, campo in enumerate(self.entidad.campos):

            self.entradas[campo].delete(
                0,
                tk.END
            )

            self.entradas[campo].insert(
                0,
                registro[i + 1]
            )

        messagebox.showinfo(
            "Registro seleccionado",
            f"ID seleccionado: {self.id_seleccionado}"
        )

    # Aca se modifica

    def modificar(self):

        if self.id_seleccionado is None:

            messagebox.showwarning(
                "Advertencia",
                "Primero seleccioná un registro."
            )

            return

        datos = self.obtener_datos()

        if any(valor == "" for valor in datos):

            messagebox.showwarning(
                "Advertencia",
                "Todos los campos son obligatorios."
            )

            return

        self.base_datos.modificar(
            self.entidad.tabla,
            self.entidad.campos,
            datos,
            self.id_seleccionado
        )

        messagebox.showinfo(
            "Éxito",
            "Registro modificado correctamente."
        )

        self.limpiar()

    # aca se elimina

    def eliminar(self):

        if self.id_seleccionado is None:

            messagebox.showwarning(
                "Advertencia",
                "Primero seleccioná un registro."
            )

            return

        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Seguro que querés eliminar este registro?"
        )

        if confirmar:

            self.base_datos.eliminar(
                self.entidad.tabla,
                self.id_seleccionado
            )

            messagebox.showinfo(
                "Éxito",
                "Registro eliminado correctamente."
            )

            self.limpiar()

    # aca se limpian los campos

    def limpiar(self):

        for entrada in self.entradas.values():

            entrada.delete(
                0,
                tk.END
            )

        self.id_seleccionado = None