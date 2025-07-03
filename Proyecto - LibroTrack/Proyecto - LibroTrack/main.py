import database
from gui import MainWindow 

def main():
    print("Iniciando LibroTrack...")

    # Asegurar que la base de datos y las tablas estén creadas
    
    database.crear_tablas()
    print("Base de datos verificada/creada.")

    # Crear e iniciar la aplicación GUI
    app = MainWindow()
    print("Lanzando interfaz gráfica...")
    app.mainloop()

    print("LibroTrack finalizado.")

if __name__ == "__main__":
    main()
