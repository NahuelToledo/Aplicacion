#Importaciones
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import tkinter as tk
import os
from PIL import Image
import bd.base_datos as sqlbd

# Configuraciones globales para la aplicacion


# ---> Rutas
# Carpeta Principal

carpeta_principal = os.path.dirname(__file__)
#/Python/AplicacionGrafica/interfaz

carpeta_imagenes = os.path.join(carpeta_principal,"imagenes")
#/Python/AplicacionGrafica/interfaz\imagenes

# Objeto para manejar bases de datos MySQL
base_datos = sqlbd.BaseDatos(**sqlbd.acceso_bd)


#Modo de color y tema
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Fuente para algunos widgets
fuente_widgets = ('Raleway', 16, tk.font.BOLD)

class Login:
    def __init__(self):
        # Creación de la ventana principal
        self.root = ctk.CTk()
        self.root.title("Programación Fácil - Proyecto de bases de datos")
        self.root.iconbitmap(os.path.join(carpeta_imagenes, "logo.ico"))
        self.root.geometry("400x500")
        self.root.resizable(False,False)

        # Contenido de la ventana principal
        # Logo
        logo = ctk.CTkImage(
            light_image= Image.open((os.path.join(carpeta_imagenes, "logo_claro.png"))),
            dark_image= Image.open((os.path.join(carpeta_imagenes, "logo_oscuro.png"))),
            size=(250, 250) # tamaño de imagenes
            )
        
        
        etiqueta = ctk.CTkLabel(master = self.root,
                                image=logo,
                                text="")
        etiqueta.pack(pady = 15)

        # Campos de texto
        # Usuario
        ctk.CTkLabel(self.root, text="Usuario").pack()
        self.usuario = ctk.CTkEntry(self.root)
        self.usuario.insert(0, "Ej:Laura")
        self.usuario.bind("<Button-1>", lambda e: self.usuario.delete(0, 'end'))
        self.usuario.pack()

        # Contraseña
        ctk.CTkLabel(self.root, text="Contraseña").pack()
        self.contrasena = ctk.CTkEntry(self.root)
        self.contrasena.insert(0, "*******")
        self.contrasena.bind("<Button-1>", lambda e: self.contrasena.delete(0, 'end'))
        self.contrasena.pack()

        # Botón de envío
        ctk.CTkButton(self.root, text="Entrar", command= self.validar).pack(pady = 10)

        # Bucle de ejecución
        self.root.mainloop()
    
        # Función para validar el login
    def validar(self):
        obtener_usuario = self.usuario.get() # Obtenemos el nombre de usuario
        obtener_contrasena = self.contrasena.get() # Obtenemos la contraseña
        
        # Verifica si el valor que tiene el usuario o la contraseña o ambos no coinciden
        if obtener_usuario != sqlbd.acceso_bd["user"] or obtener_contrasena != sqlbd.acceso_bd["password"]:
         # En caso de tener ya un elemento "info_login" (etiqueta) creado, lo borra
            if hasattr(self, "info_login"):
                self.info_login.configure(text="Usuario o contraseña incorrectos.")
            else:
                # Crea esta etiqueta siempre que el login sea incorrecto
                self.info_login = ctk.CTkLabel(self.root, text="Usuario o contraseña incorrectos.")
                self.info_login.pack()
        else:
            # En caso de tener ya un elemento "info_login" (etiqueta) creado, lo borra
            if hasattr(self, "info_login"):
                self.info_login.configure(text=f"Hola, {obtener_usuario}. Espere unos instantes...")
            else:
                # Crea esta etiqueta siempre que el login sea correcto
                self.info_login = ctk.CTkLabel(self.root, text=f"Hola, {obtener_usuario}. Espere unos instantes...")
                self.info_login.pack()
            # Se destruye la ventana de login
            self.root.destroy()
            # Se instancia la ventana de opciones del programa
            ventana_opciones = VentanaOpciones()


