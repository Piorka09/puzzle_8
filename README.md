# 🧩 8-Puzzle Solver con Pygame (DFS y A*) 🚀

Este proyecto implementa un solucionador interactivo para el clásico juego del "8-Puzzle" utilizando los algoritmos de búsqueda no informada (DFS - Búsqueda en Profundidad) y búsqueda informada (A* - A-estrella). La interfaz gráfica de usuario (GUI) está desarrollada con `Pygame` para una visualización dinámica de la generación del puzzle, el estado inicial y la solución.

## ✨ Características

* **Generación de Puzzles Resolubles:** Genera automáticamente un estado inicial aleatorio que garantiza una solución para el estado meta definido.
* **Algoritmos de Búsqueda:**
    * **Búsqueda en Profundidad (DFS - Depth-First Search):** Explora los nodos de un árbol tan profundamente como sea posible antes de retroceder.
    * **A\* (A-star Search):** Un algoritmo de búsqueda de "mejor primero" que encuentra el camino de menor costo desde un nodo inicial hasta un nodo objetivo. Utiliza la **distancia de Manhattan** como función heurística.
* **Interfaz Gráfica de Usuario (GUI) con Pygame:**
    * Visualización clara del estado inicial y el estado resuelto del puzzle.
    * Botones intuitivos para seleccionar el algoritmo de búsqueda (DFS o A\*), iniciar la resolución y generar un nuevo puzzle.
    * Muestra en tiempo real estadísticas de la solución: número de movimientos, tiempo de ejecución y nodos expandidos.
* **Estado Meta Personalizado:** El puzzle busca resolver al siguiente estado:
    ```
    1 2 3
    8 0 4
    7 6 5
    ```

## 🛠️ Tecnologías Utilizadas

* **Python 3.x**
* **Pygame**: Para la interfaz gráfica.
* **`heapq`**: Para la implementación eficiente de la cola de prioridad en A*.
* **`random`**: Para la generación aleatoria de puzzles.

## 🚀 Cómo Ejecutar el Proyecto

Sigue estos pasos para poner en marcha el 8-Puzzle Solver en tu máquina local:

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/tu-proyecto-puzzle8.git](https://github.com/tu-usuario/tu-proyecto-puzzle8.git)
    cd tu-proyecto-puzzle8/src
    ```
    *(Asegúrate de reemplazar `tu-usuario` y `tu-proyecto-puzzle8` con los datos de tu repositorio.)*


2.  **Instala las dependencias:**
    ```bash
    pip install pygame
    ```

3.  **Ejecuta el script:**
    ```bash
    python puzzle8_solver.py
    ```



## 👤 Autor

* **Alanys Silva**
