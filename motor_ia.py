import heapq
from typing import List, Tuple, Set, Dict
from nodo import Nodo

def heuristica_manhattan(x1: int, y1: int, x2: int, y2: int) -> float:
    """Calcula la estricta distancia Manhattan entre dos puntos."""
    return float(abs(x1 - x2) + abs(y1 - y2))

def obtener_vecinos(actual: Nodo, ancho: int, alto: int, paredes: Set[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Obtiene vecinos válidos (arriba, abajo, izquierda, derecha) que no sean paredes."""
    vecinos_validos = []
    # Movimientos permitidos: Arriba, Abajo, Izquierda, Derecha. Costo de paso = 1.
    direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    
    for dx, dy in direcciones:
        nx, ny = actual.x + dx, actual.y + dy
        # Verificar que el vecino esté dentro de los límites del mapa
        if 0 <= nx < ancho and 0 <= ny < alto:
            if (nx, ny) not in paredes:
                vecinos_validos.append((nx, ny))
                
    return vecinos_validos

def resolver_a_estrella(inicio_pos: Tuple[int, int], meta_pos: Tuple[int, int], 
                        ancho: int, alto: int, paredes: Set[Tuple[int, int]]) -> Tuple[List[Tuple[int, int]], Set[Tuple[int, int]]]:
    """
    Ejecuta el algoritmo A* para encontrar la ruta más corta.
    Retorna:
      - Lista de posiciones que componen la ruta final (desde el inicio hasta la meta).
      - Conjunto de tuplas con los nodos explorados (lista cerrada) para la visualización gráfica.
    """
    nodo_inicio = Nodo(inicio_pos[0], inicio_pos[1])
    nodo_meta = Nodo(meta_pos[0], meta_pos[1])
    
    # Lista Abierta (Frontera) usando min-heapq
    lista_abierta: List[Nodo] = []
    heapq.heappush(lista_abierta, nodo_inicio)
    
    # Lista Cerrada estricta, como Set O(1)
    lista_cerrada: Set[Tuple[int, int]] = set()
    
    # Hash map para almacenar el costo G más eficiente conocido hacia un nodo particular
    costos_g: Dict[Tuple[int, int], float] = {inicio_pos: 0.0}
    
    while lista_abierta:
        # Extraemos el nodo con el menor F
        nodo_actual = heapq.heappop(lista_abierta)
        pos_actual = nodo_actual.posicion
        
        # Si llegamos a la meta, reconstruimos y retornamos la ruta
        if pos_actual == meta_pos:
            ruta = []
            actual = nodo_actual
            while actual is not None:
                ruta.append(actual.posicion)
                actual = actual.padre
            return ruta[::-1], lista_cerrada
            
        # Añadir la posición al Set de cerrados para evitar reexploración O(1)
        lista_cerrada.add(pos_actual)
        
        # Exploración de nodos adyacentes
        for nx, ny in obtener_vecinos(nodo_actual, ancho, alto, paredes):
            vecino_pos = (nx, ny)
            
            # Si el vecino ya está cerrado, lo ignoramos
            if vecino_pos in lista_cerrada:
                continue
                
            nuevo_costo_g = nodo_actual.g + 1.0  # Debido a que moverse en grid vale 1
            
            # Considerar el vecino solo si encontramos un trayecto mejor o si no había sido evaluado
            if vecino_pos not in costos_g or nuevo_costo_g < costos_g[vecino_pos]:
                costos_g[vecino_pos] = nuevo_costo_g
                
                # Instanciar el vecino configurando métricas matemáticas
                vecino_nodo = Nodo(nx, ny, nodo_actual)
                vecino_nodo.g = nuevo_costo_g
                vecino_nodo.h = heuristica_manhattan(nx, ny, meta_pos[0], meta_pos[1])
                vecino_nodo.f = vecino_nodo.g + vecino_nodo.h
                
                heapq.heappush(lista_abierta, vecino_nodo)
                
    # Retorna listas vacías en caso de no hallar ruta
    return [], lista_cerrada
