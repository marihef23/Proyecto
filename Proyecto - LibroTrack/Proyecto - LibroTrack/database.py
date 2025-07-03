import sqlite3

DB_NAME = "librotrack.db"

def obtener_conexion_db():
    """Establece conexión con la base de datos SQLite y habilita las claves foráneas."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def crear_tablas():
    """Crea las tablas de la base de datos si no existen."""
    conn = None
    try:
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            genero TEXT,
            disponible BOOLEAN DEFAULT TRUE
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ci TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            telefono TEXT
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            libro_id INTEGER NOT NULL,
            usuario_id INTEGER NOT NULL,
            fecha_prestamo TEXT NOT NULL,
            fecha_devolucion TEXT,
            FOREIGN KEY (libro_id) REFERENCES Libros(id) ON DELETE CASCADE,
            FOREIGN KEY (usuario_id) REFERENCES Usuarios(id) ON DELETE CASCADE
        );
        """)
        conn.commit()
        # print("Tablas verificadas/creadas exitosamente.") # Comentado para no ser muy verboso
    except sqlite3.Error as e:
        print(f"Error al crear las tablas: {e}")
    finally:
        if conn:
            conn.close()

# --- Funciones CRUD para Libros ---

def agregar_libro_db(titulo, autor, genero):
    """Agrega un nuevo libro a la base de datos."""
    conn = None
    try:
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Libros (titulo, autor, genero, disponible) VALUES (?, ?, ?, ?)",
                       (titulo, autor, genero, True)) # Por defecto disponible es True
        conn.commit()
        return cursor.lastrowid # Retorna el ID del libro insertado
    except sqlite3.Error as e:
        print(f"Error al agregar libro: {e}")
        return None
    finally:
        if conn:
            conn.close()

def obtener_libros_db():
    """Obtiene todos los libros de la base de datos."""
    conn = None
    try:
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, autor, genero, disponible FROM Libros ORDER BY titulo")
        filas = cursor.fetchall()
        # Convertiremos estas filas a objetos Libro en model.py
        return filas
    except sqlite3.Error as e:
        print(f"Error al obtener libros: {e}")
        return []
    finally:
        if conn:
            conn.close()

def actualizar_libro_db(id_libro, titulo, autor, genero, disponible):
    """Actualiza la información de un libro existente en la base de datos."""
    conn = None
    try:
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Libros 
            SET titulo = ?, autor = ?, genero = ?, disponible = ?
            WHERE id = ?
        """, (titulo, autor, genero, disponible, id_libro))
        conn.commit()
        return cursor.rowcount > 0 # Retorna True si la actualización fue exitosa
    except sqlite3.Error as e:
        print(f"Error al actualizar libro: {e}")
        return False
    finally:
        if conn:
            conn.close()

def eliminar_libro_db(id_libro):
    """Elimina un libro de la base de datos."""
    conn = None
    try:
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Libros WHERE id = ?", (id_libro,))
        conn.commit()
        return cursor.rowcount > 0 # Retorna True si la eliminación fue exitosa
    except sqlite3.Error as e:
        print(f"Error al eliminar libro: {e}")
        return False
    finally:
        if conn:
            conn.close()

def obtener_libro_por_id_db(id_libro):
    """Obtiene un libro específico por su ID."""
    conn = None
    try:
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, autor, genero, disponible FROM Libros WHERE id = ?", (id_libro,))
        fila = cursor.fetchone()
        return fila # Se convertirá a objeto Libro en model.py
    except sqlite3.Error as e:
        print(f"Error al obtener libro por ID: {e}")
        return None
    finally:
        if conn:
            conn.close()

def buscar_libros_db(termino_busqueda, tipo_busqueda):
    """Busca libros por título, autor o género."""
    conn = None
    if tipo_busqueda not in ["titulo", "autor", "genero"]:
        print("Tipo de búsqueda no válido.")
        return []
    
    query = f"SELECT id, titulo, autor, genero, disponible FROM Libros WHERE {tipo_busqueda} LIKE ? ORDER BY titulo"
    param = f"%{termino_busqueda}%"
    
    try:
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        cursor.execute(query, (param,))
        filas = cursor.fetchall()
        return filas # Se convertirán a objetos Libro en model.py
    except sqlite3.Error as e:
        print(f"Error al buscar libros: {e}")
        return []
    finally:
        if conn:
            conn.close()

# --- Funciones CRUD para Usuarios ---

def agregar_usuario_db(ci, nombre, telefono):
    """Agrega un nuevo usuario a la base de datos."""
    conn = None
    try:
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Usuarios (ci, nombre, telefono) VALUES (?, ?, ?)",
                       (ci, nombre, telefono))
        conn.commit()
        return cursor.lastrowid # Retorna el ID del usuario insertado
    except sqlite3.Error as e:
        print(f"Error al agregar usuario '{nombre}' (CI: {ci}): {e}")
        return None
    finally:
        if conn:
            conn.close()

def obtener_usuarios_db():
    """Obtiene todos los usuarios de la base de datos."""
    conn = None
    try:
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, ci, nombre, telefono FROM Usuarios ORDER BY nombre")
        filas = cursor.fetchall()
        # Se convertirán a objetos Usuario en model.py
        return filas
    except sqlite3.Error as e:
        print(f"Error al obtener usuarios: {e}")
        return []
    finally:
        if conn:
            conn.close()

def actualizar_usuario_db(id_usuario, ci, nombre, telefono):
    """Actualiza la información de un usuario existente en la base de datos."""
    conn = None
    try:
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Usuarios 
            SET ci = ?, nombre = ?, telefono = ?
            WHERE id = ?
        """, (ci, nombre, telefono, id_usuario))
        conn.commit()
        return cursor.rowcount > 0 # Retorna True si la actualización fue exitosa
    except sqlite3.Error as e:
        print(f"Error al actualizar usuario ID {id_usuario}: {e}")
        return False
    finally:
        if conn:
            conn.close()

