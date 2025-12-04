import time
import os 
import csv
from datetime import datetime as dt
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as lp
from DataStructures.Graph import digraph as dg
from DataStructures.Graph import vertex as vt
from DataStructures.Graph import dfs
from DataStructures.Graph import dfo 
from DataStructures.Graph import bfs as bfs
from DataStructures.Graph import prim as pm 
from DataStructures.Stack import stack as st
from DataStructures.Queue import queue
from DataStructures.Stack import stack
from math import radians, cos, sin, asin, sqrt

data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/Challenge-4'

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    analyzer = {
    "event" : al.new_list(), # La parte de los elementos organizados por el timestap
    "events_by_tags" : lp.new_map(40,0.5,None), #Cada una de las grullas con su nodo de referencia
    "graph_distance" : dg.new_graph(20),
    "graph_water":dg.new_graph(20)
    }
    return analyzer
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    
# Funciones para la carga de datos
def haversine(lon1, lat1, lon2, lat2):

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 
    return c * r

def cambio_datetime(horas):
    
    pass

def time_to_minutes(t):
    fecha, hora = t.split(" ")
    hh, mm, ss = hora.split(":")
    return int(hh)*60 + int(mm) 

def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    retorno = load_grullas(catalog["event"])
    load_graph_distance(catalog)
    catalog["graph_water"] = catalog["graph_distance"]
    return retorno

    # TODO: Realizar la carga de datos
# Funciones de consulta sobre el catálogo

def load_grullas(catalog):
    flight_file = data_dir + "/1000_cranes_mongolia_large.csv" 
    input_file = csv.DictReader(open(flight_file, encoding="utf-8"), delimiter=",")
    
    for each in input_file:
        each["timestamp"] = dt.strptime(each["timestamp"], "%Y-%m-%d %H:%M:%S.%f")
        al.add_last(catalog,each)

    def default_sort(a1,a2):
        if a1["timestamp"] < a2["timestamp"]:
            return True
        return False
    al.merge_sort(catalog,default_sort)
    return catalog

def load_graph_distance(catalog):
    
    lista = catalog["events"]
    graph = catalog["graph_distance"]
    mapa = catalog["events_by_tags"]
    id_graph = al.new_list()
    for i in range(al.size(lista)):
        
        each = al.get_element(lista, i)
        
        longitude = float(each["location-long"])
        latitude = float(each["location-lat"])
        time = each["timestamp"]
        id = each["event-id"]
        distance = float(each["comments"])
        tag = each["tag-local-identifier"]
        
        if dg.order(graph) == 0:
            
            vertex_info = {
                "events": al.new_list(),
                "lon":longitude,
                "lat":latitude,
                "tiempo": time,
                "tag_identifiers": al.new_list(),
                "distance": al.new_list(),
                "events_count": 1
            }
            al.add_last(vertex_info["events"], each)
            al.add_last(vertex_info["tag_identifiers"], tag)
            al.add_last(vertex_info["distance"], distance)
            dg.insert_vertex(graph, id, vertex_info)
            al.add_last(id_graph,id)
            lp.put(mapa,id,id)
        else:
            lista_vertices = dg.vertices(graph)
            i = 0
            assigned = False
            while i < lista_vertices["size"] and not assigned:
                key = al.get_element(lista_vertices, i)
                ver = dg.get_vertex(graph, key)
                data = ver["value"]
                
                harv = haversine(data["lon"], data["lat"], longitude, latitude)
                time_dif = abs(time_to_minutes(time) - time_to_minutes(data["tiempo"]))
                
                if harv < 3 and time_dif < 180:
                    
                    ver["events_count"] += 1  
                    al.add_last(data["events"], each)
                    array = data["tag_identifiers"]
                    def cmp (a,b):
                        if a == b:
                            return 0
                        return -1
                    if al.is_present(array,tag,cmp) < 0:
                        al.add_last(data["tag_identifiers"], tag)
                    al.add_last(data["distance"],distance)
                    lp.put(mapa,id,key)
                    assigned = True
                i+=1
                
            if not assigned:
                vertex_info = {
                "events": al.new_list(),
                "lon":longitude,
                "lat":latitude,
                "tiempo": time,
                "tag_identifiers": al.new_list(),
                "distance": al.new_list(),
                "events_count": 1
            }
            al.add_last(vertex_info["events"], each)
            al.add_last(vertex_info["tag_identifiers"], tag)
            dg.insert_vertex(graph, id, vertex_info)
            al.add_last(id_graph,id)
            lp.put(mapa,id,id)
    for each in id_graph:
        node = dg.get_vertex(graph,each)
        value = node["value"]
        distance = value["distance"]
        sum = 0
        for i in distance:
            sum += i
        sum = sum / al.size(distance)
        value["distance"] = sum
    return catalog

