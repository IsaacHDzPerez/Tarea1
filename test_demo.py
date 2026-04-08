"""
Programa demostración y pruebas para Stack, Queue y HashTable

Estructura:
    1 Tests unitarios
    2 Demo 
"""

from data_structures import Stack, Queue, HashTable



def test_stack():
    print("── Stack Tests ──")


    s = Stack()
    assert s.is_empty()
    assert s.size() == 0
    assert len(s) == 0
    print("  [✓] Stack vacío: is_empty, size, len")

    # Push y peek
    s.push(10)
    s.push(20)
    s.push(30)
    assert s.peek() == 30
    assert s.size() == 3
    print("  [✓] push + peek: tope correcto")

    # Pop en orden LIFO
    assert s.pop() == 30
    assert s.pop() == 20
    assert s.pop() == 10
    assert s.is_empty()
    print("  [✓] pop: orden LIFO correcto")

    # Error en pop/peek con stack vacío
    try:
        s.pop()
        assert False, "Debió lanzar IndexError"
    except IndexError:
        pass
    try:
        s.peek()
        assert False, "Debió lanzar IndexError"
    except IndexError:
        pass
    print("  [✓] Excepciones en pop/peek vacío")

    # contains e iter
    s.push("a")
    s.push("b")
    s.push("c")
    assert "b" in s
    assert "z" not in s
    assert list(s) == ["c", "b", "a"]  # LIFO
    print("  [✓] __contains__ e __iter__ (LIFO)")

    #  Clear
    s.clear()
    assert s.is_empty()
    print("  [✓] clear")

    #  Múltiples tipos de datos
    s.push(42)
    s.push("hello")
    s.push([1, 2, 3])
    s.push(None)
    assert s.pop() is None
    assert s.pop() == [1, 2, 3]
    print("  [✓] Múltiples tipos de datos")

    print("  ── Stack: TODOS LOS TESTS PASARON ──\n")


def test_queue():
    print("── Queue Tests ──")

    # Queue vacía
    q = Queue()
    assert q.is_empty()
    assert q.size() == 0
    print("  [✓] Queue vacía: is_empty, size")

    # Enqueue y front
    q.enqueue("A")
    q.enqueue("B")
    q.enqueue("C")
    assert q.front() == "A"
    assert q.size() == 3
    print("  [✓] enqueue + front: frente correcto")

    #Dequeue en orden FIFO
    assert q.dequeue() == "A"
    assert q.dequeue() == "B"
    assert q.dequeue() == "C"
    assert q.is_empty()
    print("  [✓] dequeue: orden FIFO correcto")

    #  Excepciones
    try:
        q.dequeue()
        assert False
    except IndexError:
        pass
    try:
        q.front()
        assert False
    except IndexError:
        pass
    print("  [✓] Excepciones en dequeue/front vacío")

    #Intercalado enqueue/dequeue
    q.enqueue(1)
    q.enqueue(2)
    assert q.dequeue() == 1
    q.enqueue(3)
    assert q.dequeue() == 2
    assert q.dequeue() == 3
    assert q.is_empty()
    print("  [✓] Intercalado enqueue/dequeue")

    # contains e iter
    q.enqueue(10)
    q.enqueue(20)
    q.enqueue(30)
    assert 20 in q
    assert 99 not in q
    assert list(q) == [10, 20, 30]
    print("  [✓] __contains__ e __iter__ (FIFO)")

    # Clear
    q.clear()
    assert q.is_empty()
    assert q.size() == 0
    print("  [✓] clear")

    # Volumen: 1000 elementos
    for i in range(1000):
        q.enqueue(i)
    assert q.size() == 1000
    assert q.dequeue() == 0
    assert q.front() == 1
    print("  [✓] Volumen: 1000 elementos")

    print("  ── Queue: TODOS LOS TESTS PASARON ──\n")


