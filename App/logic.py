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
        assigned = False
        longitude = each["location-long"]
        latitude = each["location-lat"]
        time = each["timestamp"]
        id = each["event-id"]
        distance = each["comments"]
        identi = each["tag-local-identifier"]
        
        if dg.order(graph) == 0:
            
            vertex_info = {
                "events": al.new_list(),
                "lon":longitude,
                "lat":latitude,
                "tiempo": time,
                "tag_identifiers": al.new_list(),
                "distance": distance,
                "events_count": 1
            }
            al.add_last(vertex_info["events"], each)
            al.add_last(vertex_info["tag_identifiers"], id)
            dg.insert_vertex(graph, id, vertex_info)
            lp.put(mapa,id,id)
        else:
            lista_vertices = dg.vertices(graph)
            i = 0
            assigned = False
            while i < lista_vertices["size"] and not assigned:
                key = al.get_element(lista_vertices, i)
                ver = dg.get_vertex(graph, key)
                t1 = ver["value"]["timestamp"]
                time_dif = abs(time_to_minutes(t1) - time_to_minutes(time))
                harv = haversine(ver["value"]["lon"], ver["value"]["lat"], longitude, latitude)
                
                if harv < 3 and time_dif < 180:
                    ver["events_count"] += 1  
                    array = ver["tag_identifiers"]
                    array_1 = ver["events"]
                    ver["tag_identifiers"] = al.add_last(array,id)
                    ver["events"] =al.add_last(array_1,each)
                    lp.put(mapa,id.key)
            if not assigned:
                vertex_info = {
                "events": al.new_list(),
                "lon":longitude,
                "lat":latitude,
                "tiempo": time,
                "tag_identifiers": al.new_list(),
                "distance": distance,
                "events_count": 1
            }
            al.add_last(vertex_info["events"], each)
            al.add_last(vertex_info["tag_identifiers"], id)
            dg.insert_vertex(graph, id, vertex_info)
            lp.put(mapa,id,id)
            
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
