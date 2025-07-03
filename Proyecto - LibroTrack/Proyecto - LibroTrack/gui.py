import tkinter as tk
from tkinter import ttk, messagebox
from model import Biblioteca, Libro, Usuario
import datetime

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LibroTrack - Sistema de Gestión de Biblioteca")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        width = int(screen_width * 0.85)
        height = int(screen_height * 0.75)
        center_x = int((screen_width - width) / 2)
        center_y = int((screen_height - height) / 2)
        self.geometry(f'{width}x{height}+{center_x}+{center_y}')
        self.minsize(int(screen_width*0.7), int(screen_height*0.6))

        self.biblioteca = Biblioteca()
        self.libro_id_a_modificar = None
        self.usuario_id_a_modificar = None

        self.notebook_principal = ttk.Notebook(self, padding=5)
        self.notebook_principal.pack(expand=False, fill=tk.X, side=tk.TOP, padx=5, pady=(5,0))

        self.frame_agregar_libro_tab = ttk.Frame(self.notebook_principal, padding=10)
        self.frame_agregar_usuario_tab = ttk.Frame(self.notebook_principal, padding=10)
        self.frame_registrar_prestamo_tab = ttk.Frame(self.notebook_principal, padding=10)
        self.frame_registrar_devolucion_tab = ttk.Frame(self.notebook_principal, padding=10)

        self.notebook_principal.add(self.frame_agregar_libro_tab, text='Agregar Libro')
        self.notebook_principal.add(self.frame_agregar_usuario_tab, text='Agregar Usuario')
        self.notebook_principal.add(self.frame_registrar_prestamo_tab, text='Registrar Préstamo')
        self.notebook_principal.add(self.frame_registrar_devolucion_tab, text='Registrar Devolución')

        self.panel_visualizacion = ttk.Frame(self, padding="10")
        self.panel_visualizacion.pack(expand=True, fill=tk.BOTH, side=tk.TOP, padx=5, pady=5)

        self.panel_visualizacion.columnconfigure(0, weight=2)
        self.panel_visualizacion.columnconfigure(1, weight=1)
        self.panel_visualizacion.rowconfigure(0, weight=1)

        self._crear_widgets_pestana_agregar_libro()
        self._crear_widgets_pestana_agregar_usuario()
        self._crear_widgets_pestana_registrar_prestamo()
        self._crear_widgets_pestana_registrar_devolucion()

        self._crear_panel_libros()
        self._crear_panel_usuarios_prestamos()

        self._actualizar_todas_las_listas_y_combos()

    def _crear_widgets_pestana_agregar_libro(self):
        for widget in self.frame_agregar_libro_tab.winfo_children(): widget.destroy()
        form_frame = ttk.Frame(self.frame_agregar_libro_tab, padding="10")
        form_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        ttk.Label(form_frame, text="Título:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.tab_libro_titulo_entry = ttk.Entry(form_frame, width=50)
        self.tab_libro_titulo_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(form_frame, text="Autor:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.tab_libro_autor_entry = ttk.Entry(form_frame, width=50)
        self.tab_libro_autor_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(form_frame, text="Género:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.tab_libro_genero_entry = ttk.Entry(form_frame, width=50)
        self.tab_libro_genero_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        form_frame.columnconfigure(1, weight=1)
        botones_frame = ttk.Frame(self.frame_agregar_libro_tab, padding="5")
        botones_frame.pack(pady=10)
        self.btn_tab_guardar_libro = ttk.Button(botones_frame, text="Guardar Libro", command=self._accion_guardar_libro_desde_tab, width=20)
        self.btn_tab_guardar_libro.pack(side=tk.LEFT, padx=10)
        self.btn_tab_limpiar_form_libro = ttk.Button(botones_frame, text="Limpiar Formulario", command=self._accion_limpiar_form_libro_tab, width=20)
        self.btn_tab_limpiar_form_libro.pack(side=tk.LEFT, padx=10)

    def _crear_widgets_pestana_agregar_usuario(self):
        for widget in self.frame_agregar_usuario_tab.winfo_children(): widget.destroy()
        form_frame = ttk.Frame(self.frame_agregar_usuario_tab, padding="10")
        form_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        ttk.Label(form_frame, text="C.I.:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.tab_usuario_ci_entry = ttk.Entry(form_frame, width=50)
        self.tab_usuario_ci_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(form_frame, text="Nombre:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.tab_usuario_nombre_entry = ttk.Entry(form_frame, width=50)
        self.tab_usuario_nombre_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(form_frame, text="Teléfono:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.tab_usuario_telefono_entry = ttk.Entry(form_frame, width=50)
        self.tab_usuario_telefono_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        form_frame.columnconfigure(1, weight=1)
        botones_frame = ttk.Frame(self.frame_agregar_usuario_tab, padding="5")
        botones_frame.pack(pady=10)
        self.btn_tab_guardar_usuario = ttk.Button(botones_frame, text="Guardar Usuario", command=self._accion_guardar_usuario_desde_tab, width=20)
        self.btn_tab_guardar_usuario.pack(side=tk.LEFT, padx=10)
        self.btn_tab_limpiar_form_usuario = ttk.Button(botones_frame, text="Limpiar Formulario", command=self._accion_limpiar_form_usuario_tab, width=20)
        self.btn_tab_limpiar_form_usuario.pack(side=tk.LEFT, padx=10)

    def _crear_widgets_pestana_registrar_prestamo(self):
        for widget in self.frame_registrar_prestamo_tab.winfo_children(): widget.destroy()
        form_frame = ttk.Frame(self.frame_registrar_prestamo_tab, padding="10")
        form_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        ttk.Label(form_frame, text="Libro (Disponibles):").grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.prestamo_tab_libro_combobox = ttk.Combobox(form_frame, width=48)
        self.prestamo_tab_libro_combobox.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        ttk.Label(form_frame, text="Usuario:").grid(row=1, column=0, padx=5, pady=10, sticky="w")
        self.prestamo_tab_usuario_combobox = ttk.Combobox(form_frame, width=48) 
        self.prestamo_tab_usuario_combobox.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

        form_frame.columnconfigure(1, weight=1)
        botones_frame = ttk.Frame(self.frame_registrar_prestamo_tab, padding="5")
        botones_frame.pack(pady=20)
        btn_confirmar_prestamo = ttk.Button(botones_frame, text="Confirmar Préstamo", command=self._accion_confirmar_prestamo_tab, width=25)
        btn_confirmar_prestamo.pack()

    def _crear_widgets_pestana_registrar_devolucion(self):
        for widget in self.frame_registrar_devolucion_tab.winfo_children(): widget.destroy()
        form_frame = ttk.Frame(self.frame_registrar_devolucion_tab, padding="10")
        form_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        ttk.Label(form_frame, text="Libro a Devolver (Prestados):").grid(row=0, column=0, padx=5, pady=10, sticky="w")
        self.devolucion_tab_libro_combobox = ttk.Combobox(form_frame, width=60) 
        self.devolucion_tab_libro_combobox.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        form_frame.columnconfigure(1, weight=1)
        botones_frame = ttk.Frame(self.frame_registrar_devolucion_tab, padding="5")
        botones_frame.pack(pady=20)
        btn_confirmar_devolucion = ttk.Button(botones_frame, text="Confirmar Devolución", command=self._accion_confirmar_devolucion_tab, width=25)
        btn_confirmar_devolucion.pack()
        btn_refrescar_combo_devolucion = ttk.Button(botones_frame, text="Refrescar Lista Libros Prestados", command=self._poblar_combobox_libros_prestados_devolucion, width=25)
        btn_refrescar_combo_devolucion.pack(pady=5)

    def _crear_panel_libros(self):
        if not hasattr(self, 'panel_libros_frame') or not self.panel_libros_frame.winfo_exists():
            self.panel_libros_frame = ttk.LabelFrame(self.panel_visualizacion, text="Biblioteca de Libros", padding="10")
            self.panel_libros_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        else:
            for widget in self.panel_libros_frame.winfo_children(): widget.destroy()
        busqueda_frame_libros = ttk.Frame(self.panel_libros_frame)
        busqueda_frame_libros.pack(fill=tk.X, pady=(0,5), padx=2)
        ttk.Label(busqueda_frame_libros, text="Buscar Libro:").grid(row=0, column=0, padx=(0,5), pady=2, sticky="w")
        self.panel_libro_busqueda_entry = ttk.Entry(busqueda_frame_libros, width=20)
        self.panel_libro_busqueda_entry.grid(row=0, column=1, padx=0, pady=2, sticky="ew")
        self.panel_libro_busqueda_criterio_var = tk.StringVar(value="titulo")
        criterio_frame_libros = ttk.Frame(busqueda_frame_libros)
        criterio_frame_libros.grid(row=1, column=0, columnspan=2, sticky="w", pady=(2,0))
        ttk.Radiobutton(criterio_frame_libros, text="Título", variable=self.panel_libro_busqueda_criterio_var, value="titulo").pack(side=tk.LEFT, padx=(0,5))
        ttk.Radiobutton(criterio_frame_libros, text="Autor", variable=self.panel_libro_busqueda_criterio_var, value="autor").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(criterio_frame_libros, text="Género", variable=self.panel_libro_busqueda_criterio_var, value="genero").pack(side=tk.LEFT, padx=5)
        btn_buscar_libro_panel = ttk.Button(busqueda_frame_libros, text="Buscar", width=8, command=self._accion_buscar_libros_panel)
        btn_buscar_libro_panel.grid(row=0, column=2, padx=(5,0), pady=2, sticky="e")
        busqueda_frame_libros.columnconfigure(1, weight=1)
        acciones_panel_libros_frame = ttk.Frame(self.panel_libros_frame)
        acciones_panel_libros_frame.pack(fill=tk.X, pady=5, padx=2)
        btn_mostrar_todos_libros_panel = ttk.Button(acciones_panel_libros_frame, text="Mostrar Todos", command=self._accion_mostrar_todos_libros_panel)
        btn_mostrar_todos_libros_panel.pack(side=tk.LEFT, padx=(0,5))
        self.btn_panel_editar_libro = ttk.Button(acciones_panel_libros_frame, text="Editar Libro", command=self._accion_cargar_libro_modificar_panel)
        self.btn_panel_editar_libro.pack(side=tk.LEFT, padx=5)
        btn_eliminar_libro_panel = ttk.Button(acciones_panel_libros_frame, text="Eliminar Seleccionado", command=self._accion_eliminar_libro_panel)
        btn_eliminar_libro_panel.pack(side=tk.LEFT, padx=5)
        lista_frame_libros = ttk.Frame(self.panel_libros_frame)
        lista_frame_libros.pack(expand=True, fill=tk.BOTH, pady=5, padx=2)
        columnas_libros = ("id", "titulo", "autor", "genero", "disponible")
        self.tree_panel_libros = ttk.Treeview(lista_frame_libros, columns=columnas_libros, show="headings", height=10)
        self.tree_panel_libros.heading("id", text="ID"); self.tree_panel_libros.column("id", width=35, minwidth=30, stretch=tk.NO, anchor="center")
        self.tree_panel_libros.heading("titulo", text="Título"); self.tree_panel_libros.column("titulo", width=200, minwidth=150)
        self.tree_panel_libros.heading("autor", text="Autor"); self.tree_panel_libros.column("autor", width=150, minwidth=100)
        self.tree_panel_libros.heading("genero", text="Género"); self.tree_panel_libros.column("genero", width=100, minwidth=70)
        self.tree_panel_libros.heading("disponible", text="Estado"); self.tree_panel_libros.column("disponible", width=80, minwidth=70, stretch=tk.NO, anchor="center")
        scrollbar_libros_y = ttk.Scrollbar(lista_frame_libros, orient=tk.VERTICAL, command=self.tree_panel_libros.yview)
        scrollbar_libros_x = ttk.Scrollbar(lista_frame_libros, orient=tk.HORIZONTAL, command=self.tree_panel_libros.xview)
        self.tree_panel_libros.configure(yscrollcommand=scrollbar_libros_y.set, xscrollcommand=scrollbar_libros_x.set)
        scrollbar_libros_y.pack(side=tk.RIGHT, fill=tk.Y); scrollbar_libros_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree_panel_libros.pack(expand=True, fill=tk.BOTH)
        self.tree_panel_libros.bind("<Double-1>", self._on_double_click_libro_panel)

    def _crear_panel_usuarios_prestamos(self):
        if hasattr(self, 'panel_usuarios_prestamos_frame') and self.panel_usuarios_prestamos_frame.winfo_exists():
            for widget in self.panel_usuarios_prestamos_frame.winfo_children(): widget.destroy()
        else:
            self.panel_usuarios_prestamos_frame = ttk.LabelFrame(self.panel_visualizacion, text="Usuarios y Préstamos", padding="10")
            self.panel_usuarios_prestamos_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.frame_acciones_busqueda_usr = ttk.Frame(self.panel_usuarios_prestamos_frame)
        self.frame_acciones_busqueda_usr.pack(fill=tk.X, pady=(0,5), padx=2)

        self.btn_panel_editar_usuario = ttk.Button(self.frame_acciones_busqueda_usr, text="Editar Usuario", command=self._accion_cargar_usuario_modificar_panel)
        self.btn_panel_editar_usuario.pack(side=tk.LEFT, padx=(0,5))
        self.btn_panel_eliminar_usr_sel = ttk.Button(self.frame_acciones_busqueda_usr, text="Eliminar Sel.", command=self._accion_eliminar_usuario_panel)
        self.btn_panel_eliminar_usr_sel.pack(side=tk.LEFT, padx=5)
        self.btn_panel_ver_historial_usr = ttk.Button(self.frame_acciones_busqueda_usr, text="Ver Historial", command=self._accion_ver_historial_usuario_panel)
        self.btn_panel_ver_historial_usr.pack(side=tk.LEFT, padx=5)
        self.btn_panel_limpiar_seleccion_usr = ttk.Button(self.frame_acciones_busqueda_usr, text="Limpiar Sel.", command=self._accion_limpiar_seleccion_usuario_panel)
        self.btn_panel_limpiar_seleccion_usr.pack(side=tk.LEFT, padx=5)

        self.frame_busqueda_usuarios_panel = ttk.Frame(self.panel_usuarios_prestamos_frame, padding=(2,0))
        self.frame_busqueda_usuarios_panel.pack(fill=tk.X, pady=(5,5), padx=2)
        ttk.Label(self.frame_busqueda_usuarios_panel, text="Buscar Usuario:").grid(row=0, column=0, padx=(0,5), pady=2, sticky="w")
        self.panel_usuario_busqueda_entry = ttk.Entry(self.frame_busqueda_usuarios_panel, width=15)
        self.panel_usuario_busqueda_entry.grid(row=0, column=1, padx=0, pady=2, sticky="ew")
        self.panel_usuario_busqueda_criterio_var = tk.StringVar(value="nombre")
        criterio_frame_usr = ttk.Frame(self.frame_busqueda_usuarios_panel)
        criterio_frame_usr.grid(row=1, column=0, columnspan=2, sticky="w")
        self.rb_usr_nombre = ttk.Radiobutton(criterio_frame_usr, text="Nombre", variable=self.panel_usuario_busqueda_criterio_var, value="nombre")
        self.rb_usr_nombre.pack(side=tk.LEFT, padx=(0,5))
        self.rb_usr_ci = ttk.Radiobutton(criterio_frame_usr, text="C.I.", variable=self.panel_usuario_busqueda_criterio_var, value="ci")
        self.rb_usr_ci.pack(side=tk.LEFT, padx=5)
        self.btn_panel_buscar_usuario = ttk.Button(self.frame_busqueda_usuarios_panel, text="Buscar", width=7, command=self._accion_buscar_usuarios_panel)
        self.btn_panel_buscar_usuario.grid(row=0, column=2, padx=(5,0), pady=2, sticky="e")
        self.btn_panel_mostrar_todos_usuarios = ttk.Button(self.frame_busqueda_usuarios_panel, text="Todos", width=7, command=self._accion_mostrar_todos_usuarios_panel)
        self.btn_panel_mostrar_todos_usuarios.grid(row=1, column=2, padx=(5,0), pady=2, sticky="e")
        self.frame_busqueda_usuarios_panel.columnconfigure(1, weight=1)

        self.notebook_panel_derecho = ttk.Notebook(self.panel_usuarios_prestamos_frame, padding=(0, 5))
        self.notebook_panel_derecho.pack(expand=True, fill=tk.BOTH, pady=(5,0))
        self.frame_panel_usuarios_tab = ttk.Frame(self.notebook_panel_derecho, padding=5)
        self.notebook_panel_derecho.add(self.frame_panel_usuarios_tab, text='Lista de Usuarios')
        self.frame_panel_prestamos_activos_tab = ttk.Frame(self.notebook_panel_derecho, padding=5)
        self.notebook_panel_derecho.add(self.frame_panel_prestamos_activos_tab, text='Préstamos Activos Biblioteca')
        columnas_usr = ("id", "ci", "nombre", "telefono")
        self.tree_panel_usuarios = ttk.Treeview(self.frame_panel_usuarios_tab, columns=columnas_usr, show="headings", height=8)
        self.tree_panel_usuarios.heading("id", text="ID"); self.tree_panel_usuarios.column("id", width=35, minwidth=30, stretch=tk.NO, anchor="center")
        self.tree_panel_usuarios.heading("ci", text="C.I."); self.tree_panel_usuarios.column("ci", width=80, minwidth=70)
        self.tree_panel_usuarios.heading("nombre", text="Nombre"); self.tree_panel_usuarios.column("nombre", width=150, minwidth=100)
        self.tree_panel_usuarios.heading("telefono", text="Teléfono"); self.tree_panel_usuarios.column("telefono", width=100, minwidth=80)
        scrollbar_usr_y = ttk.Scrollbar(self.frame_panel_usuarios_tab, orient=tk.VERTICAL, command=self.tree_panel_usuarios.yview)
        self.tree_panel_usuarios.configure(yscrollcommand=scrollbar_usr_y.set)
        scrollbar_usr_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_panel_usuarios.pack(expand=True, fill=tk.BOTH)
        self.tree_panel_usuarios.bind("<Double-1>", self._on_double_click_usuario_panel)
        columnas_prest_act = ("id_p", "libro_titulo", "usuario_nombre", "fecha_prestamo", "libro_id_hidden")
        self.tree_panel_prestamos_activos = ttk.Treeview(self.frame_panel_prestamos_activos_tab, columns=columnas_prest_act, show="headings", height=8)
        self.tree_panel_prestamos_activos.heading("id_p", text="ID Préstamo"); self.tree_panel_prestamos_activos.column("id_p", width=80, minwidth=70, stretch=tk.NO, anchor="center")
        self.tree_panel_prestamos_activos.heading("libro_titulo", text="Libro"); self.tree_panel_prestamos_activos.column("libro_titulo", width=180, minwidth=150)
        self.tree_panel_prestamos_activos.heading("usuario_nombre", text="Usuario"); self.tree_panel_prestamos_activos.column("usuario_nombre", width=150, minwidth=100)
        self.tree_panel_prestamos_activos.heading("fecha_prestamo", text="F. Préstamo"); self.tree_panel_prestamos_activos.column("fecha_prestamo", width=100, minwidth=90, anchor="center")
        self.tree_panel_prestamos_activos.column("libro_id_hidden", width=0, stretch=tk.NO)
        scrollbar_prest_y = ttk.Scrollbar(self.frame_panel_prestamos_activos_tab, orient=tk.VERTICAL, command=self.tree_panel_prestamos_activos.yview)
        self.tree_panel_prestamos_activos.configure(yscrollcommand=scrollbar_prest_y.set)
        scrollbar_prest_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_panel_prestamos_activos.pack(expand=True, fill=tk.BOTH)
        self.notebook_panel_derecho.bind("<<NotebookTabChanged>>", self._on_panel_derecho_tab_changed)
        self._configurar_estado_botones_y_busqueda_panel_usuario()

    def _accion_guardar_libro_desde_tab(self):
        
        titulo = self.tab_libro_titulo_entry.get().strip(); autor = self.tab_libro_autor_entry.get().strip(); genero = self.tab_libro_genero_entry.get().strip()
        if not titulo or not autor: messagebox.showwarning("Datos Incompletos", "Título y Autor son obligatorios.", parent=self.frame_agregar_libro_tab); return
        if self.libro_id_a_modificar:
            if not self.biblioteca.eliminar_libro(self.libro_id_a_modificar):
                messagebox.showerror("Error al Modificar", f"No se pudo eliminar ID {self.libro_id_a_modificar}. Modificación cancelada.", parent=self.frame_agregar_libro_tab)
                self._accion_limpiar_form_libro_tab(); self._actualizar_todas_las_listas_y_combos(); return
            nuevo_libro = self.biblioteca.agregar_libro(titulo, autor, genero)
            if nuevo_libro and nuevo_libro.id_libro: messagebox.showinfo("Libro Modificado", f"Libro '{titulo}' (ID original: {self.libro_id_a_modificar}) modificado (ID: {nuevo_libro.id_libro}).", parent=self.frame_agregar_libro_tab)
            else: messagebox.showerror("Error al Modificar", "Original eliminado, pero no se guardó el nuevo.", parent=self.frame_agregar_libro_tab)
        else:
            nuevo_libro = self.biblioteca.agregar_libro(titulo, autor, genero)
            if nuevo_libro and nuevo_libro.id_libro: messagebox.showinfo("Libro Agregado", f"Libro '{titulo}' agregado (ID: {nuevo_libro.id_libro}).", parent=self.frame_agregar_libro_tab)
            else: messagebox.showerror("Error al Agregar", f"No se pudo agregar '{titulo}'.", parent=self.frame_agregar_libro_tab)
        self._accion_limpiar_form_libro_tab(); self._actualizar_todas_las_listas_y_combos()


    def _accion_limpiar_form_libro_tab(self):
        
        self.tab_libro_titulo_entry.delete(0, tk.END); self.tab_libro_autor_entry.delete(0, tk.END); self.tab_libro_genero_entry.delete(0, tk.END)
        self.libro_id_a_modificar = None; self.btn_tab_guardar_libro.config(text="Guardar Libro")
        try: self.notebook_principal.tab(self.frame_agregar_libro_tab, text='Agregar Libro')
        except tk.TclError: pass

    def _accion_guardar_usuario_desde_tab(self):
        
        ci = self.tab_usuario_ci_entry.get().strip(); nombre = self.tab_usuario_nombre_entry.get().strip(); telefono = self.tab_usuario_telefono_entry.get().strip()
        if not ci or not nombre: messagebox.showwarning("Datos Incompletos", "C.I. y Nombre son obligatorios.", parent=self.frame_agregar_usuario_tab); return
        if self.usuario_id_a_modificar:
            if not self.biblioteca.eliminar_usuario(self.usuario_id_a_modificar):
                messagebox.showerror("Error al Modificar", f"No se pudo eliminar ID {self.usuario_id_a_modificar}. Modificación cancelada.", parent=self.frame_agregar_usuario_tab)
                self._accion_limpiar_form_usuario_tab(); self._actualizar_todas_las_listas_y_combos(); return
            nuevo_usuario = self.biblioteca.registrar_usuario(ci, nombre, telefono)
            if nuevo_usuario and nuevo_usuario.id_usuario: messagebox.showinfo("Usuario Modificado", f"Usuario '{nombre}' (ID original: {self.usuario_id_a_modificar}) modificado (ID: {nuevo_usuario.id_usuario}).", parent=self.frame_agregar_usuario_tab)
            else: messagebox.showerror("Error al Modificar", f"Original eliminado, pero no se guardó el nuevo (C.I.: {ci}).\nC.I. podría ya existir.", parent=self.frame_agregar_usuario_tab)
        else:
            nuevo_usuario = self.biblioteca.registrar_usuario(ci, nombre, telefono)
            if nuevo_usuario and nuevo_usuario.id_usuario: messagebox.showinfo("Usuario Registrado", f"Usuario '{nombre}' (C.I.: {ci}) registrado (ID: {nuevo_usuario.id_usuario}).", parent=self.frame_agregar_usuario_tab)
            else: messagebox.showerror("Error al Registrar", f"No se pudo registrar '{nombre}' (C.I.: {ci}).\nC.I. podría ya existir.", parent=self.frame_agregar_usuario_tab)
        self._accion_limpiar_form_usuario_tab(); self._actualizar_todas_las_listas_y_combos()

    def _accion_limpiar_form_usuario_tab(self):
        
        self.tab_usuario_ci_entry.delete(0, tk.END); self.tab_usuario_nombre_entry.delete(0, tk.END); self.tab_usuario_telefono_entry.delete(0, tk.END)
        self.usuario_id_a_modificar = None; self.btn_tab_guardar_usuario.config(text="Guardar Usuario")
        try: self.notebook_principal.tab(self.frame_agregar_usuario_tab, text='Agregar Usuario')
        except tk.TclError: pass

    def _accion_confirmar_prestamo_tab(self):
        libro_sel_str = self.prestamo_tab_libro_combobox.get().strip() # strip() para entradas manuales
        usuario_sel_str = self.prestamo_tab_usuario_combobox.get().strip()

        if not libro_sel_str or not usuario_sel_str:
            messagebox.showwarning("Selección Incompleta", "Debe seleccionar/ingresar un libro y un usuario.", parent=self.frame_registrar_prestamo_tab); return

        libro_id = None
        if hasattr(self, 'map_libros_disponibles_prestamo'): 
            libro_id = self.map_libros_disponibles_prestamo.get(libro_sel_str)

        if libro_id is None and libro_sel_str.isdigit(): # Si no está en mapa y es número, tratar como ID
            try:
                temp_id = int(libro_sel_str)
                libro_obj = Libro.get_by_id(temp_id)
                if libro_obj and libro_obj.disponible:
                    libro_id = temp_id
                elif libro_obj and not libro_obj.disponible: # Si se ingresa ID de libro no disponible
                    messagebox.showwarning("Libro no Disponible", f"El libro con ID {temp_id} ('{libro_obj.titulo}') no está disponible.", parent=self.frame_registrar_prestamo_tab)
                    self._actualizar_todas_las_listas_y_combos() # Refrescar 
                    return
            except ValueError: pass # No era un número válido

        print(f"DEBUG Préstamo: Libro Seleccionado/Escrito='{libro_sel_str}' -> ID Obtenido={libro_id}")

        usuario_id = None
        if hasattr(self, 'map_usuarios_prestamo'):
            usuario_id = self.map_usuarios_prestamo.get(usuario_sel_str)

        if usuario_id is None and usuario_sel_str.isdigit():
            try:
                temp_id = int(usuario_sel_str)
                if Usuario.get_by_id(temp_id):
                     usuario_id = temp_id
            except ValueError: pass

        print(f"DEBUG Préstamo: Usuario Seleccionado/Escrito='{usuario_sel_str}' -> ID Obtenido={usuario_id}")

        if libro_id is None or usuario_id is None:
            error_msg = "Error de Selección/Entrada:\n"
            if libro_id is None: error_msg += f"- Libro '{libro_sel_str}' no válido o no disponible.\n"
            if usuario_id is None: error_msg += f"- Usuario '{usuario_sel_str}' no válido.\n"
            error_msg += "Asegúrese de seleccionar de las listas o ingresar un ID válido."
            messagebox.showerror("Error de Selección", error_msg, parent=self.frame_registrar_prestamo_tab)
            return

        fecha_prestamo = datetime.date.today().isoformat()
        prestamo = self.biblioteca.realizar_prestamo(libro_id, usuario_id, fecha_prestamo)

        if prestamo and prestamo.id_prestamo:
            messagebox.showinfo("Préstamo Exitoso", f"Préstamo ID: {prestamo.id_prestamo} registrado.", parent=self.frame_registrar_prestamo_tab)
            self.prestamo_tab_libro_combobox.set('')
            
        else:
            messagebox.showerror("Error de Préstamo", "No se pudo realizar el préstamo.\nConsulte la consola para más detalles (ej. libro no disponible, usuario no existe).", parent=self.frame_registrar_prestamo_tab)
        self._actualizar_todas_las_listas_y_combos()

    def _poblar_combobox_libros_disponibles_prestamo(self):
        
        self.prestamo_tab_libro_combobox.set(''); self.prestamo_tab_libro_combobox['values'] = []
        libros_disp = [l for l in self.biblioteca.listar_libros() if l.disponible]
        self.map_libros_disponibles_prestamo = {f"{l.id_libro} - {l.titulo}": l.id_libro for l in libros_disp}
        if libros_disp: self.prestamo_tab_libro_combobox['values'] = list(self.map_libros_disponibles_prestamo.keys())
        else: self.map_libros_disponibles_prestamo = {}

    def _poblar_combobox_usuarios_prestamo(self):
        
        self.prestamo_tab_usuario_combobox.set(''); self.prestamo_tab_usuario_combobox['values'] = []
        usuarios = self.biblioteca.listar_usuarios()
        self.map_usuarios_prestamo = {f"{u.id_usuario} - {u.nombre} (CI: {u.ci})": u.id_usuario for u in usuarios}
        if usuarios: self.prestamo_tab_usuario_combobox['values'] = list(self.map_usuarios_prestamo.keys())
        else: self.map_usuarios_prestamo = {}

    def _accion_confirmar_devolucion_tab(self):
        libro_prestado_sel_str = self.devolucion_tab_libro_combobox.get().strip()
        if not libro_prestado_sel_str: messagebox.showwarning("Selección Incompleta", "Seleccione o ingrese un libro a devolver.", parent=self.frame_registrar_devolucion_tab); return

        libro_id = None
        if hasattr(self, 'map_libros_prestados_devolucion'):
            libro_id = self.map_libros_prestados_devolucion.get(libro_prestado_sel_str)

        if libro_id is None: 
            
            try:
                if " - " in libro_prestado_sel_str:
                    libro_id_str_part = libro_prestado_sel_str.split(" - ")[0]
                    if libro_id_str_part.isdigit():
                        libro_id = int(libro_id_str_part)
                elif libro_prestado_sel_str.isdigit(): # Si solo ingresó un ID
                    libro_id = int(libro_prestado_sel_str)
            except ValueError:
                pass 

        print(f"DEBUG Devolución: Libro Seleccionado/Escrito='{libro_prestado_sel_str}' -> ID Obtenido={libro_id}")

        if libro_id is None:
            messagebox.showerror("Error Selección", "Entrada de libro no válida. Seleccione de la lista o ingrese un ID de libro prestado válido.", parent=self.frame_registrar_devolucion_tab); return

        fecha_devolucion = datetime.date.today().isoformat()
        if self.biblioteca.registrar_devolucion(libro_id, fecha_devolucion):
            messagebox.showinfo("Devolución Exitosa", f"Libro (ID: {libro_id}) devuelto.", parent=self.frame_registrar_devolucion_tab);
            self.devolucion_tab_libro_combobox.set('')
        else:
            messagebox.showerror("Error Devolución", f"No se pudo devolver libro (ID: {libro_id}).\nNo tenía préstamo activo o ya fue devuelto.", parent=self.frame_registrar_devolucion_tab)
        self._actualizar_todas_las_listas_y_combos()

    def _poblar_combobox_libros_prestados_devolucion(self):
        
        self.devolucion_tab_libro_combobox.set(''); self.devolucion_tab_libro_combobox['values'] = []
        prestamos_activos = self.biblioteca.listar_prestamos_activos()
        self.map_libros_prestados_devolucion = {f"{p.libro_id} - {p.libro_titulo if p.libro_titulo else 'N/A'} (a: {p.usuario_nombre if p.usuario_nombre else 'N/A'})": p.libro_id for p in prestamos_activos}
        if prestamos_activos: self.devolucion_tab_libro_combobox['values'] = list(self.map_libros_prestados_devolucion.keys())


    def _accion_buscar_libros_panel(self):
        
        termino = self.panel_libro_busqueda_entry.get().strip(); criterio = self.panel_libro_busqueda_criterio_var.get()
        if not termino: self._cargar_libros_en_tabla(); return
        libros_encontrados = self.biblioteca.buscar_libros(termino, criterio)
        if not libros_encontrados: messagebox.showinfo("Sin Resultados", f"No hay libros para '{termino}' por '{criterio}'.", parent=self.panel_libros_frame)
        self._cargar_libros_en_tabla(libros_encontrados)

    def _accion_mostrar_todos_libros_panel(self):
        
        self.panel_libro_busqueda_entry.delete(0, tk.END); self.panel_libro_busqueda_criterio_var.set("titulo")
        self._cargar_libros_en_tabla()

    def _accion_eliminar_libro_panel(self):
        
        seleccion = self.tree_panel_libros.focus()
        if not seleccion: messagebox.showwarning("Nada Seleccionado", "Seleccione libro a eliminar.", parent=self.panel_libros_frame); return
        datos = self.tree_panel_libros.item(seleccion, "values")
        try: id_libro, titulo, _, _, estado = int(datos[0]), datos[1], datos[2], datos[3], datos[4]
        except (IndexError, ValueError, TypeError): messagebox.showerror("Error Datos", "No se obtuvo info del libro.", parent=self.panel_libros_frame); return
        if estado.lower() == "prestado": messagebox.showwarning("Libro Prestado", f"Libro '{titulo}' está prestado.", parent=self.panel_libros_frame); return
        if messagebox.askyesno("Confirmar", f"Eliminar '{titulo}' (ID: {id_libro})?", parent=self.panel_libros_frame):
            if self.biblioteca.eliminar_libro(id_libro): messagebox.showinfo("Libro Eliminado", f"'{titulo}' eliminado.", parent=self.panel_libros_frame)
            else: messagebox.showerror("Error", f"No se pudo eliminar '{titulo}'.", parent=self.panel_libros_frame)
            self._actualizar_todas_las_listas_y_combos()

    def _accion_cargar_libro_modificar_panel(self):
        
        seleccion = self.tree_panel_libros.focus()
        if not seleccion: messagebox.showwarning("Nada Seleccionado", "Seleccione libro a modificar.", parent=self.panel_libros_frame); return
        datos = self.tree_panel_libros.item(seleccion, "values")
        try: id_libro, titulo, autor, genero, _ = int(datos[0]), datos[1], datos[2], datos[3], datos[4]
        except (IndexError, ValueError, TypeError): messagebox.showerror("Error Datos", "No se obtuvo info del libro.", parent=self.panel_libros_frame); return
        self._accion_limpiar_form_libro_tab()
        self.tab_libro_titulo_entry.insert(0, titulo); self.tab_libro_autor_entry.insert(0, autor); self.tab_libro_genero_entry.insert(0, genero)
        self.libro_id_a_modificar = id_libro; self.btn_tab_guardar_libro.config(text=f"Guardar Cambios (ID: {id_libro})")
        self.notebook_principal.tab(self.frame_agregar_libro_tab, text=f'Modificar Libro (ID: {id_libro})')
        self.notebook_principal.select(self.frame_agregar_libro_tab)

    def _on_double_click_libro_panel(self, event):
        
        item_id = self.tree_panel_libros.identify_row(event.y)
        if item_id: self.tree_panel_libros.focus(item_id); self._accion_cargar_libro_modificar_panel()

    def _configurar_estado_botones_y_busqueda_panel_usuario(self):
        
        if not hasattr(self, 'notebook_panel_derecho'): return
        try:
            pestana_activa_idx = self.notebook_panel_derecho.index(self.notebook_panel_derecho.select())
        except tk.TclError: pestana_activa_idx = 0
        estado_controles_usuario = tk.NORMAL if pestana_activa_idx == 0 else tk.DISABLED
        if hasattr(self, 'btn_panel_editar_usuario'): self.btn_panel_editar_usuario.config(state=estado_controles_usuario)
        if hasattr(self, 'btn_panel_eliminar_usr_sel'): self.btn_panel_eliminar_usr_sel.config(state=estado_controles_usuario)
        if hasattr(self, 'btn_panel_ver_historial_usr'): self.btn_panel_ver_historial_usr.config(state=estado_controles_usuario)
        if hasattr(self, 'btn_panel_limpiar_seleccion_usr'): self.btn_panel_limpiar_seleccion_usr.config(state=estado_controles_usuario)
        if hasattr(self, 'panel_usuario_busqueda_entry'): self.panel_usuario_busqueda_entry.config(state=estado_controles_usuario)
        if hasattr(self, 'rb_usr_nombre'): self.rb_usr_nombre.config(state=estado_controles_usuario)
        if hasattr(self, 'rb_usr_ci'): self.rb_usr_ci.config(state=estado_controles_usuario)
        if hasattr(self, 'btn_panel_buscar_usuario'): self.btn_panel_buscar_usuario.config(state=estado_controles_usuario)
        if hasattr(self, 'btn_panel_mostrar_todos_usuarios'): self.btn_panel_mostrar_todos_usuarios.config(state=estado_controles_usuario)

    def _on_panel_derecho_tab_changed(self, event=None):
        
        self._configurar_estado_botones_y_busqueda_panel_usuario()

    def _accion_eliminar_usuario_panel(self):
        
        try: pestana_activa = self.notebook_panel_derecho.index(self.notebook_panel_derecho.select())
        except tk.TclError: messagebox.showwarning("Panel no listo", "Panel de usuarios no listo.", parent=self.panel_usuarios_prestamos_frame); return
        if pestana_activa != 0: messagebox.showwarning("Pestaña Incorrecta", "Seleccione usuario de 'Lista de Usuarios'.", parent=self.panel_usuarios_prestamos_frame); return
        seleccion = self.tree_panel_usuarios.focus()
        if not seleccion: messagebox.showwarning("Nada Seleccionado", "Seleccione usuario a eliminar.", parent=self.panel_usuarios_prestamos_frame); return
        datos = self.tree_panel_usuarios.item(seleccion, "values")
        try: id_usuario, _, nombre, _ = int(datos[0]), datos[1], datos[2], datos[3]
        except (IndexError, ValueError, TypeError): messagebox.showerror("Error Datos", "No se obtuvo info del usuario.", parent=self.panel_usuarios_prestamos_frame); return
        libros_prestados_ids = [p.libro_id for p in self.biblioteca.listar_prestamos_activos() if hasattr(p, 'usuario_id') and p.usuario_id == id_usuario]
        adv = f"\n\nADVERTENCIA: Usuario tiene {len(libros_prestados_ids)} préstamo(s) activo(s). Se eliminarán y libros se marcarán disponibles." if libros_prestados_ids else ""
        if messagebox.askyesno("Confirmar", f"Eliminar '{nombre}' (ID: {id_usuario})?{adv}", parent=self.panel_usuarios_prestamos_frame):
            libros_a_poner_disponibles = libros_prestados_ids[:] if libros_prestados_ids else []
            if self.biblioteca.eliminar_usuario(id_usuario):
                messagebox.showinfo("Usuario Eliminado", f"'{nombre}' eliminado.", parent=self.panel_usuarios_prestamos_frame)
                libros_actualizados_count = 0
                for libro_id in libros_a_poner_disponibles:
                    libro = Libro.get_by_id(libro_id)
                    if libro and not libro.disponible:
                        libro.disponible = True
                        if libro.save_to_db(): libros_actualizados_count += 1
                if libros_actualizados_count > 0: messagebox.showinfo("Libros Actualizados", f"{libros_actualizados_count} libro(s) marcados como disponibles.", parent=self.panel_usuarios_prestamos_frame)
            else: messagebox.showerror("Error", f"No se pudo eliminar '{nombre}'.", parent=self.panel_usuarios_prestamos_frame)
            self._actualizar_todas_las_listas_y_combos()

    def _accion_cargar_usuario_modificar_panel(self):
        
        try: pestana_activa = self.notebook_panel_derecho.index(self.notebook_panel_derecho.select())
        except tk.TclError: messagebox.showwarning("Panel no listo", "Panel de usuarios no listo.", parent=self.panel_usuarios_prestamos_frame); return
        if pestana_activa != 0: messagebox.showwarning("Pestaña Incorrecta", "Seleccione usuario de 'Lista de Usuarios'.", parent=self.panel_usuarios_prestamos_frame); return
        seleccion = self.tree_panel_usuarios.focus()
        if not seleccion: messagebox.showwarning("Nada Seleccionado", "Seleccione usuario a modificar.", parent=self.panel_usuarios_prestamos_frame); return
        datos = self.tree_panel_usuarios.item(seleccion, "values")
        try: id_usr, ci, nombre, telefono = int(datos[0]), datos[1], datos[2], datos[3]
        except (IndexError, ValueError, TypeError): messagebox.showerror("Error Datos", "No se obtuvo info del usuario.", parent=self.panel_usuarios_prestamos_frame); return
        self._accion_limpiar_form_usuario_tab()
        self.tab_usuario_ci_entry.insert(0, ci); self.tab_usuario_nombre_entry.insert(0, nombre); self.tab_usuario_telefono_entry.insert(0, telefono)
        self.usuario_id_a_modificar = id_usr; self.btn_tab_guardar_usuario.config(text=f"Guardar Cambios (ID: {id_usr})")
        self.notebook_principal.tab(self.frame_agregar_usuario_tab, text=f'Modificar Usuario (ID: {id_usr})')
        self.notebook_principal.select(self.frame_agregar_usuario_tab)

    def _on_double_click_usuario_panel(self, event):
        
        item_id = self.tree_panel_usuarios.identify_row(event.y)
        if item_id:
            self.tree_panel_usuarios.focus(item_id)
            self._accion_cargar_usuario_modificar_panel()

    def _accion_ver_historial_usuario_panel(self):
        
        seleccion = self.tree_panel_usuarios.focus()
        if not seleccion:
            messagebox.showwarning("Sin Selección", "Por favor, seleccione un usuario de la 'Lista de Usuarios' primero.", parent=self.panel_usuarios_prestamos_frame)
            return
        datos_usuario = self.tree_panel_usuarios.item(seleccion, "values")
        try:
            usuario_id = int(datos_usuario[0]); nombre_usuario = datos_usuario[2]
            historial_window = tk.Toplevel(self)
            historial_window.title(f"Historial de Préstamos - {nombre_usuario}")
            win_width = 650; win_height = 400
            screen_width = self.winfo_screenwidth(); screen_height = self.winfo_screenheight()
            x = (screen_width/2) - (win_width/2); y = (screen_height/2) - (win_height/2)
            historial_window.geometry('%dx%d+%d+%d' % (win_width, win_height, int(x), int(y)))
            historial_window.transient(self); historial_window.grab_set()
            self._cargar_historial_prestamos_usuario(usuario_id, nombre_usuario, historial_window)
        except (IndexError, ValueError, TypeError):
            messagebox.showerror("Error de Datos", "No se pudo obtener la información del usuario seleccionado.", parent=self.panel_usuarios_prestamos_frame)

    def _accion_limpiar_seleccion_usuario_panel(self):
        
        if hasattr(self, 'tree_panel_usuarios'):
            seleccion = self.tree_panel_usuarios.selection()
            if seleccion:
                self.tree_panel_usuarios.selection_remove(seleccion)
                self.tree_panel_usuarios.focus("")

    def _cargar_historial_prestamos_usuario(self, usuario_id, nombre_usuario, parent_window):
        
        info_frame = ttk.Frame(parent_window, padding=5); info_frame.pack(fill=tk.X)
        label_info_historial_var = tk.StringVar(value=f"Historial para: {nombre_usuario} (ID: {usuario_id})")
        label_info_historial = ttk.Label(info_frame, textvariable=label_info_historial_var, wraplength=parent_window.winfo_width()-20)
        label_info_historial.pack(pady=(0,5), fill=tk.X)
        tree_frame = ttk.Frame(parent_window, padding=5); tree_frame.pack(expand=True, fill=tk.BOTH)
        columnas_historial_usr = ("id_prestamo", "libro_titulo", "fecha_prestamo", "fecha_devolucion", "estado_prestamo")
        tree_historial = ttk.Treeview(tree_frame, columns=columnas_historial_usr, show="headings", height=10)
        tree_historial.heading("id_prestamo", text="ID Préstamo");    tree_historial.column("id_prestamo", width=70, minwidth=60, stretch=tk.NO, anchor="center")
        tree_historial.heading("libro_titulo", text="Libro (Título)"); tree_historial.column("libro_titulo", width=200, minwidth=150)
        tree_historial.heading("fecha_prestamo", text="F. Préstamo"); tree_historial.column("fecha_prestamo", width=100, minwidth=90, anchor="center")
        tree_historial.heading("fecha_devolucion", text="F. Devolución");tree_historial.column("fecha_devolucion", width=100, minwidth=90, anchor="center")
        tree_historial.heading("estado_prestamo", text="Estado");     tree_historial.column("estado_prestamo", width=80, minwidth=70, anchor="center")
        scrollbar_hist_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree_historial.yview)
        tree_historial.configure(yscrollcommand=scrollbar_hist_y.set)
        scrollbar_hist_y.pack(side=tk.RIGHT, fill=tk.Y); tree_historial.pack(expand=True, fill=tk.BOTH)
        historial_data = self.biblioteca.listar_historial_prestamos_usuario(usuario_id)
        if historial_data:
            for p in historial_data:
                estado = "Devuelto" if p.fecha_devolucion else "Activo"
                fecha_dev_str = p.fecha_devolucion if p.fecha_devolucion else "---"
                tree_historial.insert("", tk.END, values=(p.id_prestamo, p.libro_titulo if p.libro_titulo else f"Libro ID: {p.libro_id}", p.fecha_prestamo, fecha_dev_str, estado), tags=(estado.lower(),))
            tree_historial.tag_configure('activo', background='#FFFFE0'); tree_historial.tag_configure('devuelto', background='#E0E0E0')
        else: tree_historial.insert("", tk.END, values=("", "Este usuario no tiene préstamos registrados.", "", "", ""))
        btn_cerrar = ttk.Button(parent_window, text="Cerrar Historial", command=parent_window.destroy)
        btn_cerrar.pack(pady=10)

    def _cargar_libros_en_tabla(self, libros_a_mostrar=None):
        
        if hasattr(self, 'tree_panel_libros'):
            for i in self.tree_panel_libros.get_children(): self.tree_panel_libros.delete(i)
            libros = libros_a_mostrar if libros_a_mostrar is not None else self.biblioteca.listar_libros()
            for libro in libros:
                estado = "Disponible" if libro.disponible else "Prestado"
                self.tree_panel_libros.insert("", tk.END, values=(libro.id_libro, libro.titulo, libro.autor, libro.genero, estado), tags=(estado.lower(),))
            self.tree_panel_libros.tag_configure('prestado', background='#FFD2D2'); self.tree_panel_libros.tag_configure('disponible', background='#D2FFD2')
        else: print("DEBUG: tree_panel_libros no existe aún.")

    def _cargar_usuarios_en_tabla(self, usuarios_a_mostrar=None):
        
        if hasattr(self, 'tree_panel_usuarios'):
            for i in self.tree_panel_usuarios.get_children(): self.tree_panel_usuarios.delete(i)
            usuarios = usuarios_a_mostrar if usuarios_a_mostrar is not None else self.biblioteca.listar_usuarios()
            for u in usuarios: self.tree_panel_usuarios.insert("", tk.END, values=(u.id_usuario, u.ci, u.nombre, u.telefono))
        else: print("DEBUG: tree_panel_usuarios no existe aún.")

    def _cargar_prestamos_activos_en_tabla(self):
        
        if hasattr(self, 'tree_panel_prestamos_activos'):
            for i in self.tree_panel_prestamos_activos.get_children(): self.tree_panel_prestamos_activos.delete(i)
            prestamos = self.biblioteca.listar_prestamos_activos()
            for p in prestamos: self.tree_panel_prestamos_activos.insert("", tk.END, values=(p.id_prestamo, p.libro_titulo, p.usuario_nombre, p.fecha_prestamo, p.libro_id))
        else: print("DEBUG: tree_panel_prestamos_activos no existe aún.")

    def _accion_buscar_usuarios_panel(self):
        
        termino = self.panel_usuario_busqueda_entry.get().strip()
        criterio = self.panel_usuario_busqueda_criterio_var.get()
        if not termino:
            self._cargar_usuarios_en_tabla()
            return
        usuarios_encontrados = self.biblioteca.buscar_usuarios(termino, criterio)
        if not usuarios_encontrados:
            messagebox.showinfo("Sin Resultados", f"No se encontraron usuarios para '{termino}' por '{criterio}'.", parent=self.frame_panel_usuarios_tab)
        self._cargar_usuarios_en_tabla(usuarios_encontrados)

    def _accion_mostrar_todos_usuarios_panel(self):
        
        self.panel_usuario_busqueda_entry.delete(0, tk.END)
        self.panel_usuario_busqueda_criterio_var.set("nombre")
        self._cargar_usuarios_en_tabla()

    def _actualizar_todas_las_listas_y_combos(self):
        
        print("DEBUG: _actualizar_todas_las_listas_y_combos")
        self._cargar_libros_en_tabla()
        self._cargar_usuarios_en_tabla()
        self._cargar_prestamos_activos_en_tabla()
        self._poblar_combobox_libros_disponibles_prestamo()
        self._poblar_combobox_usuarios_prestamo()
        self._poblar_combobox_libros_prestados_devolucion()

if __name__ == '__main__':
    import database
    database.crear_tablas()
    app = MainWindow()
    app.notebook_principal.select(2)
    if hasattr(app, 'notebook_panel_derecho'):
        app.notebook_panel_derecho.select(0)
        app._configurar_estado_botones_y_busqueda_panel_usuario()
    app.mainloop()