class FuncionesPrograma:
    def ventana_consultas(self):
        # Creación de la ventana secundaria
        ventana = ctk.CTkToplevel()
        
        # Título de la ventana
        ventana.title("Ventana de consultas SQL")
        
        # Pone el foco en la ventana
        ventana.grab_set()
        
        # Crea el frame y añádelo a la ventana
        marco = ctk.CTkFrame(ventana)
        marco.pack(padx=10, pady=10)
        
                # Crea el entry y establece su tamaño a 300px de ancho
        self.entrada = ctk.CTkEntry(marco, width=300)
        # Establece un valor personalizado de fuente
        self.entrada.configure(font=fuente_widgets)
        # Posiciona el elemento en grid
        self.entrada.grid(row=0,column=0, pady=10)
        
        # Método para utilizar la lógica del método consulta de base_datos.py
        def procesar_datos():
            try:
                # Borra el contenido de "texto"
                self.texto.delete('1.0', 'end')
                # obtiene el contenido del entry
                datos = self.entrada.get()
                # llama al método base_datos.consulta() con los datos como argumento
                resultado = base_datos.consulta(datos)
                for registro in resultado:
                    self.texto.insert('end', registro)
                    self.texto.insert('end', '\n')
                # Actualiza el contador de registros devueltos
                numero_registros = len(resultado)
                self.contador_registros.configure(text=f"Registros devueltos: {numero_registros}")
            except Exception:
                self.contador_registros.configure(text=f"Hay un error en tu consulta SQL. Por favor, revísela.")
                CTkMessagebox(title="Error", message="¡Hay un error en tu consulta SQL! Por favor, revísela.", icon="cancel")
            
            

        # Crea el botón de envío
        boton_envio = ctk.CTkButton(marco, 
                                text="Enviar",
                                command=lambda : procesar_datos())
        # Posiciona el botón a la derecha del Entry()
        boton_envio.grid(row=0, column=1)
        
        # Crea el botón de borrado
        boton_borrar = ctk.CTkButton(marco, 
                                 text="Borrar",
                                 command=self.limpiar_texto)
        # Posiciona el botón a la derecha del botón de envío
        boton_borrar.grid(row=0, column=2)
        
        # Crea el widget de texto
        self.texto = ctk.CTkTextbox(marco, 
                                    width=610, 
                                    height=300)

        # Coloca el widget texto debajo del entry y el botón usando grid
        self.texto.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
        # Agrega un nuevo widget Label para mostrar el número de registros devueltos
        self.contador_registros = ctk.CTkLabel(marco, text="Esperando una instruccion...")
        self.contador_registros.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
                
    def limpiar_texto(self):
    # borra todo el contenido del widget Text
        self.texto.delete('1.0', 'end')
        
        
    def ventana_mostrar_bases_datos(self):
        # Se crea la ventana
        ventana = ctk.CTkToplevel()
        # Se le da un título
        ventana.title("Ventana para mostrar las bases de datos del servidor.")
        # Se le da un tamaño
        ventana.geometry("400x565")
        # Se evita su redimensión
        ventana.resizable(0,0)
        # Pone el foco en la ventana
        ventana.grab_set()
        #Se crea un marco
        marco = ctk.CTkFrame(ventana)
        marco.pack(padx=10, pady=10)        
        
        # Se crea una etiqueta informativa para la ventana
        ctk.CTkLabel(marco, text="Listado de las bases de datos en el servidor",
                     font=fuente_widgets).pack(padx=10, pady=10)
        # Agregar un campo de entrada para la búsqueda
        self.busqueda_control = tk.StringVar()
        
        # Se crear la entrada de texto para búsquedas 
        ctk.CTkEntry(marco, 
                    font=fuente_widgets,
                    textvariable=self.busqueda_control,
                    width=300).pack(padx=10)        
        
        #Caja de resultados
        self.texto = ctk.CTkTextbox(marco,
                                    font=fuente_widgets,
                                    width=300,
                                    height=300)
        self.texto.pack(padx=10, pady=10)
        
        # Se crea una etiqueta para mostrar el número de resultados
        self.resultados_label = ctk.CTkLabel(marco,
                                            text="",
                                            font=fuente_widgets)
        self.resultados_label.pack(pady=10)
        
    
        # Función interna de actualización SHOW DATABASES
        def actualizar():
            # Se establece el valor de la variable de control a string vacío (reset)
            self.busqueda_control.set('')
            # Se elimina el contenido de la caja de resultados
            self.texto.delete('1.0', 'end')
            # Se realiza la llamada al método mostrar_bd (SHOW DATABASES) y se guarda en resultado
            resultado = base_datos.mostrar_bd()
            # Se itera el resultado y se presenta línea a línea en la caja de texto. 
            for bd in resultado:
                self.texto.insert('end', f"-{bd[0]}\n")
                
            # Se evalúa el resultado para deteminar la frase singular o plural
            numero_resultados = len(resultado)
            if numero_resultados == 1:
                self.resultados_label.configure(text=f"Se encontró {numero_resultados} resultado.")
            else:
                self.resultados_label.configure(text=f"Se encontraron {numero_resultados} resultados.")
        
        # Función interna de búsqueda        
        def buscar():
            # Se elimina el contenido de la caja de resultados
            self.texto.delete('1.0', 'end')
            # Se realiza la llamada al método mostrar_bd (SHOW DATABASES) y se guarda en resultado 
            resultado = base_datos.mostrar_bd()
            # Se obtiene el valor string de la variable de control (lo que se busca en el Entry())
            busqueda = self.busqueda_control.get().lower()
            
            # Se crea una lista vacía donde almacenar los resultados filtrados
            resultado_filtrado = []
            # Se itera la tupla fetchall.
            for bd in resultado:
                #Si lo que tiene la StringVar está en cada lista de la tupla, se añade a la lista
                if busqueda in bd[0]:
                    resultado_filtrado.append(bd)
            
            # Se itera la lista ya filtrada, con lo que se insertan los resultados en la caja de resultados
            for bd in resultado_filtrado:
                self.texto.insert('end', f"-{bd[0]}\n")
            
            # Se evalúa el resultado para deteminar la frase singular o plural
            numero_resultados = len(resultado_filtrado)
            if numero_resultados == 1:
                self.resultados_label.configure(text=f"Se encontró {numero_resultados} resultado.")
            else:
                self.resultados_label.configure(text=f"Se encontraron {numero_resultados} resultados.")
            
        # Se crea un botón para buscar bases de datos
        boton_buscar = ctk.CTkButton(marco,
                                    text="Buscar",
                                    command=buscar,
                                    )
        boton_buscar.pack(pady=10)
        
        # Se crea un botón para actualizar los resultados de la caja
        boton_actualizar = ctk.CTkButton(marco,
                                         text="Actualizar",
                                         command=actualizar,
                                         )
        boton_actualizar.pack(pady=10)
            
        actualizar()
        
    def ventana_eliminar_bases_datos(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para eliminar bases de datos")
        
    def ventana_crear_bases_datos(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para crear bases de datos")
        
    def ventana_crear_respaldos(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para crear respaldos")
        
    def ventana_crear_tablas(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para crear tablas")
    
    def ventana_eliminar_tablas(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para eliminar tablas")
        
    def ventana_mostrar_tablas(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para mostrar tablas")
        
    def ventana_mostrar_columnas(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para mostrar columnas de una tabla")
        
    def ventana_insertar_registros(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para insertar registros")
        
    def ventana_eliminar_registros(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para eliminar registros")
        
    def ventana_vaciar_tablas(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para vaciar tablas")
    
    def ventana_actualizar_tablas(self):
        ventana = ctk.CTkToplevel()
        ventana.title("Ventana para actualizar tablas")
        
objeto_funciones = FuncionesPrograma()

class VentanaOpciones:
    # Diccionario para los botones
    botones = {'Consulta SQL': objeto_funciones.ventana_consultas, 
               'Mostrar Bases de Datos': objeto_funciones.ventana_mostrar_bases_datos,
               'Eliminar Bases de Datos': objeto_funciones.ventana_eliminar_bases_datos,
               'Crear Bases de Datos': objeto_funciones.ventana_crear_bases_datos, 
               'Crear Respaldos': objeto_funciones.ventana_crear_respaldos,
               'Crear Tablas': objeto_funciones.ventana_crear_tablas,
               'Eliminar Tablas': objeto_funciones.ventana_eliminar_tablas,
               'Mostrar Tablas': objeto_funciones.ventana_mostrar_tablas,
               'Mostrar Columnas': objeto_funciones.ventana_mostrar_columnas,
               'Insertar Registros': objeto_funciones.ventana_insertar_registros,
               'Eliminar Registros': objeto_funciones.ventana_eliminar_registros,
               'Vaciar Tablas': objeto_funciones.ventana_vaciar_tablas,
               'Actualizar Registros': objeto_funciones.ventana_actualizar_tablas
               }
    def __init__(self):
        # Se crea la ventana de CustomTkinter
        self.root = ctk.CTk()
        # Se le da un título
        self.root.title("Opciones para trabajar con bases de datos.")
    
        # Marco para contener el menú superior
        menu_frame = ctk.CTkFrame(self.root)
        menu_frame.pack(side='top', fill='x')

        # Se crea el botón de Menú
        archivo = tk.Menubutton(menu_frame, 
                                text='Archivo', 
                                background='#2b2b2b', 
                                foreground='white', 
                                activeforeground='black', 
                                activebackground='gray52')
        
        # Se crea el botón de Menú
        edicion = tk.Menubutton(menu_frame, 
                                text='Edición', 
                                background='#2b2b2b', 
                                foreground='white', 
                                activeforeground='black', 
                                activebackground='gray52')
        
        # Se crea el menú
        menu_archivo = tk.Menu(archivo, tearoff=0)
        # Se crea el menú
        menu_edicion = tk.Menu(edicion, tearoff=0)

        # Añade una opción al menú desplegable
        menu_archivo.add_command(label='Imprimir Saludo', 
                                 command=lambda: print('Hello PC Master!'), 
                                 background='#2b2b2b', 
                                 foreground='white', 
                                 activeforeground='black', 
                                 activebackground='gray52')
        
        
        # Crea un nuevo menú para la cascada
        cascada = tk.Menubutton(menu_edicion, 
                                text='Cascada', 
                                background='black', 
                                foreground='white', 
                                activeforeground='black', 
                                activebackground='gray52')
        
        # Se crea el menú
        menu_cascada = tk.Menu(cascada, tearoff=0)
        cascada.config(menu=menu_cascada)
        
        # Se crea una cascada dentro del menu de edición
        menu_edicion.add_cascade(label="Opciones", menu=menu_cascada, 
                                 background='#2b2b2b', 
                                 foreground='white', 
                                 activeforeground='black', 
                                 activebackground='gray52')
    
        # Agrega opciones a la cascada
        menu_cascada.add_command(label="Opción 1", 
                                 command=lambda: print("Opción 1 seleccionada"), 
                                 background='#2b2b2b', 
                                 foreground='white', 
                                 activeforeground='black', 
                                 activebackground='gray52')
        
        menu_cascada.add_command(label="Opción 2", 
                                 command=lambda: print("Opción 2 seleccionada"), 
                                 background='#2b2b2b', 
                                 foreground='white', 
                                 activeforeground='black', 
                                 activebackground='gray52')
        
        menu_cascada.add_command(label="Opción 3", 
                                 command=lambda: print("Opción 3 seleccionada"), 
                                 background='#2b2b2b', 
                                 foreground='white', 
                                 activeforeground='black', 
                                 activebackground='gray52')
        
        # Asigna el menú desplegable al Menubutton
        archivo.config(menu=menu_archivo)
        # Posiciona el Menubutton dentro del Frame
        archivo.pack(side='left')
        
        # Asigna el menú desplegable al Menubutton
        edicion.config(menu=menu_edicion)
        # Posiciona el Menubutton dentro del Frame
        edicion.pack(side='left')
        
        # Asigna el menú desplegable al Menubutton
        cascada.config(menu=menu_cascada)
        
        # Crea un Frame para contener los botones de la ventana
        frame_botones = ctk.CTkFrame(self.root)
        # Posiciona el Frame debajo del menú
        frame_botones.pack(side='top', fill='x')

        # Contador para la posición de los botones
        contador = 0

        # Valor de elementos por fila
        elementos_fila = 3

        # Crea los botones y establece su texto
        for texto_boton in self.botones:
            boton = ctk.CTkButton(
                master=frame_botones, #Se le indica en que frame aparecer
                text=texto_boton,
                height=25,
                width=200,
                command=self.botones[texto_boton]
            )
            boton.grid(row=contador//elementos_fila, column=contador%elementos_fila, padx=5, pady=5)

            # Incrementa el contador
            contador += 1

        self.root.mainloop()