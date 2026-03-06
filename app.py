import sys
from PySide6.QtWidgets import QApplication
from interfaz import VentanaPrincipal

def main() -> None:
    """Función de entrada para iniciar la aplicación A*."""
    app = QApplication(sys.argv)
    
    # Creamos el mapa por defecto de 20x20 celdas
    ventana = VentanaPrincipal(ancho=20, alto=20, tamaño_celda=30)
    ventana.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
