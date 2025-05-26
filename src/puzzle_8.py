import random # Importa el módulo random para generar números aleatorios (usado para barajar el puzzle).
import heapq # Importa el módulo heapq, que implementa el algoritmo de cola de prioridad (usado en A*).
import pygame # Importa el módulo pygame para la creación de la interfaz gráfica de usuario (GUI).
import time # Importa el módulo time para medir el tiempo de ejecución de los algoritmos de búsqueda.
from collections import deque # Importa deque (cola de doble extremo) del módulo collections (usado para BFS, aunque aquí se utiliza una lista como pila para DFS).

# Realizado por: Alanys Silva
# --- Clase para representar un nodo en la búsqueda (para DFS/BFS) ---
class Nodo:
    def __init__(self, estado, padre=None):
        # El estado debe ser una tupla de tuplas para ser inmutable y hashable
        # Convierte el estado de entrada a una tupla de tuplas. Esto es crucial
        # porque las tuplas son inmutables y pueden ser usadas como claves en diccionarios
        # o elementos en conjuntos (sets), lo cual es necesario para `visitados`.
        self.estado = tuple(map(tuple, estado))
        self.padre = padre  # Almacena el nodo padre para reconstruir el camino una vez que se encuentra la solución.

# --- Clase para representar un nodo en A* ---
class NodoAStar:
    def __init__(self, estado, padre=None, costo=0):
        self.estado = tuple(map(tuple, estado)) # Convierte el estado a tupla de tuplas para hacerlo inmutable y hashable.
        self.padre = padre # Almacena el nodo padre para reconstruir el camino.
        self.costo = costo  # Costo acumulado desde el nodo inicial hasta este nodo (g_cost).
        # Calcula la heurística (costo estimado desde este nodo hasta el nodo meta)
        # utilizando la distancia de Manhattan.
        self.heuristica = self.calcular_distancia_manhattan(estado)  # Heurística (h_cost)
        self.f = self.costo + self.heuristica  # Costo total (f_cost = g_cost + h_cost), usado para la prioridad en A*.

    def __lt__(self, other):
        # Este método permite comparar dos objetos NodoAStar.
        # Es esencial para que `heapq` (cola de prioridad) sepa cómo ordenar los nodos.
        # Compara los nodos basándose en su atributo `f` (costo total).
        return self.f < other.f

    def __eq__(self, other):
        # Este método define cómo se verifica la igualdad entre dos objetos NodoAStar.
        # Es importante para verificar si un nodo ya ha sido visitado o está en la cola.
        # Dos nodos son iguales si sus estados son iguales.
        return self.estado == other.estado

    def __hash__(self):
        # Este método hace que los objetos NodoAStar sean "hashable", lo que significa
        # que pueden ser usados como claves en diccionarios o como elementos en conjuntos (`set`).
        # El hash se basa en el estado del nodo.
        return hash(self.estado)

    def calcular_distancia_manhattan(self, estado_actual):
        distancia = 0
    
        # Este diccionario almacena la posición (fila, columna) ideal para cada número
        # en el estado meta. El 0 representa el espacio vacío.
        meta_positions = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            8: (1, 0), 0: (1, 1), 4: (1, 2), # 0 es el espacio vacío
            7: (2, 0), 6: (2, 1), 5: (2, 2)
        }

        # Itera sobre cada celda del estado actual (puzzle 3x3).
        for r in range(3):
            for c in range(3):
                valor = estado_actual[r][c] # Obtiene el valor de la celda actual.
                if valor != 0: # Si el valor no es el espacio vacío (0).
                    # Obtiene la posición objetivo (meta) para el valor actual.
                    target_row, target_col = meta_positions[valor]
                    # Calcula la distancia de Manhattan para este valor:
                    # |fila_actual - fila_objetivo| + |columna_actual - columna_objetivo|.
                    # Suma esta distancia a la distancia total.
                    distancia += abs(r - target_row) + abs(c - target_col)
        return distancia # Retorna la suma total de las distancias de Manhattan para todos los números.

