from typing import Optional

class Nodo:
    """Clase que representa un nodo en el grid para el algoritmo A*."""
    
    def __init__(self, x: int, y: int, padre: Optional['Nodo'] = None):
        self.x: int = x
        self.y: int = y
        self.padre: Optional['Nodo'] = padre
        
        # Costos variables
        self.g: float = 0.0  # Costo desde el inicio
        self.h: float = 0.0  # Heurística (distancia estimada a la meta)
        self.f: float = 0.0  # Costo total (g + h)
        
    def __lt__(self, otro: 'Nodo') -> bool:
        """
        Sobrescribe el operador Menor Que (<).
        Compara nodos por su valor f (costo total) para que 
        heapq (min-heap) los ordene correctamente priorizando el menor costo.
        """
        return self.f < otro.f

    def __eq__(self, otro: object) -> bool:
        """Compara si dos nodos representan la misma posición."""
        if not isinstance(otro, Nodo):
            return False
        return self.x == otro.x and self.y == otro.y
        
    @property
    def posicion(self) -> tuple[int, int]:
        """Retorna la posición del nodo como tupla (x, y)."""
        return (self.x, self.y)
