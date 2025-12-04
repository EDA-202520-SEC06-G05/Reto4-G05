import sys
import tabulate
from App import logic as lg
from DataStructures.List import array_list as al


def new_logic():
    """
        Se crea una instancia del controlador
    """
    data = lg.new_logic()
    return data 
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
    data = lg.load_data(control)
    print(data)
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
    ["Primer nodo encontrado", f"{answer['mensaje']}"],
    ["Distancia total", answer["distancia_total"]],
    ["Total de puntos", answer["total_puntos"]]
]
    print(tabulate(resumen, headers=["Descripción", "Valor"], tablefmt="grid"))

    first = []
    first_list = answer["detalle"]

    for i in range(al.size(first_list)):
        flight = al.get_element(first_list, i)
        first.append([
            flight["nombre"],
            flight["lat"],
            flight["lon"],
            flight["n_individuos"],
            flight["primeros_3"],
            flight["u3"],
            flight["dest"],
            flight["dist_sig"],
        ])

    titulo_first = f"Primeros {len(first)} vertices encontrados"
    print(f"\n============ {titulo_first} ============\n")

    print(
        tabulate(
            first,
            headers=[
                "nombre",
                "lat",
                "lon",
                "n_individuos",
                "primeros_3",
                "ultimos3",
                "dest",
                "dist_sig"
        ],
            tablefmt="grid",
            showindex=range(1, len(first) + 1)
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
    ["Mensaje ", f"{answer['mensaje']}"],
    ["Ultimo nodo encontrado", f"{answer['ultimo_dentro_radio']}"],
    ["Distancia total", answer["distancia_total"]],],
    ["Total de puntos", answer["total_puntos"]]
    print(tabulate(resumen, headers=["Descripción", "Valor"], tablefmt="grid"))

    first = []
    for i in range(answer["ruta"]["size"]):
        flight = al.get_element(answer["ruta"], i)
        first.append([flight
    ])

    titulo_first = f"Primeros {len(first)} nodos encontrados"
    print(f"\n============ {titulo_first} ============")

    print(tabulate(
        first,
        headers=["Camino"
        ],
        tablefmt="grid",
        showindex=range(1, len(first) + 1)
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
    ["Total de puntos", f"{answer['vertices']}"],
    ["Total de individuos encontrados", answer["pajaros"]],
]
    print(tabulate(resumen, headers=["Descripción", "Valor"], tablefmt="grid"))

    first = []
    for i in range(answer["fisrt"]["size"]):
        flight = al.get_element(answer["fisrt"], i)
        first.append([
        flight["id"],
        flight["lon"],
        flight["lan"],
        flight["pajaros"],
        flight["first"],
        flight["last"],
        flight["dest"],
        flight["adyacentes"],
    ])

    titulo_first = f"Primeros {len(first)} nodos encontrados"
    print(f"\n============ {titulo_first} ============")
    print(
        tabulate(
        first,
        headers=[
            "id",
            "lon",
            "lan",
            "pajaros",
            "first",
            "last",
            "dest",
            "adyacentes",
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
        flight["lon"],
        flight["lan"],
        flight["pajaros"],
        flight["first"],
        flight["last"],
        flight["dest"],
        flight["adyacentes"],
    ])

    titulo_last = f"Últimos {len(last)} nodos encontrados"
    print(f"\n============ {titulo_last} ============")
    print(
    tabulate(
        last,
        headers=[
            "id",
            "lon",
            "lan",
            "pajaros",
            "first",
            "last",
            "dest",
            "adyacentes",
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
    ["Total de puntos", f"{answer['total_vertice']}"],
    ["Total de individuos encontrados", answer["total_individuos"]],
    ["Total de distancia", answer["distancia_total"]]
]
    print(tabulate(resumen, headers=["Descripción", "Valor"], tablefmt="grid"))

    first = []
    for i in range(answer["primeros_5"]["size"]):
        flight = al.get_element(answer["primeros_5"], i)
        first.append([
        flight["id"],
        flight["lon"],
        flight["lat"],
        flight["num_pajaros"],
        flight["first_tags"],
        flight["last_tags"],
    ])

    titulo_first = f"Primeros {len(first)} nodos encontrados"
    print(f"\n============ {titulo_first} ============")
    print(
        tabulate(
        first,
        headers=[
            "ID",
            "lon",
            "lat",
            "num_pajaros",
            "first_tags",
            "last_tags",
        ],
        tablefmt="grid",
        showindex=range(1, len(first) + 1)
    )
)

    last = []
    for i in range(answer["ultimos_5"]["size"]):
        flight = al.get_element(answer["ultimos_5"], i)
        last.append([
        flight["id"],
        flight["lon"],
        flight["lat"],
        flight["num_pajaros"],
        flight["first_tags"],
        flight["last_tags"],
    ])

    titulo_last = f"Últimos {len(last)} nodos encontrados"
    print(f"\n============ {titulo_last} ============")
    print(
    tabulate(
        last,
        headers=[
            "ID",
            "lon",
            "lat",
            "num_pajaros",
            "first_tags",
            "last_tags",
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
    ["Ruta optima encontrada", f"{answer['mensaje']}"],
    ["El costo total que tomará el individuo en distancia", f"{answer['cost']}"],
    ["El total de puntos que contiene el camino", answer["total_points"]],
    ["El total de segmentos que conforman la ruta identificad", answer["total_segments"]],
    ["Ruta identificada", answer["full_route"]]
]
    print(tabulate(resumen, headers=["Descripción", "Valor"], tablefmt="grid"))

    first = []
    for i in range(answer["first_nodes"]["size"]):
        flight = al.get_element(answer["first_nodes"], i)
        first.append([
        flight["id"],
        flight["lat"],
        flight["lon"],
        flight["num_grullas"],
        flight["first3"],
        flight["last3"],
        flight["events"],
        flight["dnext"],
    ])

    titulo_first = f"Primeros {len(first)} nodos encontrados"
    print(f"\n============ {titulo_first} ============")
    print(
        tabulate(
        first,
        headers=[
            "ID",
            "lat",
            "lon",
            "num_grullas",
            "first3",
            "last3",
            "events",
            "dnext",
        ],
        tablefmt="grid",
        showindex=range(1, len(first) + 1)
    )
)

    last = []
    for i in range(answer["last_nodes"]["size"]):
        flight = al.get_element(answer["last_nodes"], i)
        last.append([
        flight["id"],
        flight["lat"],
        flight["lon"],
        flight["num_grullas"],
        flight["first3"],
        flight["last3"],
        flight["events"],
        flight["dnext"],
    ])

    titulo_last = f"Últimos {len(last)} nodos encontrados"
    print(f"\n============ {titulo_last} ============")
    print(
    tabulate(
        last,
        headers=[
            "ID",
            "lat",
            "lon",
            "num_grullas",
            "first3",
            "last3",
            "events",
            "dnext",
        ],
        tablefmt="grid",
        showindex=range(1, len(last) + 1)
    )
)
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    answer = lg.req_6(control)

    if answer["subredes"] is None or answer["total_subredes"] == 0:
        print("\n=== RESULTADO REQ 6 ===")
        print("No se identificaron subredes hídricas")
        return

    total_subredes = answer["total_subredes"]
    top_subredes = answer["top_subredes"]

    print("\n=== RESULTADO REQ 6 ===")
    print(f"Total de subredes identificadas: {total_subredes}\n")

    resumen = []
    i = 1
    while i <= al.size(top_subredes):
        sub = al.get_element(top_subredes, i)
        resumen.append([
            sub["subred_id"],
            sub["total_puntos"],
            sub["total_individuos"],
            sub["min_lat"],
            sub["max_lat"],
            sub["min_lon"],
            sub["max_lon"]
        ])
        i += 1

    print(tabulate(
        resumen,
        headers=[
            "ID Subred",
            "Total puntos",
            "Total individuos",
            "Lat mínima",
            "Lat máxima",
            "Lon mínima",
            "Lon máxima"
        ],
        tablefmt="grid",
        showindex=range(1, len(resumen) + 1)
    ))

    i = 1
    while i <= al.size(top_subredes):
        sub = al.get_element(top_subredes, i)
        print(f"\n=== Detalle de la subred {sub['subred_id']} ===")
        puntos = sub["puntos"]

        detalle = []
        j = 1
        while j <= al.size(puntos):
            p = al.get_element(puntos, j)

            primeros3 = p["primeros_3"]
            ultimos3 = p["ultimos_3"]

            prim = []
            k = 1
            while k <= al.size(primeros3):
                prim.append(al.get_element(primeros3, k))
                k += 1

            ult = []
            k = 1
            while k <= al.size(ultimos3):
                ult.append(al.get_element(ultimos3, k))
                k += 1

            detalle.append([
                p["nid"],
                p["lat"],
                p["lon"],
                p["n_individuos"],
                ", ".join(str(x) for x in prim) if prim else "Unknown",
                ", ".join(str(x) for x in ult) if ult else "Unknown"
            ])
            j += 1

        print(tabulate(
            detalle,
            headers=[
                "Nodo",
                "Latitud",
                "Longitud",
                "# Individuos",
                "Primeros 3 tags",
                "Últimos 3 tags"
            ],
            tablefmt="grid",
            showindex=range(1, len(detalle) + 1)
        ))

        i += 1
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