# --- Funciones Auxiliares ---

# Función para verificar si el estado es el estado meta
def es_estado_meta(estado):
   
    meta = ((1, 2, 3), (8, 0, 4), (7, 6, 5)) # Define el estado meta como una tupla de tuplas.
    return estado == meta # Retorna True si el estado actual es igual al estado meta, False en caso contrario.

# Función para obtener los movimientos posibles
def obtener_movimientos(estado):
    movimientos = [] # Inicializa una lista vacía para almacenar los nuevos estados posibles.
    fila_vacia, col_vacia = -1, -1 # Inicializa las coordenadas del espacio vacío.
    # Encuentra la posición (fila, columna) del espacio vacío (0).
    for r in range(3):
        for c in range(3):
            if estado[r][c] == 0:
                fila_vacia, col_vacia = r, c
                break # Sale del bucle interior una vez encontrado el espacio vacío.
        if fila_vacia != -1:
            break # Sale del bucle exterior.

    # Define las posibles direcciones de movimiento: arriba, abajo, izquierda, derecha.
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)] # dr (cambio en fila), dc (cambio en columna).
    for dr, dc in direcciones: # Itera sobre cada dirección.
        nueva_fila = fila_vacia + dr # Calcula la nueva fila para el movimiento.
        nueva_col = col_vacia + dc # Calcula la nueva columna para el movimiento.

        # Verifica si el nuevo movimiento está dentro de los límites del tablero (3x3).
        if 0 <= nueva_fila < 3 and 0 <= nueva_col < 3:
            # Crea una copia mutable del estado actual para realizar el intercambio.
            nuevo_estado_list = [list(fila) for fila in estado]
            # Intercambia el espacio vacío con el valor de la nueva posición.
            nuevo_estado_list[fila_vacia][col_vacia], nuevo_estado_list[nueva_fila][nueva_col] = \
                nuevo_estado_list[nueva_fila][nueva_col], nuevo_estado_list[fila_vacia][col_vacia]
            # Convierte el nuevo estado (lista de listas) a una tupla de tuplas y lo añade a la lista de movimientos.
            movimientos.append(tuple(map(tuple, nuevo_estado_list)))
    return movimientos # Retorna la lista de todos los estados posibles después de un movimiento.

# Función para verificar si el estado es resoluble
def es_resoluble(estado):
    inversions = 0 # Contador de inversiones.
    # Aplanar la lista y eliminar el 0 para el cálculo de inversiones.
    # Un "aplanado" significa convertir la matriz 3x3 en una lista simple.
    # Se excluye el 0 porque no participa en el cálculo de inversiones.
    flat_list = [num for row in estado for num in row if num != 0]

    # Calcula el número de inversiones. Una inversión ocurre cuando un número mayor
    # precede a un número menor en la secuencia aplanada.
    for i in range(len(flat_list)):
        for j in range(i + 1, len(flat_list)):
            if flat_list[i] > flat_list[j]:
                inversions += 1

    # Para un puzzle 8 (3x3), la resolubilidad depende de la paridad de las inversiones.
    # Si el número de inversiones del estado inicial tiene la misma paridad que el número de inversiones
    # del estado meta, entonces es resoluble.
    # El estado meta deseado ([1,2,3],[8,0,4],[7,6,5]) tiene 7 inversiones (impar).
    # Por lo tanto, un puzzle inicial solo tiene solución si su número de inversiones también es impar.
    return inversions % 2 != 0 # Retorna True si el número de inversiones es impar, False si es par.

