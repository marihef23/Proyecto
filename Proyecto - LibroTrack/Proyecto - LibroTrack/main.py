import database
from gui import MainWindow # Importar la clase MainWindow de gui.py
# Ya no necesitamos importar Biblioteca, Libro, Usuario, Prestamo directamente aquí
# a menos que queramos hacer alguna operación antes o después de la GUI.

def main():
    print("Iniciando LibroTrack...")

    # Asegurar que la base de datos y las tablas estén creadas
    # Esto es importante hacerlo antes de que la GUI intente acceder a la BD.
    database.crear_tablas()
    print("Base de datos verificada/creada.")

    # Crear e iniciar la aplicación GUI
    app = MainWindow()
    print("Lanzando interfaz gráfica...")
    app.mainloop()

    print("LibroTrack finalizado.")

if __name__ == "__main__":
    main()