def test_hashtable():
    print("── HashTable Tests ──")

    #Tabla vacía
    ht = HashTable()
    assert ht.is_empty()
    assert ht.size() == 0
    print("  [✓] Tabla vacía: is_empty, size")

    # Put y get
    ht.put("nombre", "Isaac")
    ht.put("edad", 22)
    ht.put("carrera", "ITC")
    assert ht.get("nombre") == "Isaac"
    assert ht.get("edad") == 22
    assert ht.size() == 3
    print("  [✓] put + get")

    #Actualización de valor existente
    ht.put("edad", 23)
    assert ht.get("edad") == 23
    assert ht.size() == 3 
    print("  [✓] Actualización de clave existente")

    #get con default
    assert ht.get("telefono") is None
    assert ht.get("telefono", "N/A") == "N/A"
    print("  [✓] get con valor default")

    # contains
    assert ht.contains("nombre")
    assert not ht.contains("telefono")
    assert "carrera" in ht
    print("  [✓] contains / __contains__")

    # Operadores 
    ht["lenguaje"] = "Python"
    assert ht["lenguaje"] == "Python"
    del ht["lenguaje"]
    assert not ht.contains("lenguaje")
    print("  [✓] Operadores __getitem__, __setitem__, __delitem__")

    #  KeyError en acceso inexistente
    try:
        _ = ht["no_existe"]
        assert False
    except KeyError:
        pass
    print("  [✓] KeyError en clave inexistente")

    #Delete
    ht.put("temp", 999)
    val = ht.delete("temp")
    assert val == 999
    assert not ht.contains("temp")
    try:
        ht.delete("temp")
        assert False
    except KeyError:
        pass
    print("  [✓] delete + KeyError en delete inexistente")

    #Orden de inserción preservado
    ht2 = HashTable()
    keys_in = ["z", "a", "m", "b", "x"]
    for k in keys_in:
        ht2.put(k, k.upper())
    assert ht2.keys() == keys_in
    assert ht2.values() == [k.upper() for k in keys_in]
    assert ht2.items() == [(k, k.upper()) for k in keys_in]
    print("  [✓] Orden de inserción preservado (keys, values, items)")

    # Iteración
    assert list(ht2) == keys_in
    print("  [✓] __iter__ en orden de inserción")

    #Resize automático (más de 12 elementos con capacidad inicial 16)
    ht3 = HashTable()
    for i in range(50):
        ht3.put(f"key_{i}", i)
    assert ht3.size() == 50
    for i in range(50):
        assert ht3.get(f"key_{i}") == i
    print("  [✓] Resize automático: 50 elementos, integridad conservada")

    # Clear
    ht3.clear()
    assert ht3.is_empty()
    assert ht3.keys() == []
    print("  [✓] clear")

    #Claves de distintos tipos
    ht4 = HashTable()
    ht4.put(1, "int")
    ht4.put(3.14, "float")
    ht4.put((1, 2), "tuple")
    ht4.put(True, "bool")  
    assert ht4.get(1) == "bool"
    assert ht4.get(3.14) == "float"
    assert ht4.get((1, 2)) == "tuple"
    print("  [✓] Claves de distintos tipos hashables")


    ht5 = HashTable()
    # En CPython, hash(0) = 0 y hash(16) = 16, pero mod 16 ambos van al bucket 0
    ht5.put(0, "cero")
    ht5.put(16, "dieciséis")
    assert ht5.get(0) == "cero"
    assert ht5.get(16) == "dieciséis"
    print("  [✓] Manejo de colisiones (separate chaining)")

    print("  ── HashTable: TODOS LOS TESTS PASARON ──\n")



#  DEMO 

def demo():
    print("=" * 56)
    print("  DEMO: Uso práctico de las estructuras de datos")
    print("=" * 56)


    print("\n📚 Stack — Simulación de Undo en un editor")
    undo_stack = Stack()
    actions = ["Escribir 'Hola'", "Negrita", "Cambiar fuente", "Insertar imagen"]
    for action in actions:
        undo_stack.push(action)
        print(f"   Acción: {action}")

    print(f"   Estado: {undo_stack}")
    print(f"   Undo → {undo_stack.pop()}")
    print(f"   Undo → {undo_stack.pop()}")
    print(f"   Estado: {undo_stack}")


    print("\n🖨️  Queue — Cola de impresión")
    print_queue = Queue()
    docs = ["Reporte_Q1.pdf", "Factura_042.pdf", "Contrato.docx"]
    for doc in docs:
        print_queue.enqueue(doc)
        print(f"   En cola: {doc}")

    print(f"   Estado: {print_queue}")
    while not print_queue.is_empty():
        print(f"   Imprimiendo → {print_queue.dequeue()}")
    print(f"   Cola vacía: {print_queue.is_empty()}")


    print("\n📖 HashTable — Catálogo de productos")
    catalogo = HashTable()
    productos = [
        ("SKU-001", {"nombre": "Laptop", "precio": 15999.00}),
        ("SKU-002", {"nombre": "Mouse", "precio": 349.50}),
        ("SKU-003", {"nombre": "Monitor", "precio": 5899.00}),
        ("SKU-004", {"nombre": "Teclado", "precio": 899.00}),
    ]
    for sku, info in productos:
        catalogo.put(sku, info)

    print(f"   Productos registrados: {catalogo.size()}")
    print(f"   Buscar SKU-002: {catalogo.get('SKU-002')}")
    print(f"   ¿Existe SKU-005? {catalogo.contains('SKU-005')}")

    # Actualizar precio
    catalogo["SKU-002"] = {"nombre": "Mouse Ergonómico", "precio": 499.00}
    print(f"   SKU-002 actualizado: {catalogo['SKU-002']}")

    # Eliminar producto
    eliminado = catalogo.delete("SKU-004")
    print(f"   Eliminado SKU-004: {eliminado}")
    print(f"   Claves restantes: {catalogo.keys()}")
    print(f"   Estado: {catalogo}")

#  MAIN

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════╗")
    print("║  Tarea #1 — Estructuras de Datos (Compiladores)     ║")
    print("║  Stack (LIFO) · Queue (FIFO) · HashTable (Ordered)  ║")
    print("╚══════════════════════════════════════════════════════╝\n")

    test_stack()
    test_queue()
    test_hashtable()

    print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE\n")

    demo()