# Función para generar un estado inicial aleatorio resoluble
def generar_estado_aleatorio():

    # estado meta aquí también para evitar generarlo como estado inicial.
    meta = ((1, 2, 3), (8, 0, 4), (7, 6, 5)) # Define el estado meta para la comprobación.
    while True: # Bucle infinito hasta que se genere un estado válido.
        estado_plano = list(range(9)) # Crea una lista de números del 0 al 8.
        random.shuffle(estado_plano) # Baraja aleatoriamente los números en la lista.
        # Convierte la lista plana en una tupla de tuplas 3x3.
        estado_2d = tuple(tuple(estado_plano[i:i + 3]) for i in range(0, 9, 3))

        # Verificar si es resoluble para el estado meta y si es diferente de él.
        # Si el estado generado es resoluble y no es el estado meta, se retorna.
        if es_resoluble(estado_2d) and estado_2d != meta:
            return estado_2d

# --- Algoritmos de Búsqueda ---

# Implementación de Búsqueda en Profundidad (DFS)
def busqueda_profundidad(estado_inicial):
    pila = [Nodo(estado_inicial)] # Crea una pila (lista) y añade el nodo inicial. DFS usa una pila (LIFO).
    visitados = set() # Un conjunto para almacenar los estados ya visitados y evitar ciclos.
    nodos_expandidos = 0 # Contador para el número de nodos expandidos.

    while pila: # Mientras la pila no esté vacía.
        nodo_actual = pila.pop() # Saca el nodo superior de la pila (LIFO).

        if es_estado_meta(nodo_actual.estado): # Si el estado del nodo actual es el estado meta.
            return nodo_actual, nodos_expandidos # Retorna el nodo meta y el número de nodos expandidos.

        if nodo_actual.estado not in visitados: # Si el estado actual no ha sido visitado.
            visitados.add(nodo_actual.estado) # Añade el estado actual al conjunto de visitados.
            nodos_expandidos += 1 # Incrementa el contador de nodos expandidos.

            # Genera sucesores en orden inverso para explorar el "primer" hijo primero.
            # DFS explora un camino tan profundo como sea posible antes de retroceder.
            # Al invertir el orden de los movimientos, se asegura una exploración consistente.
            for estado_hijo in reversed(obtener_movimientos(nodo_actual.estado)):
                if estado_hijo not in visitados: # Si el estado hijo no ha sido visitado.
                    hijo = Nodo(estado_hijo, nodo_actual) # Crea un nuevo nodo hijo con el padre actual.
                    pila.append(hijo) # Añade el nodo hijo a la pila.
    return None, nodos_expandidos # Si la pila se vacía y no se encuentra la solución, retorna None.

# Implementación de Búsqueda A* con distancia Manhattan
def busqueda_a_star(estado_inicial):
    cola_prioridad = [] # Inicializa una lista que actuará como cola de prioridad.
    # Añade el nodo inicial a la cola de prioridad.
    # heapq.heappush mantiene la propiedad del montículo (el elemento más pequeño está en la raíz).
    heapq.heappush(cola_prioridad, NodoAStar(estado_inicial, costo=0))

    visitados = set() # Conjunto para almacenar los estados ya procesados (cerrados).
    # Diccionario para almacenar el costo g_cost (costo real desde el inicio) para cada estado.
    g_scores = {estado_inicial: 0}
    nodos_expandidos = 0 # Contador para el número de nodos expandidos.

    while cola_prioridad: # Mientras la cola de prioridad no esté vacía.
        # Saca el nodo con el menor f_cost (costo total) de la cola de prioridad.
        nodo_actual = heapq.heappop(cola_prioridad)

        if nodo_actual.estado in visitados: # Si el nodo ya ha sido procesado, lo ignora.
            continue

        visitados.add(nodo_actual.estado) # Marca el nodo actual como visitado (cerrado).
        nodos_expandidos += 1 # Incrementa el contador de nodos expandidos.

        if es_estado_meta(nodo_actual.estado): # Si el estado del nodo actual es el estado meta.
            return nodo_actual, nodos_expandidos # Retorna el nodo meta y el número de nodos expandidos.

        # Itera sobre todos los movimientos posibles desde el estado actual.
        for estado_hijo in obtener_movimientos(nodo_actual.estado):
            # Calcula el costo acumulado para llegar al hijo desde el inicio (costo del padre + 1 movimiento).
            costo_hijo_desde_inicio = nodo_actual.costo + 1

            # Si el hijo no ha sido visitado antes, o si se encontró un camino más corto hacia él.
            if estado_hijo not in g_scores or costo_hijo_desde_inicio < g_scores[estado_hijo]:
                g_scores[estado_hijo] = costo_hijo_desde_inicio # Actualiza el g_score para el hijo.
                # Crea un nuevo nodo hijo con el padre, costo y heurística.
                hijo = NodoAStar(estado_hijo, nodo_actual, costo_hijo_desde_inicio)
                heapq.heappush(cola_prioridad, hijo) # Añade el hijo a la cola de prioridad.
    return None, nodos_expandidos # Si la cola de prioridad se vacía y no se encuentra la solución, retorna None.

