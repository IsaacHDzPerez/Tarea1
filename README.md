Implementación en Python desde cero de tres estructuras básicas sin usar librerías externas:

Stack (LIFO): pila con lista dinámica, operaciones push, pop, peek, clear en O(1) amortizado.
Queue (FIFO): cola con lista enlazada (head/tail) para enqueue y dequeue en O(1) real.
HashTable (Ordered): tabla hash con separate chaining, mantiene orden de inserción y hace resize automático al 75% de carga.

Archivos:

data_structures.py: contiene las tres clases.
test_demo.py: 28 tests + demo.

Tests cubren casos normales, errores, iteración, tipos mixtos, volumen y colisiones.

Tecnología: Python 3.10+ sin dependencias.
