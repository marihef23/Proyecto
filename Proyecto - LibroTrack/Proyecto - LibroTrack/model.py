import datetime
import database # Importamos el módulo de base de datos

class Libro:
    def __init__(self, id_libro, titulo, autor, genero, disponible=True):
        self.id_libro = id_libro
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.disponible = disponible

    def __str__(self):
        estado = "Disponible" if self.disponible else "Prestado"
        return f"ID: {self.id_libro}, Título: {self.titulo}, Autor: {self.autor}, Género: {self.genero}, Estado: {estado}"

    @staticmethod
    def _a_objeto(fila_db):
        """Convierte una fila de la base de datos (tupla) a un objeto Libro."""
        if fila_db:
            return Libro(id_libro=fila_db[0], titulo=fila_db[1], autor=fila_db[2], genero=fila_db[3], disponible=bool(fila_db[4]))
        return None

    def save_to_db(self):
        if self.id_libro is None:
            nuevo_id = database.agregar_libro_db(self.titulo, self.autor, self.genero)
            if nuevo_id: self.id_libro = nuevo_id; return True
            else: return False
        else:
            return database.actualizar_libro_db(self.id_libro, self.titulo, self.autor, self.genero, self.disponible)

    def delete_from_db(self):
        if self.id_libro is not None: return database.eliminar_libro_db(self.id_libro)
        return False

    @staticmethod
    def get_by_id(id_libro):
        fila = database.obtener_libro_por_id_db(id_libro)
        return Libro._a_objeto(fila)

    @staticmethod
    def get_all():
        filas = database.obtener_libros_db()
        return [Libro._a_objeto(fila) for fila in filas]

    @staticmethod
    def search(termino, tipo_busqueda):
        filas = database.buscar_libros_db(termino, tipo_busqueda)
        return [Libro._a_objeto(fila) for fila in filas]

class Usuario:
    def __init__(self, id_usuario, ci, nombre, telefono):
        self.id_usuario = id_usuario
        self.ci = ci
        self.nombre = nombre
        self.telefono = telefono

    def __str__(self):
        return f"ID: {self.id_usuario}, C.I.: {self.ci}, Nombre: {self.nombre}, Teléfono: {self.telefono}"

    @staticmethod
    def _a_objeto(fila_db):
        if fila_db: # id, ci, nombre, telefono
            return Usuario(id_usuario=fila_db[0], ci=fila_db[1], nombre=fila_db[2], telefono=fila_db[3])
        return None

    def save_to_db(self):
        if self.id_usuario is None:
            nuevo_id = database.agregar_usuario_db(self.ci, self.nombre, self.telefono)
            if nuevo_id: self.id_usuario = nuevo_id; return True
            else: return False
        else:
            return database.actualizar_usuario_db(self.id_usuario, self.ci, self.nombre, self.telefono)

    def delete_from_db(self):
        if self.id_usuario is not None: return database.eliminar_usuario_db(self.id_usuario)
        return False

    @staticmethod
    def get_by_id(id_usuario):
        fila = database.obtener_usuario_por_id_db(id_usuario)
        return Usuario._a_objeto(fila)

    @staticmethod
    def get_all():
        filas = database.obtener_usuarios_db()
        return [Usuario._a_objeto(fila) for fila in filas]

    @classmethod
    def search(cls, termino, criterio): 
        """Busca usuarios en la base de datos por CI o Nombre."""
        if criterio not in ["ci", "nombre"]:
            print(f"Error: Criterio de búsqueda '{criterio}' no válido para usuarios.")
            return []
        filas = database.buscar_usuarios_db(termino, criterio)
        usuarios_encontrados = []
        for fila in filas:
            usuarios_encontrados.append(cls._a_objeto(fila))
        return usuarios_encontrados