# Función para reconstruir la solución
def reconstruir_solucion(nodo):
    camino = [] # Inicializa una lista vacía para almacenar los estados del camino.
    while nodo: # Mientras el nodo no sea None (es decir, mientras haya un padre).
        camino.append(nodo.estado) # Añade el estado del nodo actual al camino.
        nodo = nodo.padre # Retrocede al nodo padre.
    return camino[::-1] # Retorna el camino invertido para que empiece desde el estado inicial hasta el meta.

# --- Interfaz Gráfica Pygame (Sin cambios en esta sección, funciona con la nueva lógica) ---

def main():
    pygame.init() # Inicializa todos los módulos de Pygame.

    WIDTH, HEIGHT = 900, 650 # Define el ancho y alto de la ventana.
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Crea la ventana de visualización.
    pygame.display.set_caption("Puzzle 8 Solver") # Establece el título de la ventana.

    # Definición de colores RGB.
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    GREEN = (0, 200, 0)
    DARK_GREEN = (0, 150, 0)
    BLUE = (50, 50, 200)
    DARK_BLUE = (30, 30, 150)

    # Definición de fuentes para el texto.
    font_large = pygame.font.Font(None, 74) # Fuente grande para los números del puzzle.
    font_medium = pygame.font.Font(None, 40) # Fuente mediana para títulos y botones.
    font_small = pygame.font.Font(None, 30) # Fuente pequeña para estadísticas.

    estado_inicial = generar_estado_aleatorio() # Genera un estado inicial resoluble aleatorio.

    # Variables para almacenar los resultados de la solución.
    solucion_path = None # El camino de estados que lleva a la solución.
    movimientos = 0 # Número de movimientos en la solución.
    tiempo_ejecucion = 0.0 # Tiempo que tardó el algoritmo en resolver.
    nodos_expandidos = 0 # Número de nodos expandidos por el algoritmo.
    algoritmo_seleccionado = None # Almacena el algoritmo de búsqueda seleccionado ("DFS" o "A*").

    # Banderas para controlar el estado de la GUI.
    solving_in_progress = False # True si un algoritmo está en ejecución.
    solution_found_display = False # True si se ha encontrado una solución y se debe mostrar.

    # Definición de los botones para seleccionar algoritmos.
    buttons_alg = [
        {"rect": pygame.Rect(20, 20, 150, 50), "text": "DFS", "color": GRAY, "hover_color": (150, 150, 150), "value": "DFS"},
        {"rect": pygame.Rect(200, 20, 150, 50), "text": "A*", "color": GRAY, "hover_color": (150, 150, 150), "value": "A*"}
    ]
    # Definición de los botones "Empezar" y "Reset".
    start_button = {"rect": pygame.Rect(20, 90, 150, 50), "text": "Empezar", "color": GREEN, "hover_color": DARK_GREEN, "value": "START"}
    reset_button = {"rect": pygame.Rect(200, 90, 150, 50), "text": "Reset", "color": BLUE, "hover_color": DARK_BLUE, "value": "RESET"}

    # Función para dibujar un botón en la pantalla.
    def draw_button(screen, button_data, current_alg_selected=None):
        mouse_pos = pygame.mouse.get_pos() # Obtiene la posición actual del ratón.
        # Cambia el color del botón si el ratón está sobre él.
        current_color = button_data["hover_color"] if button_data["rect"].collidepoint(mouse_pos) else button_data["color"]

        # Si el botón es un selector de algoritmo y es el algoritmo seleccionado, dibuja un borde azul.
        if button_data["value"] == current_alg_selected:
            pygame.draw.rect(screen, BLUE, button_data["rect"].inflate(6, 6), 3, border_radius=10)

        # Dibuja el cuerpo del botón.
        pygame.draw.rect(screen, current_color, button_data["rect"], border_radius=10)
        # Renderiza el texto del botón.
        text_surf = font_medium.render(button_data["text"], True, BLACK)
        # Centra el texto dentro del botón.
        text_rect = text_surf.get_rect(center=button_data["rect"].center)
        screen.blit(text_surf, text_rect) # Dibuja el texto en la pantalla.

    # Función para dibujar la cuadrícula del puzzle.
    def dibujar_puzzle_grid(estado, screen, offset_x=0, offset_y=0, tile_size=100):
        TILE_SIZE = tile_size # Tamaño de cada celda (ficha) del puzzle.
        TILE_MARGIN = 5 # Margen entre celdas.

        for r in range(3): # Itera sobre las filas.
            for c in range(3): # Itera sobre las columnas.
                valor = estado[r][c] # Obtiene el valor de la celda.
                # Calcula la posición X e Y de la celda en la pantalla.
                rect_x = offset_x + c * (TILE_SIZE + TILE_MARGIN)
                rect_y = offset_y + r * (TILE_SIZE + TILE_MARGIN)

                if valor != 0: # Si la celda no es el espacio vacío.
                    # Dibuja el fondo de la celda con un color gris claro.
                    pygame.draw.rect(screen, (230, 230, 230), (rect_x, rect_y, TILE_SIZE, TILE_SIZE), border_radius=8)
                    # Dibuja el borde de la celda en negro.
                    pygame.draw.rect(screen, BLACK, (rect_x, rect_y, TILE_SIZE, TILE_SIZE), 2, border_radius=8)
                    # Renderiza el número de la celda.
                    text_surf = font_large.render(str(valor), True, BLACK)
                    # Centra el número dentro de la celda.
                    text_rect = text_surf.get_rect(center=(rect_x + TILE_SIZE // 2, rect_y + TILE_SIZE // 2))
                    screen.blit(text_surf, text_rect) # Dibuja el número en la pantalla.
                else: # Si la celda es el espacio vacío (0).
                    # Dibuja un rectángulo de color azul claro para el espacio vacío.
                    pygame.draw.rect(screen, (200, 220, 240), (rect_x, rect_y, TILE_SIZE, TILE_SIZE), border_radius=8)

    running = True # Bucle principal del juego.
    while running:
        for event in pygame.event.get(): # Procesa los eventos de Pygame.
            if event.type == pygame.QUIT: # Si el usuario cierra la ventana.
                running = False # Sale del bucle principal.

            if event.type == pygame.MOUSEBUTTONDOWN: # Si se hace clic con el ratón.
                mouse_x, mouse_y = event.pos # Obtiene las coordenadas del clic.

                for btn in buttons_alg: # Itera sobre los botones de selección de algoritmo.
                    if btn["rect"].collidepoint(mouse_x, mouse_y): # Si el clic fue en un botón de algoritmo.
                        algoritmo_seleccionado = btn["value"] # Establece el algoritmo seleccionado.
                        # Reinicia las variables de solución al cambiar de algoritmo.
                        solucion_path = None
                        movimientos = 0
                        tiempo_ejecucion = 0.0
                        nodos_expandidos = 0
                        solution_found_display = False

                # Si el clic fue en el botón "Empezar" y no hay una solución en progreso.
                if start_button["rect"].collidepoint(mouse_x, mouse_y) and not solving_in_progress:
                    if algoritmo_seleccionado: # Si se ha seleccionado un algoritmo.
                        solving_in_progress = True # Indica que la solución está en progreso.
                        # Reinicia las variables de solución.
                        solucion_path = None
                        movimientos = 0
                        tiempo_ejecucion = 0.0
                        nodos_expandidos = 0
                        solution_found_display = False

                        start_time = time.time() # Registra el tiempo de inicio de la ejecución.
                        found_node = None # Nodo encontrado que contiene la solución.
                        current_nodos_expandidos = 0 # Nodos expandidos durante la ejecución actual.

                        if algoritmo_seleccionado == "DFS":
                            print("Resolviendo con DFS...")
                            # Llama a la función de búsqueda en profundidad.
                            found_node, current_nodos_expandidos = busqueda_profundidad(estado_inicial)
                        elif algoritmo_seleccionado == "A*":
                            print("Resolviendo con A*...")
                            # Llama a la función de búsqueda A*.
                            found_node, current_nodos_expandidos = busqueda_a_star(estado_inicial)

                        end_time = time.time() # Registra el tiempo de finalización.
                        tiempo_ejecucion = end_time - start_time # Calcula el tiempo total de ejecución.
                        nodos_expandidos = current_nodos_expandidos # Actualiza el contador de nodos expandidos.

                        if found_node: # Si se encontró una solución.
                            solucion_path = reconstruir_solucion(found_node) # Reconstruye el camino.
                            # Calcula el número de movimientos (longitud del camino - 1).
                            movimientos = len(solucion_path) - 1 if solucion_path else 0
                            print(f"Solución encontrada en {movimientos} movimientos con {algoritmo_seleccionado}.")
                            print(f"Nodos expandidos: {nodos_expandidos}")
                            solution_found_display = True # Activa la bandera para mostrar la solución.
                        else: # Si no se encontró una solución.
                            print(f"No se encontró solución con {algoritmo_seleccionado}.")
                            print(f"Nodos expandidos: {nodos_expandidos}")
                            solucion_path = [] # La ruta de la solución está vacía.
                            movimientos = 0
                            solution_found_display = True # Activa la bandera para mostrar el mensaje de "no solución".

                        solving_in_progress = False # Indica que la solución ha terminado.

                # Si el clic fue en el botón "Reset" y no hay una solución en progreso.
                if reset_button["rect"].collidepoint(mouse_x, mouse_y) and not solving_in_progress:
                    estado_inicial = generar_estado_aleatorio() # Genera un nuevo estado inicial aleatorio.
                    # Reinicia todas las variables de solución y estado de la GUI.
                    solucion_path = None
                    movimientos = 0
                    tiempo_ejecucion = 0.0
                    nodos_expandidos = 0
                    algoritmo_seleccionado = None
                    solution_found_display = False
                    print("\nNuevo puzzle generado.")

        screen.fill(WHITE) # Rellena el fondo de la pantalla con blanco.

        for btn in buttons_alg: # Dibuja los botones de selección de algoritmo.
            draw_button(screen, btn, algoritmo_seleccionado)

        draw_button(screen, start_button) # Dibuja el botón "Empezar".
        draw_button(screen, reset_button) # Dibuja el botón "Reset".

        if algoritmo_seleccionado: # Si se ha seleccionado un algoritmo.
            # Muestra el nombre del algoritmo seleccionado.
            selected_alg_text = font_medium.render(f"Algoritmo: {algoritmo_seleccionado}", True, BLUE)
            screen.blit(selected_alg_text, (550, 60))

        # Define el tamaño y el espaciado para la visualización de los puzzles.
        PUZZLE_TILE_SIZE = 100
        TILE_MARGIN = 5
        PUZZLE_WIDTH = PUZZLE_TILE_SIZE * 3 + TILE_MARGIN * 2
        TOTAL_PUZZLE_AREA_WIDTH = PUZZLE_WIDTH * 2 + 100
        INITIAL_PUZZLE_OFFSET_X = (WIDTH - TOTAL_PUZZLE_AREA_WIDTH) // 2
        SOLVED_PUZZLE_OFFSET_X = INITIAL_PUZZLE_OFFSET_X + PUZZLE_WIDTH + 100
        PUZZLE_OFFSET_Y = 220

        initial_puzzle_text = font_medium.render("Puzzle Inicial:", True, BLACK) # Texto "Puzzle Inicial".
        screen.blit(initial_puzzle_text, (INITIAL_PUZZLE_OFFSET_X, PUZZLE_OFFSET_Y - 40)) # Dibuja el texto.
        # Dibuja la cuadrícula del puzzle inicial.
        dibujar_puzzle_grid(estado_inicial, screen, offset_x=INITIAL_PUZZLE_OFFSET_X, offset_y=PUZZLE_OFFSET_Y, tile_size=PUZZLE_TILE_SIZE)

        if solving_in_progress: # Si la solución está en progreso.
            solving_text = font_medium.render("Resolviendo...", True, (255, 0, 0)) # Muestra el texto "Resolviendo...".
            screen.blit(solving_text, (WIDTH // 2 - solving_text.get_width() // 2, HEIGHT - 60))
        elif solution_found_display: # Si se encontró o no se encontró una solución y se debe mostrar.
            resolved_puzzle_text = font_medium.render("Puzzle Resuelto:", True, BLACK) # Texto "Puzzle Resuelto".
            screen.blit(resolved_puzzle_text, (SOLVED_PUZZLE_OFFSET_X, PUZZLE_OFFSET_Y - 40))

            if solucion_path and len(solucion_path) > 0: # Si hay una solución encontrada.
                # Dibuja el estado final del puzzle resuelto.
                dibujar_puzzle_grid(solucion_path[-1], screen, offset_x=SOLVED_PUZZLE_OFFSET_X, offset_y=PUZZLE_OFFSET_Y, tile_size=PUZZLE_TILE_SIZE)
            else: # Si no se encontró solución.
                no_sol_text = font_medium.render("No se encontró solución", True, (255, 0, 0)) # Muestra el mensaje de "no solución".
                screen.blit(no_sol_text, (SOLVED_PUZZLE_OFFSET_X, PUZZLE_OFFSET_Y + 100))

            # Muestra las estadísticas de la solución: movimientos, tiempo y nodos expandidos.
            movimientos_text = font_small.render(f"Movimientos: {movimientos}", True, BLACK)
            screen.blit(movimientos_text, (SOLVED_PUZZLE_OFFSET_X, PUZZLE_OFFSET_Y + PUZZLE_TILE_SIZE * 3 + 20))

            tiempo_text = font_small.render(f"Tiempo: {tiempo_ejecucion:.4f} seg", True, BLACK)
            screen.blit(tiempo_text, (SOLVED_PUZZLE_OFFSET_X, PUZZLE_OFFSET_Y + PUZZLE_TILE_SIZE * 3 + 50))

            nodos_expandidos_text = font_small.render(f"Nodos Expandidos: {nodos_expandidos}", True, BLACK)
            screen.blit(nodos_expandidos_text, (SOLVED_PUZZLE_OFFSET_X, PUZZLE_OFFSET_Y + PUZZLE_TILE_SIZE * 3 + 80))

        pygame.display.flip() # Actualiza toda la pantalla para mostrar los cambios.
        pygame.time.Clock().tick(60) # Limita el bucle a un máximo de 60 fotogramas por segundo.

    pygame.quit() # Desinicializa todos los módulos de Pygame al salir del bucle principal.

if __name__ == "__main__":
    main() # Llama a la función principal cuando el script es ejecutado directamente.