def eliminar_usuario_db(id_usuario):
    """Elimina un usuario de la base de datos."""
    conn = None
    try:
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Usuarios WHERE id = ?", (id_usuario,))
        conn.commit()
        return cursor.rowcount > 0 # Retorna True si la eliminación fue exitosa
    except sqlite3.Error as e:
        print(f"Error al eliminar usuario: {e}")
        return False
    finally:
        if conn:
            conn.close()

def obtener_usuario_por_id_db(id_usuario):
    """Obtiene un usuario específico por su ID."""
    conn = None
    try:
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, ci, nombre, telefono FROM Usuarios WHERE id = ?", (id_usuario,))
        fila = cursor.fetchone()
        # Se convertirá a objeto Usuario en model.py
        return fila
    except sqlite3.Error as e:
        print(f"Error al obtener usuario por ID {id_usuario}: {e}")
        return None
    finally:
        if conn:
            conn.close()

# --- Funciones para Préstamos ---

def registrar_prestamo_db(libro_id, usuario_id, fecha_prestamo):
    """Registra un nuevo préstamo en la base de datos y actualiza la disponibilidad del libro."""
    conn = None
    try:
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        # Registrar el préstamo
        cursor.execute("INSERT INTO Prestamos (libro_id, usuario_id, fecha_prestamo) VALUES (?, ?, ?)",
                       (libro_id, usuario_id, fecha_prestamo))
        prestamo_id = cursor.lastrowid
        
        # Actualizar disponibilidad del libro
        cursor.execute("UPDATE Libros SET disponible = 0 WHERE id = ?", (libro_id,)) # Usar 0 para FALSE
        
        conn.commit()
        return prestamo_id
    except sqlite3.Error as e:
        if conn:
            conn.rollback() # Revertir cambios si algo falla
        print(f"Error al registrar préstamo para libro ID {libro_id}: {e}")
        return None
    finally:
        if conn:
            conn.close()

def registrar_devolucion_db(prestamo_id, fecha_devolucion):
    """Registra la devolución de un préstamo y actualiza la disponibilidad del libro."""
    conn = None
    try:
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        
        # Obtener el libro_id del préstamo para actualizar su disponibilidad
        cursor.execute("SELECT libro_id FROM Prestamos WHERE id = ?", (prestamo_id,))
        fila = cursor.fetchone()
        if not fila:
            print(f"No se encontró el préstamo con ID {prestamo_id}.")
            return False
        libro_id = fila[0]
        
        # Actualizar fecha de devolución del préstamo
        cursor.execute("UPDATE Prestamos SET fecha_devolucion = ? WHERE id = ?",
                       (fecha_devolucion, prestamo_id))
        
        # Actualizar disponibilidad del libro
        cursor.execute("UPDATE Libros SET disponible = 1 WHERE id = ?", (libro_id,)) # Usar 1 para TRUE
        
        conn.commit()
        return True
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        print(f"Error al registrar devolución para préstamo ID {prestamo_id}: {e}")
        return False
    finally:
        if conn:
            conn.close()

def obtener_prestamos_activos_db():
    """Obtiene todos los préstamos activos (sin fecha de devolución)."""
    conn = None
    try:
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        # Seleccionar más información para mostrar (títulos de libros, nombres de usuarios)
        cursor.execute("""
            SELECT p.id, p.libro_id, l.titulo, p.usuario_id, u.nombre, p.fecha_prestamo
            FROM Prestamos p
            JOIN Libros l ON p.libro_id = l.id
            JOIN Usuarios u ON p.usuario_id = u.id
            WHERE p.fecha_devolucion IS NULL
            ORDER BY p.fecha_prestamo
        """)
        filas = cursor.fetchall()
        return filas # Se convertirán a objetos o tuplas informativas en model/GUI
    except sqlite3.Error as e:
        print(f"Error al obtener préstamos activos: {e}")
        return []
    finally:
        if conn:
            conn.close()