class Prestamo:
    def __init__(self, id_prestamo, libro_id, usuario_id, fecha_prestamo, fecha_devolucion=None,
                 libro_titulo=None, usuario_nombre=None, usuario_ci=None):
        self.id_prestamo = id_prestamo
        self.libro_id = libro_id
        self.usuario_id = usuario_id
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        self.libro_titulo = libro_titulo
        self.usuario_nombre = usuario_nombre
        self.usuario_ci = usuario_ci

    def __str__(self):
        estado = f"Devuelto el {self.fecha_devolucion}" if self.fecha_devolucion else "Activo"
        libro_info = f"Libro ID: {self.libro_id}" + (f" ('{self.libro_titulo}')" if self.libro_titulo else "")
        usuario_info = f"Usuario ID: {self.usuario_id}" + (f" ({self.usuario_nombre})" if self.usuario_nombre else "")
        ci_info = (f" CI Usuario: {self.usuario_ci}" if self.usuario_ci else "")
        return f"ID Préstamo: {self.id_prestamo}, {libro_info}, {usuario_info}{ci_info}, F.Préstamo: {self.fecha_prestamo}, Estado: {estado}"

    @staticmethod
    def _a_objeto(fila_db, tipo_join=None, usuario_id_contexto=None):
        if not fila_db: return None
        id_prestamo = fila_db[0]; libro_id = fila_db[1]
        libro_titulo = None; usuario_nombre = None; usuario_ci = None
        usuario_id_obj = usuario_id_contexto
        fecha_prestamo_val = None 
        fecha_devolucion_val = None

        if tipo_join == 'activos':
            libro_titulo = fila_db[2]; usuario_id_obj = fila_db[3]; usuario_nombre = fila_db[4]
            fecha_prestamo_val = fila_db[5]; fecha_devolucion_val = None
        elif tipo_join == 'todos':
            libro_titulo = fila_db[2]; usuario_id_obj = fila_db[3]; usuario_nombre = fila_db[4]
            fecha_prestamo_val = fila_db[5]; fecha_devolucion_val = fila_db[6]
        elif tipo_join == 'por_id':
            libro_titulo = fila_db[2]; usuario_id_obj = fila_db[3]; usuario_nombre = fila_db[4]
            usuario_ci = fila_db[5]; fecha_prestamo_val = fila_db[6]; fecha_devolucion_val = fila_db[7]
        elif tipo_join == 'activo_por_libro':
            usuario_id_obj = fila_db[2]; fecha_prestamo_val = fila_db[3]; fecha_devolucion_val = fila_db[4]
        elif tipo_join == 'historial_usuario':
            libro_titulo = fila_db[2]; fecha_prestamo_val = fila_db[3]; fecha_devolucion_val = fila_db[4]
        else:
            usuario_id_obj = fila_db[2]; fecha_prestamo_val = fila_db[3]; fecha_devolucion_val = fila_db[4]
        return Prestamo(id_prestamo, libro_id, usuario_id_obj, fecha_prestamo_val, fecha_devolucion_val, libro_titulo, usuario_nombre, usuario_ci)

    def save_to_db(self):
        if self.id_prestamo is None:
            nuevo_id = database.registrar_prestamo_db(self.libro_id, self.usuario_id, self.fecha_prestamo)
            if nuevo_id: self.id_prestamo = nuevo_id; return True
        return False

    def marcar_como_devuelto(self, fecha_devolucion=None):
        if self.id_prestamo is not None:
            if fecha_devolucion is None: fecha_devolucion = datetime.date.today().isoformat()
            if database.registrar_devolucion_db(self.id_prestamo, fecha_devolucion):
                self.fecha_devolucion = fecha_devolucion; return True
        return False

    @staticmethod
    def delete_from_db(id_prestamo): print(f"DEBUG: La eliminación de préstamos se maneja por ON DELETE CASCADE.")

    @staticmethod
    def get_by_id(id_prestamo): return Prestamo._a_objeto(database.obtener_prestamo_por_id_db(id_prestamo), tipo_join='por_id')

    @staticmethod
    def get_all(): return [Prestamo._a_objeto(fila, tipo_join='todos') for fila in database.obtener_todos_los_prestamos_db()]

    @staticmethod
    def get_all_active(): return [Prestamo._a_objeto(fila, tipo_join='activos') for fila in database.obtener_prestamos_activos_db()]

    @staticmethod
    def get_active_by_libro_id(libro_id): return Prestamo._a_objeto(database.obtener_prestamo_activo_por_libro_id_db(libro_id), tipo_join='activo_por_libro')

    @staticmethod
    def get_historial_by_usuario_id(usuario_id):
        filas = database.obtener_prestamos_por_usuario_id_db(usuario_id)
        return [Prestamo._a_objeto(fila, tipo_join='historial_usuario', usuario_id_contexto=usuario_id) for fila in filas]

