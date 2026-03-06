from typing import Set, Tuple, List, Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QGraphicsView, QGraphicsScene, QGraphicsRectItem,
    QMessageBox
)
from PySide6.QtGui import QColor, QPen, QBrush, QMouseEvent, QPainter
from PySide6.QtCore import Qt

from motor_ia import resolver_a_estrella

# Constantes de colores (RGB)
COLOR_BLANCO = QColor(255, 255, 255)
COLOR_NEGRO = QColor(0, 0, 0)
COLOR_VERDE = QColor(0, 255, 0)
COLOR_ROJO = QColor(255, 0, 0)
COLOR_AZUL = QColor(0, 0, 255)
COLOR_GRIS = QColor(200, 200, 200)

class Celda(QGraphicsRectItem):
    """Representa una celda interactiva del mapa."""
    def __init__(self, x: int, y: int, size: int):
        super().__init__(x * size, y * size, size, size)
        self.grid_x: int = x
        self.grid_y: int = y
        self.setPen(QPen(Qt.black))
        self.setBrush(QBrush(COLOR_BLANCO))

class VistaGrid(QGraphicsView):
    """Vista de PySide6 para gestionar la interacción del cursor."""
    def __init__(self, scene: QGraphicsScene, parent: 'VentanaPrincipal'):
        super().__init__(scene)
        self.ventana = parent
        self.setRenderHint(QPainter.Antialiasing)
        
    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.pos())
        item = self.scene().itemAt(pos, self.transform())
        
        if isinstance(item, Celda):
            # Lógica de clicks
            if event.button() == Qt.LeftButton:
                if event.modifiers() & Qt.ShiftModifier:
                    # Alternativa a clic central: Shift + Clic Izquierdo -> Meta
                    self.ventana.set_meta(item.grid_x, item.grid_y)
                else:
                    self.ventana.toggle_pared(item.grid_x, item.grid_y)
            elif event.button() == Qt.RightButton:
                self.ventana.set_inicio(item.grid_x, item.grid_y)
            elif event.button() == Qt.MiddleButton:
                self.ventana.set_meta(item.grid_x, item.grid_y)
                
        super().mousePressEvent(event)

class VentanaPrincipal(QWidget):
    """Clase principal de UI que integra la separación del motor."""
    def __init__(self, ancho: int = 20, alto: int = 20, tamaño_celda: int = 25):
        super().__init__()
        self.ancho_grid: int = ancho
        self.alto_grid: int = alto
        self.tamaño_celda: int = tamaño_celda
        
        self.inicio_pos: Optional[Tuple[int, int]] = None
        self.meta_pos: Optional[Tuple[int, int]] = None
        self.paredes: Set[Tuple[int, int]] = set()
        self.celdas: List[List[Celda]] = []
        
        self.init_ui()
        
    def init_ui(self) -> None:
        self.setWindowTitle("Visualizador A*")
        self.layout_principal = QVBoxLayout()
        
        # Engine de dibujo
        self.escena = QGraphicsScene()
        self.vista = VistaGrid(self.escena, self)
        self.layout_principal.addWidget(self.vista)
        
        # Generar las celdas
        for y in range(self.alto_grid):
            fila = []
            for x in range(self.ancho_grid):
                celda = Celda(x, y, self.tamaño_celda)
                self.escena.addItem(celda)
                fila.append(celda)
            self.celdas.append(fila)
            
        # UI controls
        self.layout_botones = QHBoxLayout()
        self.btn_resolver = QPushButton("Resolver (Ejecutar A*)")
        self.btn_limpiar = QPushButton("Limpiar Mapa")
        
        self.btn_resolver.clicked.connect(self.resolver)
        self.btn_limpiar.clicked.connect(self.limpiar_mapa)
        
        self.layout_botones.addWidget(self.btn_resolver)
        self.layout_botones.addWidget(self.btn_limpiar)
        
        self.layout_principal.addLayout(self.layout_botones)
        self.setLayout(self.layout_principal)
        self.resize(self.ancho_grid * self.tamaño_celda + 50, self.alto_grid * self.tamaño_celda + 100)
        
    def get_celda(self, x: int, y: int) -> Celda:
        return self.celdas[y][x]
        
    def actualizar_colores(self) -> None:
        """Renderiza todo el mapa basándose en el estado interno modificado por eventos o A*."""
        for y in range(self.alto_grid):
            for x in range(self.ancho_grid):
                pos = (x, y)
                celda = self.get_celda(x, y)
                
                if pos == self.inicio_pos:
                    celda.setBrush(QBrush(COLOR_VERDE))
                elif pos == self.meta_pos:
                    celda.setBrush(QBrush(COLOR_ROJO))
                elif pos in self.paredes:
                    celda.setBrush(QBrush(COLOR_NEGRO))
                else:
                    celda.setBrush(QBrush(COLOR_BLANCO))
                    
    def toggle_pared(self, x: int, y: int) -> None:
        pos = (x, y)
        if pos == self.inicio_pos or pos == self.meta_pos:
            return
            
        if pos in self.paredes:
            self.paredes.remove(pos)
        else:
            self.paredes.add(pos)
        self.actualizar_colores()
        
    def set_inicio(self, x: int, y: int) -> None:
        pos = (x, y)
        if pos in self.paredes:
            self.paredes.remove(pos)
        if pos == self.meta_pos:
            self.meta_pos = None
            
        self.inicio_pos = pos
        self.actualizar_colores()
        
    def set_meta(self, x: int, y: int) -> None:
        pos = (x, y)
        if pos in self.paredes:
            self.paredes.remove(pos)
        if pos == self.inicio_pos:
            self.inicio_pos = None
            
        self.meta_pos = pos
        self.actualizar_colores()
        
    def limpiar_mapa(self) -> None:
        self.inicio_pos = None
        self.meta_pos = None
        self.paredes.clear()
        self.actualizar_colores()
        
    def colorear_ruta_explorada(self, ruta: List[Tuple[int, int]], explorados: Set[Tuple[int, int]]) -> None:
        """Muestra de manera visual los análisis y los resultados expuestos por el IA."""
        self.actualizar_colores()
        
        for pos in explorados:
            if pos != self.inicio_pos and pos != self.meta_pos and pos not in self.paredes:
                self.get_celda(pos[0], pos[1]).setBrush(QBrush(COLOR_GRIS))
                
        for pos in ruta:
            if pos != self.inicio_pos and pos != self.meta_pos:
                self.get_celda(pos[0], pos[1]).setBrush(QBrush(COLOR_AZUL))
                
    def resolver(self) -> None:
        if not self.inicio_pos or not self.meta_pos:
            QMessageBox.warning(self, "Acción requerida", "Marque un punto Verde de Entrada (Click Derecho) y uno Rojo de Salida (Click Central o Shift+Click).")
            return
            
        ruta, explorados = resolver_a_estrella(
            self.inicio_pos, 
            self.meta_pos, 
            self.ancho_grid, 
            self.alto_grid, 
            self.paredes
        )
        
        if not ruta:
            QMessageBox.information(self, "Estancado", "El Motor de IA determinó que no existe camino a la meta.")
        
        self.colorear_ruta_explorada(ruta, explorados)