def construir_arcos_distancia(catalog):
    eventos = catalog["event"]
    tags_events = catalog["event_by_tags"]
    grafo = catalog["graph_distance"]
    
    trips = lp.new_map(200000, 0.7, None)
    groups = lp.new_map(2000, 0.7, None)
    
    table = eventos["elements"]
    i = 0
    while i < eventos["size"]:
        each = al.get_element(eventos, i)
        tag = each["tag-local-identifier"]
        lista_tag = lp.get(groups, tag)
        if lista_tag is None:
            lista_tag = al.new_list()
            lp.put(groups, tag, lista_tag)
        al.add_last(lista_tag, each)
        i+=1
        
    tabla_groups = groups["table"]["elements"]
    g = 0
    while g < al.size(tabla_groups):
        slot = al.get_element(tabla_groups, g)
        if slot["key"] is not None:
            lista_ev = slot["value"]
            prev_node = None
            
            j = 0
            ev_elem = lista_ev["elements"]
            while j < lista_ev["size"]:
                ev = al.get_element(ev_elem, j)
                event_id = ev["event-id"]
                
                nodo_entry = lp.get(tags_events)
                if nodo_entry is not None:
                    actual = nodo_entry["value"]
                    if prev_node is not None and actual != prev_node:
                        vertA = dg.get_vertex(grafo, prev_node)
                        vertB = dg.get_vertex(grafo, actual)
                        
                        infoA = vertA["value"]["value"]
                        infoB = vertB["value"]["value"]
                        
                        dist = haversine(infoA["lon"], infoA["lat"], infoB["lon"], infoB["lat"])
                        
                        key = prev_node + "->" + actual
                        lista_dist = lp.get(trips, key)
                        if lista_dist is None:
                            list_dist = al.new_list()
                            lp.put(trips, key, list_dist)
                        al.add_last(list_dist, dist)
                        
                    prev_node = actual
                j += 1
        g += 1
    trip_table = trips["table"]["elements"]
    k = 0
    while k < al.size(trip_table):
        other = al.get_element(trip_table, k)
        if other["key"] is not None:
            key = slot["key"]
            lista_dist = slot["value"]
            parts = key.split("->")
            A = parts[0]
            B = parts[1]
            
            suma = 0
            ls = list_dist["elements"]
            t = 0
            while t < list_dist["size"]:
                distan = al.get_element(ls, t)
                suma += distan
                t += 1
            average = suma / lista_dist["size"]
            dg.add_edge(grafo, A, B, average)
        k += 1
    return catalog

def build_water_edges(catalog):
    events_array = catalog["event"]
    mapa_id = catalog["event_by_tags"]
    graph = catalog["graph_water"]
    trips = lp.new_map(200000, 0.7, None)
    groups = lp.new_map(2000, 0.7, None)
    i = 1
    while i <= events_array["size"]:
        each = al.get_element(events_array, i)
        tag = each["tag-local-identifier"]
        entry = lp.get(groups, tag)
        if entry is None:
            lista_tag = al.new_list()
            lp.put(groups, tag, lista_tag)
        else:
            lista_tag = lp.get(groups,entry)
            al.add_last(lista_tag, each)
        i += 1
        
    tabla_groups = groups["table"]["elements"]
    g = 0
    while g < al.size(tabla_groups):
        slot = al.get_element(tabla_groups, g)
        if slot is not None:
            lista_ev = slot["value"]      
            prev_node = None              
            j = 1
            while j <= lista_ev["size"]:
                ev = al.get_element(lista_ev, j)
                event_id = ev["event-id"]
                nodo_entry = lp.get(mapa_id, event_id)
                if nodo_entry is not None:
                    actual = lp.get(mapa_id,nodo_entry)   
                    if prev_node is not None and actual != prev_node:
                        vertB = dg.get_vertex(graph, actual)
                        infoB = vertB["value"]
                        prom_agua_B = infoB["distance"]
                        key = prev_node + "->" + actual
                        lista_entry = lp.get(trips, key)
                        if lista_entry is None:
                            lista_dist = al.new_list()
                            lp.put(trips, key, lista_dist)
                        else:
                            lista_dist = lp.get(trips,key)
                        al.add_last(lista_dist, prom_agua_B)
                    prev_node = actual
                j += 1
        g += 1
    trip_table = trips["table"]["elements"]
    k = 0
    while k < al.size(trip_table):
        other = al.get_element(trip_table, k)
        if other["key"] is not None:
            key = other["key"]
            lista_dist = other["value"]

            parts = key.split("->")
            a = parts[0]
            b = parts[1]
            suma = 0
            t = 1
            while t <= lista_dist["size"]:
                val = al.get_element(lista_dist, t)
                suma += val
                t += 1
            average = suma / lista_dist["size"]
            dg.add_edge(graph, a, b, average)
        k += 1
    return catalog