class Biblioteca:
    def __init__(self, db_path="librotrack.db"):
        self.db_path = db_path

    def agregar_libro(self, titulo, autor, genero):
        libro_nuevo = Libro(id_libro=None, titulo=titulo, autor=autor, genero=genero)
        if libro_nuevo.save_to_db(): return libro_nuevo
        return None

    def registrar_usuario(self, ci, nombre, telefono):
        usuario_nuevo = Usuario(id_usuario=None, ci=ci, nombre=nombre, telefono=telefono)
        if usuario_nuevo.save_to_db(): return usuario_nuevo
        return None

    def listar_usuarios(self):
        return Usuario.get_all()

    def realizar_prestamo(self, libro_id, usuario_id, fecha_prestamo=None):
        if fecha_prestamo is None: fecha_prestamo = datetime.date.today().isoformat()
        libro = Libro.get_by_id(libro_id)
        if not libro: print(f"Error: Libro ID {libro_id} no encontrado."); return None
        if not libro.disponible: print(f"Error: Libro '{libro.titulo}' (ID: {libro_id}) no disponible."); return None
        usuario = Usuario.get_by_id(usuario_id)
        if not usuario: print(f"Error: Usuario ID {usuario_id} no encontrado."); return None
        prestamo_nuevo = Prestamo(id_prestamo=None, libro_id=libro_id, usuario_id=usuario_id, fecha_prestamo=fecha_prestamo)
        if prestamo_nuevo.save_to_db(): return prestamo_nuevo
        return None

    def registrar_devolucion(self, libro_id, fecha_devolucion=None):
        if fecha_devolucion is None: fecha_devolucion = datetime.date.today().isoformat()
        prestamo_activo = Prestamo.get_active_by_libro_id(libro_id)
        if not prestamo_activo or prestamo_activo.id_prestamo is None :
            libro = Libro.get_by_id(libro_id)
            titulo_libro = libro.titulo if libro else f"ID {libro_id}"
            if libro and libro.disponible: print(f"Info: El libro '{titulo_libro}' ya figura como disponible.")
            else: print(f"Info: No se encontró préstamo activo para '{titulo_libro}'.")
            return False
        if prestamo_activo.marcar_como_devuelto(fecha_devolucion): return True
        return False

    def buscar_libros(self, termino, tipo_busqueda):
        return Libro.search(termino, tipo_busqueda)

    def listar_libros(self):
        return Libro.get_all()

    def listar_prestamos_activos(self):
        return Prestamo.get_all_active()

    def eliminar_libro(self, libro_id):
        libro_a_eliminar = Libro.get_by_id(libro_id)
        if libro_a_eliminar: return libro_a_eliminar.delete_from_db()
        return False

    def eliminar_usuario(self, usuario_id):
        usuario_a_eliminar = Usuario.get_by_id(usuario_id)
        if usuario_a_eliminar: return usuario_a_eliminar.delete_from_db()
        return False

    def listar_historial_prestamos_usuario(self, usuario_id):
        return Prestamo.get_historial_by_usuario_id(usuario_id)

    def buscar_usuarios(self, termino, criterio): 
        """Busca usuarios por CI o Nombre a través de la clase Usuario."""
        return Usuario.search(termino, criterio)
