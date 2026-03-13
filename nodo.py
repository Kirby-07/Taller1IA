from typing import Optional

class Nodo:
    """Clase que representa un nodo en el grid para el algoritmo A*."""
    
    def __init__(self, x: int, y: int, padre: Optional['Nodo'] = None):
        self.x: int = x
        self.y: int = y
        self.padre: Optional['Nodo'] = padre # Camino que va dejando al recorrer los nodos, si se hace una similitud a hansel y gretel, es como dejar migajas de pan en el camino
        
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

    """ En python existen los dunder methods que son métodos que al tener una estructura tipo __init__ o __lt__ , etc. 
    es una simplificación de una operación matemática como comparar donde se ejecuta por debajo gracias a su tipado de alto nivel
    Algo similar en Java sería: public boolean equals(Object obj) { ... } que sería una función para comparar 2 objetos """
    def __eq__(self, otro: object) -> bool:
        """Compara si dos nodos representan la misma posición."""
        if not isinstance(otro, Nodo):
            return False
        return self.x == otro.x and self.y == otro.y
        
    # Getter
    @property
    def posicion(self) -> tuple[int, int]:
        """Retorna la posición del nodo como tupla (x, y)."""
        return (self.x, self.y)
