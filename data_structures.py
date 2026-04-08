"""
Estructuras de datos: Stack (LIFO), Queue (FIFO), HashTable (Ordered Dictionary).

"""

from __future__ import annotations
from typing import Any, Iterator


# Stack LIFO

class Stack:
    """
    Pila LIFO respaldada por una lista dinámica de Python.

    """

    def __init__(self) -> None:
        self._items: list[Any] = []


    def peek(self) -> Any:
        """Devuelve el elemento del tope sin removerlo."""
        if self.is_empty():
            raise IndexError("peek en stack vacío")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)


    def push(self, item: Any) -> None:
        """Agrega un elemento al tope."""
        self._items.append(item)

    def pop(self) -> Any:
        """Remueve y devuelve el elemento del tope."""
        if self.is_empty():
            raise IndexError("pop en stack vacío")
        return self._items.pop()

    def clear(self) -> None:
        """Vacía la pila."""
        self._items.clear()


    def __len__(self) -> int:
        return self.size()

    def __repr__(self) -> str:
        return f"Stack(top → {list(reversed(self._items))})"

    def __contains__(self, item: Any) -> bool:
        return item in self._items

    def __iter__(self) -> Iterator[Any]:
        """Itera del tope a la base (orden LIFO)."""
        return reversed(self._items)



# Queue FIFO

class _Node:
    """Nodo interno para la queue basada en lista enlazada."""
    __slots__ = ("value", "next")

    def __init__(self, value: Any) -> None:
        self.value = value
        self.next: _Node | None = None


class Queue:
    """
    Cola FIFO implementada con lista enlazada simple
    (head → front, tail → back)
    """

    def __init__(self) -> None:
        self._head: _Node | None = None
        self._tail: _Node | None = None
        self._size: int = 0


    def front(self) -> Any:
        """Devuelve el elemento al frente sin removerlo."""
        if self.is_empty():
            raise IndexError("front en queue vacía")
        return self._head.value  # type: ignore[union-attr]

    def is_empty(self) -> bool:
        return self._size == 0

    def size(self) -> int:
        return self._size


    def enqueue(self, item: Any) -> None:
        """Agrega un elemento al final de la cola."""
        node = _Node(item)
        if self._tail is not None:
            self._tail.next = node
        self._tail = node
        if self._head is None:
            self._head = node
        self._size += 1

    def dequeue(self) -> Any:
        """Remueve y devuelve el elemento del frente."""
        if self.is_empty():
            raise IndexError("dequeue en queue vacía")
        value = self._head.value  # type: ignore[union-attr]
        self._head = self._head.next  # type: ignore[union-attr]
        if self._head is None:
            self._tail = None
        self._size -= 1
        return value

    def clear(self) -> None:
        """Vacía la cola."""
        self._head = None
        self._tail = None
        self._size = 0


    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        items = list(self)
        return f"Queue(front → {items})"

    def __contains__(self, item: Any) -> bool:
        return any(v == item for v in self)

    def __iter__(self) -> Iterator[Any]:
        """Itera del frente al final."""
        current = self._head
        while current is not None:
            yield current.value
            current = current.next



# HashTable

class HashTable:
    """
    Tabla hash con resolución de colisiones por encadenamiento.
    Mantiene una lista enlazada por bucket + una lista de orden de inserción.


    """

    _INITIAL_CAPACITY = 16
    _LOAD_FACTOR_THRESHOLD = 0.75

    class _Entry:
        """Par clave-valor almacenado en cada bucket."""
        __slots__ = ("key", "value", "next")

        def __init__(self, key: Any, value: Any) -> None:
            self.key = key
            self.value = value
            self.next: HashTable._Entry | None = None

    def __init__(self) -> None:
        self._capacity: int = self._INITIAL_CAPACITY
        self._buckets: list[HashTable._Entry | None] = [None] * self._capacity
        self._size: int = 0
        self._order: list[Any] = []  


    def _hash(self, key: Any) -> int:
        return hash(key) % self._capacity

    def _resize(self) -> None:
        """Duplica la capacidad y reinserta todas las entradas."""
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [None] * self._capacity
        self._size = 0
        old_order = self._order[:]
        self._order.clear()

        for bucket in old_buckets:
            entry = bucket
            while entry is not None:
                self._put_internal(entry.key, entry.value)
                entry = entry.next


        self._order = old_order

    def _put_internal(self, key: Any, value: Any) -> None:
        """Inserción interna sin verificar resize ni orden."""
        idx = self._hash(key)
        entry = self._buckets[idx]
        while entry is not None:
            if entry.key == key:
                entry.value = value
                return
            entry = entry.next
        new_entry = self._Entry(key, value)
        new_entry.next = self._buckets[idx]
        self._buckets[idx] = new_entry
        self._size += 1


    def get(self, key: Any, default: Any = None) -> Any:
        """Obtiene el valor asociado a la clave, o *default* si no existe."""
        idx = self._hash(key)
        entry = self._buckets[idx]
        while entry is not None:
            if entry.key == key:
                return entry.value
            entry = entry.next
        return default

    def contains(self, key: Any) -> bool:
        """Verifica si la clave existe en la tabla."""
        return self.get(key, _SENTINEL) is not _SENTINEL

    def is_empty(self) -> bool:
        return self._size == 0

    def size(self) -> int:
        return self._size

    def keys(self) -> list[Any]:
        """Retorna las claves en orden de inserción."""
        return [k for k in self._order if self.contains(k)]

    def values(self) -> list[Any]:
        """Retorna los valores en orden de inserción."""
        return [self.get(k) for k in self.keys()]

    def items(self) -> list[tuple[Any, Any]]:
        """Retorna pares (clave, valor) en orden de inserción."""
        return [(k, self.get(k)) for k in self.keys()]


    def put(self, key: Any, value: Any) -> None:
        """Inserta o actualiza un par clave-valor."""
        if (self._size + 1) / self._capacity > self._LOAD_FACTOR_THRESHOLD:
            self._resize()

        existed = self.contains(key)
        self._put_internal(key, value)
        if not existed:
            self._order.append(key)

    def delete(self, key: Any) -> Any:
        """Elimina una clave y retorna su valor. Lanza KeyError si no existe."""
        idx = self._hash(key)
        entry = self._buckets[idx]
        prev: HashTable._Entry | None = None

        while entry is not None:
            if entry.key == key:
                if prev is None:
                    self._buckets[idx] = entry.next
                else:
                    prev.next = entry.next
                self._size -= 1
                self._order.remove(key)
                return entry.value
            prev = entry
            entry = entry.next

        raise KeyError(f"Clave no encontrada: {key!r}")

    def clear(self) -> None:
        """Vacía toda la tabla."""
        self._buckets = [None] * self._INITIAL_CAPACITY
        self._capacity = self._INITIAL_CAPACITY
        self._size = 0
        self._order.clear()


    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        pairs = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"HashTable({{{pairs}}})"

    def __contains__(self, key: Any) -> bool:
        return self.contains(key)

    def __getitem__(self, key: Any) -> Any:
        val = self.get(key, _SENTINEL)
        if val is _SENTINEL:
            raise KeyError(key)
        return val

    def __setitem__(self, key: Any, value: Any) -> None:
        self.put(key, value)

    def __delitem__(self, key: Any) -> None:
        self.delete(key)

    def __iter__(self) -> Iterator[Any]:
        """Itera las claves en orden de inserción."""
        return iter(self.keys())



_SENTINEL = object()