def obtener_todos_los_prestamos_db():
    """Obtiene todos los préstamos, activos e inactivos."""
    conn = None
    try:
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.libro_id, l.titulo, p.usuario_id, u.nombre, p.fecha_prestamo, p.fecha_devolucion
            FROM Prestamos p
            JOIN Libros l ON p.libro_id = l.id
            JOIN Usuarios u ON p.usuario_id = u.id
            ORDER BY p.fecha_prestamo DESC
        """)
        filas = cursor.fetchall()
        return filas
    except sqlite3.Error as e:
        print(f"Error al obtener todos los préstamos: {e}")
        return []
    finally:
        if conn:
            conn.close()

def obtener_prestamo_por_id_db(prestamo_id):
    """Obtiene un préstamo específico por su ID."""
    conn = None
    try:
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.libro_id, l.titulo, p.usuario_id, u.nombre, u.ci, p.fecha_prestamo, p.fecha_devolucion
            FROM Prestamos p
            JOIN Libros l ON p.libro_id = l.id
            JOIN Usuarios u ON p.usuario_id = u.id
            WHERE p.id = ?
        """, (prestamo_id,))
        fila = cursor.fetchone()
        return fila
    except sqlite3.Error as e:
        print(f"Error al obtener préstamo por ID {prestamo_id}: {e}")
        return None
    finally:
        if conn:
            conn.close()

def obtener_prestamo_activo_por_libro_id_db(libro_id):
    """Obtiene el préstamo activo para un libro específico, si existe."""
    conn = None
    try:
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.libro_id, p.usuario_id, p.fecha_prestamo, p.fecha_devolucion
            FROM Prestamos p
            WHERE p.libro_id = ? AND p.fecha_devolucion IS NULL
        """, (libro_id,))
        fila = cursor.fetchone() # Debería haber como máximo uno
        return fila
    except sqlite3.Error as e:
        print(f"Error al obtener préstamo activo por libro ID {libro_id}: {e}")
        return None
    finally:
        if conn:
            conn.close()

# Nueva función para historial de préstamos de un usuario
def obtener_prestamos_por_usuario_id_db(usuario_id):
    """Obtiene todos los préstamos (activos y devueltos) para un usuario específico."""
    conn = None
    try:
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.libro_id, l.titulo, p.fecha_prestamo, p.fecha_devolucion
            FROM Prestamos p
            JOIN Libros l ON p.libro_id = l.id
            WHERE p.usuario_id = ?
            ORDER BY p.fecha_prestamo DESC
        """, (usuario_id,))
        filas = cursor.fetchall()
        # La conversión a objetos Prestamo se hará en model.py
        return filas
    except sqlite3.Error as e:
        print(f"Error al obtener préstamos para el usuario ID {usuario_id}: {e}")
        return []
    finally:
        if conn:
            conn.close()

# Nueva función para buscar usuarios
def buscar_usuarios_db(termino_busqueda, criterio_busqueda):
    """Busca usuarios por CI o Nombre."""
    conn = None
    if criterio_busqueda not in ["ci", "nombre"]:
        print("Error: Criterio de búsqueda de usuario no válido.")
        return []
    
    # Asegurarse que la columna es segura para interpolar (evitar SQL injection aunque aquí es controlada)
    columna_segura = criterio_busqueda 
    
    query = f"SELECT id, ci, nombre, telefono FROM Usuarios WHERE {columna_segura} LIKE ? ORDER BY nombre"
    param = f"%{termino_busqueda}%"
    
    try:
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        cursor.execute(query, (param,))
        filas = cursor.fetchall()
        # La conversión a objetos Usuario se hará en model.py
        return filas
    except sqlite3.Error as e:
        print(f"Error al buscar usuarios por {criterio_busqueda} con término '{termino_busqueda}': {e}")
        return []
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    print("Inicializando la base de datos...")
    crear_tablas()
    print("Base de datos lista.")
    # Ejemplo de uso 
    # id_nuevo = agregar_libro_db("El Principito", "Antoine de Saint-Exupéry", "Infantil")
    # if id_nuevo:
    #     print(f"Libro agregado con ID: {id_nuevo}")
    #     libro = obtener_libro_por_id_db(id_nuevo)
    #     print(f"Libro obtenido: {libro}")
    #     actualizar_libro_db(id_nuevo, "El Principito", "Antoine de Saint-Exupéry", "Fábula", True)
    #     libro_actualizado = obtener_libro_por_id_db(id_nuevo)
    #     print(f"Libro actualizado: {libro_actualizado}")
    # libros = obtener_libros_db()
    # print(f"Todos los libros: {libros}")
    # busqueda = buscar_libros_db("Principito", "titulo")
    # print(f"Búsqueda: {busqueda}")
    # eliminar_libro_db(id_nuevo)
    # print(f"Libros después de eliminar: {obtener_libros_db()}")