def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog, gps_origen, gps_destino, radio):
    """
    Retorna el resultado del requerimiento 2
    """
    lat_origen = gps_origen[0]
    lon_origen = gps_origen[1]
    lat_dest = gps_destino[0]
    lon_dest = gps_destino[1]

    grafo = catalog["graph_distance"]
    vertex_list = dg.vertices(grafo)
    nodoA = None
    nodoB = None
    bestA = 999999999
    bestB = 999999999
    
    i = 0
    while i < vertex_list["size"]:
        each = al.get_element(vertex_list, i)
        vert = dg.get_vertex(grafo, each)
        info = vert["value"]
        lat = info["lat"]
        lon = info["lon"]
        
        distA = haversine(lon_origen, lat_origen, lon, lat)
        distB = haversine(lon_dest, lat_dest, lon, lat)
        
        if distA < bestA:
            bestA = distA
            nodoA = each
        if distB < bestB:
            bestB = distB
            nodoB = each
        
        i+=1
    visit = bfs.bfs(grafo, nodoA)
    if not bfs.has_path_to(nodoB, visit):
        return {
            "mensaje": "No existe ningun camino entre los puntos.",
            "ruta": None
        }
    path = bfs.path_to(nodoB, visit)
    last = None
    temp_stack = st.new_stack()
    
    while not st.is_empty(path):
        ver = st.pop(path)
        st.push(temp_stack, ver)
        
        vert = dg.get_vertex(grafo, ver)
        info = vert["value"]
        lat = info["lat"]
        lon = info["lon"]
        
        d = haversine(lon_origen, lat_origen, lon, lat)
        if d <= radio:
            ultimo = ver
    path["elements"] = temp_stack["elements"]
    path["size"] = temp_stack["size"]
    
    total_distance = 0
    path_list = al.new_list()
    temp2 = st.new_stack()
    while not st.is_empty(path):
        v = st.pop(path)
        st.push(temp2, v)
        al.add_last(path_list, v)
    path["elements"] = temp2["elements"]
    path["size"] = temp2["size"]
    
    prev = None
    elems_ruta = path_list["elements"]
    j = 0
    while j < path_list["size"]:
        v = al.get_element(elems_ruta, j)
        if prev is not None:
            vert_prev = dg.get_vertex(grafo, prev)
            edge = vt.get_edge(vert_prev, v)
            if edge is not None:
                total_distance = total_distance + edge["weight"]
        prev = v
        j+=1
    total_points = path_list["size"]
    return {
        "mensaje": "Ruta encontrada",
        "ultimo_dentro_radio": last,
        "distancia_total": total_distance,
        "total_puntos": total_points, 
        "ruta": path_list
    }
    # TODO: Modificar el requerimiento 2
    
def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    nicho_biologico = catalog["graph_distance"]
    answer = {
        "vertices" : 0,
        "pajaros" : 0,        
    }
    graph, centinela = dfs.dfs(nicho_biologico,"8087306349")
    if centinela:
        post_reversed = dfo.dfo(nicho_biologico)
        post_reversed = post_reversed["reversepost"]
        first = al.new_list()
        vertices = st.size(post_reversed)
        pajaros= 0
        while not st.is_empty(post_reversed):
            vertex = dg.get_vertex(nicho_biologico,st.pop(post_reversed))["value"]
            dict_clean = {
                "id": vertex["id"],
                "lon": vertex["lon"],
                "lan": vertex["lan"],
                "pajaros" : al.size(vertex["tag_identifiers"]),
                "first": al.sub_list(vertex["tag_identifiers"],0,2),
                "last": al.sub_list(vertex["tag_identifiers"],al.size(vertex["tag_identifiers"])-3, 3),
                "adyacentes":dg.edges_vertex(nicho_biologico,st.pop(post_reversed))
            }
            pajaros += al.size(vertex["tag_identifiers"])
            al.add_last(first,dict_clean)
        answer["vertices"] = vertices
        answer["pajaros"] = pajaros
        answer["fisrt"] = al.sub_list(first,0,4)
        answer["last"] = al.sub_list(first,al.size(first)-5,5)
        return answer
    else:
        return ("Se presentaron ciclos dentro del grafo a realizar dfo")
    # TODO: Modificar el requerimiento 3
    pass

