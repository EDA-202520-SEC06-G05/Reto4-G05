import time
import os 
import csv
from datetime import datetime as dt
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as lp
from DataStructures.Graph import digraph as dg
from DataStructures.Graph import vertex as v
from math import radians, cos, sin, asin, sqrt

data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/Challenge-4'

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    analyzer = {
    "event" : al.newlist(), # La parte de los elementos organizados por el timestap
    "events_by_tags" : lp.new_map(40,0.5,None), #Cada una de las grullas con su nodo de referencia
    "graph_distance" : dg.new_graph(None),
    "graph_water":dg.new_graph(None)
    }
    return analyzer
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    
# Funciones para la carga de datos
def cambio_datetime(horas):
    
    pass
    
    
def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    retorno = load_grullas(catalog["event"])
    
    return retorno

    # TODO: Realizar la carga de datos
    
def time_to_minutes(t):
    fecha, hora = t.split(" ")
    hh, mm, ss = hora.split(":")
    return int(hh)*60 + int(mm)                
            
# Funciones de consulta sobre el catálogo
def load_graph_distance(catalog):
    
    lista = catalog["events"]
    graph = catalog["graph_distance"]
    mapa = catalog["events_by_tags"]
    
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
            lp.put(mapa,id,id)
            
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

def haversine(lon1, lat1, lon2, lat2):

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 
    return c * r

def agrupar_eventos_por_grulla(lista_eventos):
    por_grulla = {}
    
    
    
    
def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
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
