import sys
import tabulate
from App import logic as lg
from DataStructures.List import array_list as al
def new_logic():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función de la lógica donde se crean las estructuras de datos
    pass

def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def load_data(control):
    """
    Carga los datos
    """
    data = lg.load_data()
    #TODO: Realizar la carga de datos
    pass


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    puntos_migratorios = input("Punto migratorio de origen, definido por ser el nodo más cercano a la locación GPS especificada por el usuario (latitud-longitud): ")
    puntos_llegada = (input("Punto migratorio de destino, definido por ser el nodo más cercano a la locación GPS especificada por el usuario (latitud-longitud).: "))
    
    answer = lg.req_1(control,puntos_migratorios,puntos_llegada )
    print("\n=== RESULTADO REQ 1 ===")

    resumen = [
    ["Primer nodo encontrado", f"{answer['time_ms']}"],
    ["Distancia total", answer["filtered_number"]],
    ["Total de puntos", answer["filtered_number"]]
]
    print(tabulate(resumen, headers=["Descripción", "Valor"], tablefmt="grid"))

    first = []
    first_list = answer["first5"]

    for i in range(al.size(first_list)):
        flight = al.get_element(first_list, i)
        first.append([
            flight["id"],
            flight["flight"],
            flight["date"],
            flight["airline_name"],
            flight["airline_code"],
            flight["origin"],
            flight["dest"],
            flight["delay_minutes"],
        ])

    titulo_first = f"Primeros {len(first)} vertices encontrados"
    print(f"\n============ {titulo_first} ============\n")

    print(
        tabulate(
            first,
            headers=[
                "ID vuelo",
                "Código vuelo",
                "Fecha",
                "Aerolínea",
                "Carrier",
                "Origen",
                "Destino",
                "Retraso (min)"
        ],
            tablefmt="grid",
            showindex=range(1, len(first) + 1)
    )
)


    if "last5" in answer:
        last = []
        last_list = answer["last5"]

        for i in range(al.size(last_list)):
            flight = al.get_element(last_list, i)
            last.append([
                flight["id"],
                flight["flight"],
                flight["date"],
                flight["airline_name"],
                flight["airline_code"],
                flight["origin"],
                flight["dest"],
                flight["delay_minutes"],
        ])

    titulo_last = f"Últimos {len(last)} vertices encontrados"
    print(f"\n============ {titulo_last} ============\n")

    print(
        tabulate(
            last,
            headers=[
                "ID vuelo",
                "Código vuelo",
                "Fecha",
                "Aerolínea",
                "Carrier",
                "Origen",
                "Destino",
                "Retraso (min)"
            ],
            tablefmt="grid",
            showindex=range(1, len(last) + 1)
        )
    )
    
    
    
    # TODO: Imprimir el resultado del requerimiento 1
    pass


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    puntos_migratorios = input("Punto migratorio de origen, definido por ser el nodo más cercano a la locación GPS especificada por el usuario (latitud-longitud): ")
    puntos_llegada = (input("Punto migratorio de destino, definido por ser el nodo más cercano a la locación GPS especificada por el usuario (latitud-longitud).: "))
    radio =  int(input("Radio del área de interés en km (desde el punto de origen: "))
    answer = lg.req_2(control,puntos_migratorios,puntos_llegada,radio)
    print("\n=== RESULTADO REQ 2 ===")
    resumen = [
    ["Ultimo nodo encontrado", f"{answer['time_ms']}"],
    ["Distancia total", answer["filtered_number"]],],
    ["Total de puntos", answer["filtered_number"]]
    print(tabulate(resumen, headers=["Descripción", "Valor"], tablefmt="grid"))

    first = []
    for i in range(answer["first5"]["size"]):
        flight = al.get_element(answer["first5"], i)
        first.append([
        flight["id"],
        flight["flight"],
        flight["date"],
        flight["airline_name"],
        flight["airline_code"],
        flight["origin"],
        flight["dest"],
        flight["early_minutes"],
    ])

    titulo_first = f"Primeros {len(first)} nodos encontrados"
    print(f"\n============ {titulo_first} ============")

    print(tabulate(
        first,
        headers=[
        "ID vuelo", "Código vuelo", "Fecha",
        "Aerolínea", "Carrier", "Origen",
        "Destino", "Distancia (mi)"
        ],
        tablefmt="grid",
        showindex=range(1, len(first) + 1)
))

    last = []
    for i in range(answer["last5"]["size"]):
        flight = al.get_element(answer["last5"], i)
        last.append([
        flight["id"],
        flight["flight"],
        flight["date"],
        flight["airline_name"],
        flight["airline_code"],
        flight["origin"],
        flight["dest"],
        flight["early_minutes"],
    ])

    titulo_last = f"Últimos {len(last)} nodos encontrados"
    print(f"\n============ {titulo_last} ============")

    print(tabulate(
        last,
        headers=[
        "ID vuelo", "Código vuelo", "Fecha",
        "Aerolínea", "Carrier", "Origen",
        "Destino", "Distancia (mi)"
        ],
        tablefmt="grid",
        showindex=range(1, len(last) + 1)
))
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    answer = lg.req_3(control)
    print("\n=== RESULTADO REQ 3 ===")
    resumen = [
    ["Total de puntos", f"{answer['time']}"],
    ["Total de individuos encontrados", answer["total_flights"]],
]
    print(tabulate(resumen, headers=["Descripción", "Valor"], tablefmt="grid"))

    first = []
    for i in range(answer["first"]["size"]):
        flight = al.get_element(answer["first"], i)
        first.append([
        flight["id"],
        flight["flight"],
        flight["date"],
        flight["airline_name"],
        flight["airline_code"],
        flight["origin"],
        flight["dest"],
        flight["distance"],
    ])

    titulo_first = f"Primeros {len(first)} nodos encontrados"
    print(f"\n============ {titulo_first} ============")
    print(
        tabulate(
        first,
        headers=[
            "ID vuelo",
            "Código vuelo",
            "Fecha",
            "Aerolínea",
            "Carrier",
            "Origen",
            "Destino",
            "Distancia (mi)",
        ],
        tablefmt="grid",
        showindex=range(1, len(first) + 1)
    )
)

    last = []
    for i in range(answer["last"]["size"]):
        flight = al.get_element(answer["last"], i)
        last.append([
        flight["id"],
        flight["flight"],
        flight["date"],
        flight["airline_name"],
        flight["airline_code"],
        flight["origin"],
        flight["dest"],
        flight["distance"],
    ])

    titulo_last = f"Últimos {len(last)} nodos encontrados"
    print(f"\n============ {titulo_last} ============")
    print(
    tabulate(
        last,
        headers=[
            "ID vuelo",
            "Código vuelo",
            "Fecha",
            "Aerolínea",
            "Carrier",
            "Origen",
            "Destino",
            "Distancia (mi)",
        ],
        tablefmt="grid",
        showindex=range(1, len(last) + 1)
    )
)
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    puntos_migratorios = input("Punto migratorio de origen, definido por ser el nodo más cercano a la locación GPS especificada por el usuario (latitud-longitud): ")
    answer = lg.req_4(control,puntos_migratorios)
    print("\n=== RESULTADO REQ 4 ===")

    resumen = [
    ["Total de puntos", f"{answer['time']}"],
    ["Total de individuos encontrados", answer["total_flights"]],
    ["Total de distancia", answer["total_flights"]]
]
    print(tabulate(resumen, headers=["Descripción", "Valor"], tablefmt="grid"))

    first = []
    for i in range(answer["first"]["size"]):
        flight = al.get_element(answer["first"], i)
        first.append([
        flight["id"],
        flight["flight"],
        flight["date"],
        flight["airline_name"],
        flight["airline_code"],
        flight["origin"],
        flight["dest"],
        flight["distance"],
    ])

    titulo_first = f"Primeros {len(first)} nodos encontrados"
    print(f"\n============ {titulo_first} ============")
    print(
        tabulate(
        first,
        headers=[
            "ID vuelo",
            "Código vuelo",
            "Fecha",
            "Aerolínea",
            "Carrier",
            "Origen",
            "Destino",
            "Distancia (mi)",
        ],
        tablefmt="grid",
        showindex=range(1, len(first) + 1)
    )
)

    last = []
    for i in range(answer["last"]["size"]):
        flight = al.get_element(answer["last"], i)
        last.append([
        flight["id"],
        flight["flight"],
        flight["date"],
        flight["airline_name"],
        flight["airline_code"],
        flight["origin"],
        flight["dest"],
        flight["distance"],
    ])

    titulo_last = f"Últimos {len(last)} nodos encontrados"
    print(f"\n============ {titulo_last} ============")
    print(
    tabulate(
        last,
        headers=[
            "ID vuelo",
            "Código vuelo",
            "Fecha",
            "Aerolínea",
            "Carrier",
            "Origen",
            "Destino",
            "Distancia (mi)",
        ],
        tablefmt="grid",
        showindex=range(1, len(last) + 1)
    )
)
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    puntos_migratorios = input("Punto migratorio de origen, definido por ser el nodo más cercano a la locación GPS especificada por el usuario (latitud-longitud): ")
    puntos_llegada = (input("Punto migratorio de destino, definido por ser el nodo más cercano a la locación GPS especificada por el usuario (latitud-longitud).: "))
    grafo = input("Selección entre el grafo por distancia de desplazamiento o el grafo por distancias a fuentes hídrica: ")
    answer = lg.req_4(control,puntos_migratorios,puntos_llegada,grafo)
    
    print("\n=== RESULTADO REQ 4 ===")

    resumen = [
    ["El costo total que tomará el individuo en distancia", f"{answer['time']}"],
    ["El total de puntos que contiene el camino", answer["total_flights"]],
    ["El total de segmentos que conforman la ruta identificad", answer["total_flights"]]
]
    print(tabulate(resumen, headers=["Descripción", "Valor"], tablefmt="grid"))

    first = []
    for i in range(answer["first"]["size"]):
        flight = al.get_element(answer["first"], i)
        first.append([
        flight["id"],
        flight["flight"],
        flight["date"],
        flight["airline_name"],
        flight["airline_code"],
        flight["origin"],
        flight["dest"],
        flight["distance"],
    ])

    titulo_first = f"Primeros {len(first)} nodos encontrados"
    print(f"\n============ {titulo_first} ============")
    print(
        tabulate(
        first,
        headers=[
            "ID vuelo",
            "Código vuelo",
            "Fecha",
            "Aerolínea",
            "Carrier",
            "Origen",
            "Destino",
            "Distancia (mi)",
        ],
        tablefmt="grid",
        showindex=range(1, len(first) + 1)
    )
)

    last = []
    for i in range(answer["last"]["size"]):
        flight = al.get_element(answer["last"], i)
        last.append([
        flight["id"],
        flight["flight"],
        flight["date"],
        flight["airline_name"],
        flight["airline_code"],
        flight["origin"],
        flight["dest"],
        flight["distance"],
    ])

    titulo_last = f"Últimos {len(last)} nodos encontrados"
    print(f"\n============ {titulo_last} ============")
    print(
    tabulate(
        last,
        headers=[
            "ID vuelo",
            "Código vuelo",
            "Fecha",
            "Aerolínea",
            "Carrier",
            "Origen",
            "Destino",
            "Distancia (mi)",
        ],
        tablefmt="grid",
        showindex=range(1, len(last) + 1)
    )
)
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    answer = lg.req_3(control)
    print("\n=== RESULTADO REQ 3 ===")
    resumen = [
    ["El total de subredes hídricas identificadas en el nicho biológico", f"{answer['time']}"],
]
    print(tabulate(resumen, headers=["Descripción", "Valor"], tablefmt="grid"))

    first = []
    for i in range(answer["first"]["size"]):
        flight = al.get_element(answer["first"], i)
        first.append([
        flight["id"],
        flight["flight"],
        flight["date"],
        flight["airline_name"],
        flight["airline_code"],
        flight["origin"],
        flight["dest"],
        flight["distance"],
    ])

    titulo_first = f"Primeros {len(first)} nodos encontrados"
    print(f"\n============ {titulo_first} ============")
    print(
        tabulate(
        first,
        headers=[
            "ID vuelo",
            "Código vuelo",
            "Fecha",
            "Aerolínea",
            "Carrier",
            "Origen",
            "Destino",
            "Distancia (mi)",
        ],
        tablefmt="grid",
        showindex=range(1, len(first) + 1)
    )
)

    last = []
    for i in range(answer["last"]["size"]):
        flight = al.get_element(answer["last"], i)
        last.append([
        flight["id"],
        flight["flight"],
        flight["date"],
        flight["airline_name"],
        flight["airline_code"],
        flight["origin"],
        flight["dest"],
        flight["distance"],
    ])

    titulo_last = f"Últimos {len(last)} nodos encontrados"
    print(f"\n============ {titulo_last} ============")
    print(
    tabulate(
        last,
        headers=[
            "ID vuelo",
            "Código vuelo",
            "Fecha",
            "Aerolínea",
            "Carrier",
            "Origen",
            "Destino",
            "Distancia (mi)",
        ],
        tablefmt="grid",
        showindex=range(1, len(last) + 1)
    )
)
    # TODO: Imprimir el resultado del requerimiento 6
    pass

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 5:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