def req_4(catalog,lon,lat):
    """
    Retorna el resultado del requerimiento 4
    """
    answer ={
        "total_vertice": 0,
        "total_individuos": 0,
        "distancia_total": 0,
        
    }
    graph = catalog["graph_water"]
    min = 999999999
    key = 0
    vertices= dg.vertices(graph)
    for i in vertices["elements"]:
        vertex = dg.get_vertex(graph,i)
        lon_x = vertex["lon"]
        lat_x = vertex["lat"]
        distance = haversine(lon,lat,lon_x,lat_x)
        if min > distance:
            min = distance
            key = i
    prim = pm.prim_mst(graph,key) 
    edges = pm.edges_mst(graph, prim)

    if al.size(edges) == 0:
        return "No se encontró una red hídrica viable desde el origen especificado"
    else:
        distancia_total = pm.weight_mst(graph, prim)
        answer["distancia_total"] = distancia_total
        visited = prim["visited"]
        tabla = visited["table"]["elements"]
        total_vertices = 0
        i = 0
        while i < al.size(tabla):
            slot = al.get_element(tabla, i)
            if slot["key"] is not None:
                info = slot["value"]
                if info["marked"] is True:
                    total_vertices += 1
            i += 1
        answer["total_vertice"] = total_vertices 
        map_tags = lp.new_map(2000, 0.5, None)
        i = 0
        while i < al.size(tabla):
            slot = al.get_element(tabla, i)
            if slot["key"] is not None:
                vid = slot["key"]
                info = slot["value"]
                if info["marked"] is True:
                    vert_info = dg.get_vertex(graph, vid)["value"]
                    tags = vert_info["tag_identifiers"]
                    j = 1
                    while j <= al.size(tags):
                        tag = al.get_element(tags, j)
                        if not lp.contains(map_tags, tag):
                            lp.put(map_tags, tag, True)
                        j += 1
            i += 1
        answer["total_individuos"] = lp.size(map_tags)

        children = lp.new_map(2000, 0.5, None)
        i = 0
        while i < al.size(tabla):
            slot = al.get_element(tabla, i)
            if slot["key"] is not None:
                vid = slot["key"]
                info = slot["value"]
                parent = info["edge_from"]
                if info["marked"] is True and parent is not None:
                    entry = lp.get(children, parent)
                    if entry is None:
                        lista_hijos = al.new_list()
                        lp.put(children, parent, lista_hijos)
                    else:
                        lista_hijos = entry["value"]
                    al.add_last(lista_hijos, vid)
            i += 1

        ruta = al.new_list()
        q = queue.new_queue()
        vistos = lp.new_map(2000, 0.5, None)
        queue.enqueue(q, key)
        lp.put(vistos, key, True)

        while not queue.is_empty(q):
            v = queue.dequeue(q)
            al.add_last(ruta, v)
            entry = lp.get(children, v)
            if entry is not None:
                hijos = entry["value"]
                j = 1
                while j <= al.size(hijos):
                    w = al.get_element(hijos, j)
                    if not lp.contains(vistos, w):
                        lp.put(vistos, w, True)
                        queue.enqueue(q, w)
                    j += 1

        n = al.size(ruta)
        if n == 0:
            answer["primeros_5"] = al.new_list()
            answer["ultimos_5"] = al.new_list()
            return answer

        k = 5 if n >= 5 else n

        lista_info = al.new_list()
        j = 1
        while j <= n:
            vid = al.get_element(ruta, j)
            vert_info = dg.get_vertex(graph, vid)["value"]
            tags = vert_info["tag_identifiers"]
            num_tags = al.size(tags)

            if num_tags == 0:
                first_tags = "Unknown"
                last_tags = "Unknown"
            else:
                fcount = 3 if num_tags >= 3 else num_tags
                first_tags = al.sub_list(tags, 1, fcount)

                lcount = 3 if num_tags >= 3 else num_tags
                start_last = num_tags - lcount + 1
                last_tags = al.sub_list(tags, start_last, lcount)

            info_node = {
                "id": vid,
                "lon": vert_info["lon"],
                "lat": vert_info["lat"],
                "num_pajaros": num_tags,
                "first_tags": first_tags,
                "last_tags": last_tags
            }
            al.add_last(lista_info, info_node)
            j += 1

        primeros = al.sub_list(lista_info, 1, k)
        ultimos = al.sub_list(lista_info, n - k + 1, k)

        answer["primeros_5"] = primeros
        answer["ultimos_5"] = ultimos

        return answer
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
