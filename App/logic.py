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
from DataStructures.Graph import dijkstra as dj
from DataStructures.Graph import edge as ed
from DataStructures.Graph import prim as pm
from DataStructures.Queue import queue as queue 
from math import radians, cos, sin, asin, sqrt

data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/Challenge-4'

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    analyzer = {
    "event" : al.new_list(), # La parte de los elementos organizados por el timestap
    "events_by_tags" : lp.new_map(40,0.5,None), #Cada una de las grullas con su nodo de referencia
    "graph_distance" : dg.new_graph(10000),
    "graph_water":dg.new_graph(10000)
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

def time_to_minutes(t):
    t = str(t)
    fecha, hora = t.split(" ")
    hh, mm, ss = hora.split(":")
    return int(hh)*60 + int(mm) 

def load_data(catalog,):
    """
    Carga los datos del reto
    """
    load_grullas(catalog["event"])
    load_graph_distance(catalog)
    build_water_vertices(catalog)
    construir_arcos_distancia(catalog)
    construir_arcos_water(catalog)
    resumen_distance = resumen_carga_distance(catalog)
    resumen_water = resumen_carga_water(catalog)
    return {
        "distance": resumen_distance,
        "water": resumen_water
    }
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
    lista = catalog["event"]              # Lista de todos los eventos ordenados
    graph = catalog["graph_distance"]     # Grafo de distancia migratoria
    mapa = catalog["events_by_tags"]      # event-id → vertex-id

    id_graph = al.new_list()              # Lista con todos los ID de vértices

    i = 0
    while i < al.size(lista):
        each = al.get_element(lista, i)

        lon = float(each["location-long"])
        lat = float(each["location-lat"])
        tiempo = each["timestamp"]
        ev_id = each["event-id"]
        dist_water = float(each["comments"])     # distancia al agua
        tag = each["tag-local-identifier"]

        # PRIMER VÉRTICE
        if dg.order(graph) == 0:

            info = {
                "events": al.new_list(),
                "lon": lon,
                "lat": lat,
                "tiempo": tiempo,
                "tag_identifiers": al.new_list(),
                "distance": al.new_list(),
                "events_count": 1
            }

            al.add_last(info["events"], each)
            al.add_last(info["tag_identifiers"], tag)
            al.add_last(info["distance"], dist_water)

            dg.insert_vertex(graph, ev_id, info)
            al.add_last(id_graph, ev_id)
            lp.put(mapa, ev_id, ev_id)

        else:

            lista_vertices = dg.vertices(graph)
            j = 0
            assigned = False
            # Intentar asignarlo a un vértice ya existente
            while j < al.size(lista_vertices) and not assigned:

                key_v = al.get_element(lista_vertices, j)
                vert = dg.get_vertex(graph, key_v)
                info_v = vert["value"]

                harv = haversine(info_v["lon"], info_v["lat"], lon, lat)
                time_dif = abs(time_to_minutes(tiempo) - time_to_minutes(info_v["tiempo"]))
                
                if harv < 3 and time_dif < 180:
                    info_v["events_count"] += 1
                    al.add_last(info_v["events"], each)
                    
                    # Añadir tag si no existe
                    def cmp(a, b):
                        if a == b:
                            return 0
                        return -1

                    if al.is_present(info_v["tag_identifiers"], tag, cmp) < 0:
                        al.add_last(info_v["tag_identifiers"], tag)

                    al.add_last(info_v["distance"], dist_water)

                    lp.put(mapa, ev_id, key_v)

                    assigned = True

                j += 1

            # No se pudo agrupar → crear un nuevo vértice
            if not assigned:

                info = {
                    "events": al.new_list(),
                    "lon": lon,
                    "lat": lat,
                    "tiempo": tiempo,
                    "tag_identifiers": al.new_list(),
                    "distance": al.new_list(),
                    "events_count": 1
                }

                al.add_last(info["events"], each)
                al.add_last(info["tag_identifiers"], tag)
                al.add_last(info["distance"], dist_water)

                dg.insert_vertex(graph, ev_id, info)
                al.add_last(id_graph, ev_id)
                lp.put(mapa, ev_id, ev_id)

        i += 1

    # Convertir la lista de distancias al agua en el promedio
    k = 0
    while k < al.size(id_graph):
        key_v = al.get_element(id_graph, k)
        vert = dg.get_vertex(graph, key_v)
        info = vert["value"]
        dist_list = info["distance"]

        s = 0
        m = 0
        while m < al.size(dist_list):
            s += al.get_element(dist_list, m)
            m += 1

        if al.size(dist_list) > 0:
            info["distance"] = s / al.size(dist_list)
        else:
            info["distance"] = 0

        k += 1
    return catalog

def build_water_vertices(catalog):

    graph_dist = catalog["graph_distance"]
    graph_water = catalog["graph_water"]

    lista_vertices = dg.vertices(graph_dist)

    i = 0
    while i < al.size(lista_vertices):

        vid = al.get_element(lista_vertices, i)
        vert = dg.get_vertex(graph_dist, vid)
        info = vert["value"]
        nueva_info = {
            "events": info["events"],
            "lon": info["lon"],
            "lat": info["lat"],
            "tiempo": info["tiempo"],
            "tag_identifiers": info["tag_identifiers"],
            "distance": info["distance"],  # promedio agua ya calculado
            "events_count": info["events_count"]
        }

        dg.insert_vertex(graph_water, vid, nueva_info)

        i += 1

    return catalog

def construir_arcos_distancia(catalog):
    eventos = catalog["event"]
    tags_events = catalog["events_by_tags"]
    grafo = catalog["graph_distance"]

    # trips: key = "A->B" , value = lista de distancias
    trips = lp.new_map(200000, 0.7, None)

    # groups: tag → lista de eventos del tag
    grupos = lp.new_map(2000, 0.7, None)

    # 1. Agrupar eventos por tag
    i = 0
    while i < al.size(eventos):
        ev = al.get_element(eventos, i)
        tag = ev["tag-local-identifier"]

        lista_tag = lp.get(grupos, tag)
        if lista_tag is None:
            lista_tag = al.new_list()
            lp.put(grupos, tag, lista_tag)

        al.add_last(lista_tag, ev)
        i += 1

    # 2. Procesar cada tag para detectar viajes
    tabla_grupos = grupos["table"]
    g = 0
    while g < al.size(tabla_grupos):

        slot = al.get_element(tabla_grupos, g)
        if slot["key"] is not None:

            lista_ev = slot["value"]
            prev_node = None

            j = 0
            while j < al.size(lista_ev):

                ev = al.get_element(lista_ev, j)
                event_id = ev["event-id"]

                nodo_actual = lp.get(tags_events, event_id)

                if nodo_actual is not None:

                    if prev_node is not None and nodo_actual != prev_node:

                        # info de A y B
                        vertA = dg.get_vertex(grafo, prev_node)
                        vertB = dg.get_vertex(grafo, nodo_actual)

                        infoA = vertA["value"]
                        infoB = vertB["value"]

                        dist = haversine(infoA["lon"], infoA["lat"], infoB["lon"], infoB["lat"])

                        key_arc = prev_node + "->" + nodo_actual
                        lista_dist = lp.get(trips, key_arc)
                        if lista_dist is None:
                            lista_dist = al.new_list()
                            lp.put(trips, key_arc, lista_dist)

                        al.add_last(lista_dist, dist)

                    prev_node = nodo_actual

                j += 1

        g += 1

    # 3. Crear arcos promediando las distancias
    tabla_trips = trips["table"]
    k = 0
    while k < al.size(tabla_trips):

        slot = al.get_element(tabla_trips, k)
        if slot["key"] is not None:

            key = slot["key"]         # "A->B"
            lista_dist = slot["value"]

            partes = key.split("->")
            A = partes[0]
            B = partes[1]

            # promedio
            suma = 0
            t = 0
            while t < al.size(lista_dist):
                suma += al.get_element(lista_dist, t)
                t += 1

            promedio = suma / al.size(lista_dist)

            dg.add_edge(grafo, A, B, promedio)

        k += 1

    return catalog

def construir_arcos_water(catalog):

    eventos = catalog["event"]
    mapa_ids = catalog["events_by_tags"]     # event-id → id punto migratorio
    grafo = catalog["graph_water"]

    trips = lp.new_map(200000, 0.7, None)    # (A->B) → lista de distancias agua
    groups = lp.new_map(2000, 0.7, None)     # tag → lista de eventos

    # =====================================================
    # 1. Agrupar eventos por tag
    # =====================================================
    i = 0
    while i < eventos["size"]:
        ev = al.get_element(eventos, i)
        tag = ev["tag-local-identifier"]

        lista_tag = lp.get(groups, tag)
        if lista_tag is None:
            lista_tag = al.new_list()
            lp.put(groups, tag, lista_tag)

        al.add_last(lista_tag, ev)
        i += 1

    # =====================================================
    # 2. Recorrer cada tag y construir transiciones A -> B
    # =====================================================
    tabla_groups = groups["table"]
    g = 0
    while g < al.size(tabla_groups):

        slot = al.get_element(tabla_groups, g)

        if slot["key"] is not None:

            lista_ev = slot["value"]
            prev_point = None

            j = 0
            while j < lista_ev["size"]:

                ev = al.get_element(lista_ev, j)
                event_id = ev["event-id"]

                punto = lp.get(mapa_ids, event_id)
                if punto is not None:

                    actual_point = punto

                    # si existe transición A -> B
                    if prev_point is not None and actual_point != prev_point:

                        nodoB = dg.get_vertex(grafo, actual_point)
                        infoB = nodoB["value"]

                        # distancia promedio a fuentes hídricas de B
                        dist_agua = infoB["distance"]

                        key = prev_point + "->" + actual_point

                        lista = lp.get(trips, key)
                        if lista is None:
                            lista = al.new_list()
                            lp.put(trips, key, lista)

                        al.add_last(lista, dist_agua)

                    prev_point = actual_point

                j += 1

        g += 1

    # =====================================================
    # 3. Promediar transiciones y agregar arcos al grafo
    # =====================================================
    tabla_trips = trips["table"]
    k = 0
    while k < al.size(tabla_trips):

        slot = al.get_element(tabla_trips, k)

        if slot["key"] is not None:

            key = slot["key"]
            lista = slot["value"]

            A, B = key.split("->")

            # promedio
            suma = 0
            t = 0
            while t < lista["size"]:
                suma += al.get_element(lista, t)
                t += 1

            promedio = suma / lista["size"]

            # crear arco A → B con peso promedio
            dg.add_edge(grafo, A, B, promedio)

        k += 1

    return catalog

def resumen_carga_distance(catalog):
    grafo = catalog["graph_distance"]

    total_eventos = al.size(catalog["event"])

    tags_unicos = lp.new_map(2000, 0.7, None)

    eventos = catalog["event"]
    i = 0
    while i < al.size(eventos):
        ev = al.get_element(eventos, i)
        tag = ev["tag-local-identifier"]

        existe_tag = lp.get(tags_unicos, tag)
        if existe_tag is None:
            lp.put(tags_unicos, tag, True)

        i += 1

    total_grullas = tags_unicos["size"]

    total_nodos = dg.order(grafo)
    total_arcos = dg.size(grafo)

    vertices = dg.vertices(grafo)

    primeros5 = al.new_list()

    i = 0
    while i < 5 and i < al.size(vertices):

        vid = al.get_element(vertices, i)
        v = dg.get_vertex(grafo, vid)
        info = v["value"]

        nodo_info = {
            "id": vid,
            "lat": info["lat"],
            "lon": info["lon"],
            "fecha": info["tiempo"],
            "tags": info["tag_identifiers"],
            "eventos": info["events_count"]
        }

        al.add_last(primeros5, nodo_info)
        i += 1

    ultimos5 = al.new_list()
    total_vertices = al.size(vertices)

    hay_mas_de_5 = total_vertices > 5

    if hay_mas_de_5:
        start = total_vertices - 5
    else:
        start = 0

    j = start
    while j < total_vertices:

        vid = al.get_element(vertices, j)
        v = dg.get_vertex(grafo, vid)
        info = v["value"]

        nodo_info = {
            "id": vid,
            "lat": info["lat"],
            "lon": info["lon"],
            "fecha": info["tiempo"],
            "tags": info["tag_identifiers"],
            "eventos": info["events_count"]
        }

        al.add_last(ultimos5, nodo_info)
        j += 1

    return {
        "total_grullas": total_grullas,
        "total_eventos": total_eventos,
        "total_nodos": total_nodos,
        "total_arcos": total_arcos,
        "primeros5": primeros5,
        "ultimos5": ultimos5
    }

def resumen_carga_water(catalog):
    grafo = catalog["graph_water"]

    total_eventos = al.size(catalog["event"])

    tags_unicos = lp.new_map(2000, 0.7, None)

    eventos = catalog["event"]
    i = 0
    while i < al.size(eventos):

        ev = al.get_element(eventos, i)
        tag = ev["tag-local-identifier"]

        existe = lp.get(tags_unicos, tag)
        if existe is None:
            lp.put(tags_unicos, tag, True)

        i += 1

    total_grullas = tags_unicos["size"]

    total_nodos = dg.order(grafo)
    total_arcos = dg.size(grafo)

    vertices = dg.vertices(grafo)

    primeros5 = al.new_list()

    i = 0
    while i < 5 and i < al.size(vertices):

        vid = al.get_element(vertices, i)
        v = dg.get_vertex(grafo, vid)
        info = v["value"]

        nodo_info = {
            "id": vid,
            "lat": info["lat"],
            "lon": info["lon"],
            "fecha": info["tiempo"],
            "tags": info["tag_identifiers"],
            "eventos": info["events_count"]
        }

        al.add_last(primeros5, nodo_info)
        i += 1
        
    ultimos5 = al.new_list()
    total_vertices = al.size(vertices)

    hay_mas_de_5 = total_vertices > 5

    if hay_mas_de_5:
        start = total_vertices - 5
    else:
        start = 0

    j = start
    while j < total_vertices:

        vid = al.get_element(vertices, j)
        v = dg.get_vertex(grafo, vid)
        info = v["value"]

        nodo_info = {
            "id": vid,
            "lat": info["lat"],
            "lon": info["lon"],
            "fecha": info["tiempo"],
            "tags": info["tag_identifiers"],
            "eventos": info["events_count"]
        }

        al.add_last(ultimos5, nodo_info)
        j += 1

    return {
        "total_grullas": total_grullas,
        "total_eventos": total_eventos,
        "total_nodos": total_nodos,
        "total_arcos": total_arcos,
        "primeros5": primeros5,
        "ultimos5": ultimos5
    }

def req_1(catalog,gps_origen,gps_destino,tag_id):
    grafo=catalog["graph_distance"]
    vertex_list=dg.vertices(grafo)
    lat_origen,lon_origen=gps_origen
    lat_dest,lon_dest=gps_destino
    
    nodo_o,nodo_d=None,None
    best_o,best_d=999999999,999999999
    
    
    i=0
    while i<vertex_list["size"]:
        vid=al.get_element(vertex_list,i)
        vert=dg.get_vertex(grafo,vid)
        info=vert["value"]
        lat=info["lat"] if "lat" in info else "Desconocido"
        lon=info["lon"] if "lon" in info else "Desconocido"
        
        if lat!="Desconocido" and lon!="Desconocido":
            dist_o=haversine(lon_origen,lat_origen,lon,lat)
            dist_d=haversine(lon_dest,lat_dest,lon,lat)
            
            if dist_o<best_o:
                best_o=dist_o
                nodo_o=vid
            if dist_d<best_d:
                best_d=dist_d
                nodo_d=vid
        i+=1
    
    if nodo_o is None or nodo_d is None:
        return {"mensaje": "No se pudo determinar origen o destino."}
    
    
    visit=dfs.dfs(grafo,nodo_o)
    if not dfs.has_path_to(nodo_d,visit):
        return {"mensaje": "No existe un camino viable.", "ruta": None}
    
    path=dfs.path_to(nodo_d,visit)
    
    
    temp_stack=st.new_stack()
    while not st.is_empty(path):
        st.push(temp_stack,st.pop(path))
    path=temp_stack
    
    
    ruta=al.new_list()
    temp_stack2=st.new_stack()
    while not st.is_empty(path):
        v=st.pop(path)
        st.push(temp_stack2,v)
        al.add_last(ruta,v)
    path=temp_stack2
    
    total_points=al.size(ruta)
    total_distance=0
    primer="Desconocido"
    prev=None
    j=0
    
    
    while j<total_points:
        nid=al.get_element(ruta,j)
        vert=dg.get_vertex(grafo,nid)
        info=vert["value"]
        tags=info["tag_identifiers"] if "tag_identifiers" in info else None
        
        if primer=="Desconocido" and tags is not None:
            k=0
            while k<al.size(tags):
                if al.get_element(tags,k)==tag_id:
                    primer=nid
                    break
                k+=1
        
        if prev is not None:
            vert_prev=dg.get_vertex(grafo,prev)
            edge=vt.get_edge(vert_prev,nid)
            if edge is not None:
                total_distance+=edge.get("weight",0)
        prev=nid
        j+=1
    
    
    detalle=al.new_list()
    
    
    x=0
    while x<5 and x<total_points:
        nid=al.get_element(ruta,x)
        vert=dg.get_vertex(grafo,nid)
        info=vert["value"]
        name=info["name"] if "name" in info else nid
        lat=info["lat"] if "lat" in info else "Desconocido"
        lon=info["lon"] if "lon" in info else "Desconocido"
        tags=info["tag_identifiers"] if "tag_identifiers" in info else None
        num=al.size(tags) if tags is not None else 0
        
        p3=al.new_list()
        u3=al.new_list()
        a=0
        while tags is not None and a<3 and a<num:
            al.add_last(p3,al.get_element(tags,a))
            a+=1
        b=max(0,num-3)
        while tags is not None and b<num:
            al.add_last(u3,al.get_element(tags,b))
            b+=1
        
        dist_sig="Desconocido"
        if x+1<total_points:
            sig=al.get_element(ruta,x+1)
            edge=vt.get_edge(vert,sig)
            if edge is not None:
                dist_sig=edge.get("weight","Desconocido")
        
        al.add_last(detalle,{
            "nombre": name,
            "lat": lat,
            "lon": lon,
            "n_individuos": num,
            "primeros_3": p3,
            "ultimos_3": u3,
            "dist_sig": dist_sig
        })
        x+=1
    
    
    ini=max(0,total_points-5)
    while ini<total_points:
        nid=al.get_element(ruta,ini)
        vert=dg.get_vertex(grafo,nid)
        info=vert["value"]
        name=info["name"] if "name" in info else nid
        lat=info["lat"] if "lat" in info else "Desconocido"
        lon=info["lon"] if "lon" in info else "Desconocido"
        tags=info["tag_identifiers"] if "tag_identifiers" in info else None
        num=al.size(tags) if tags is not None else 0
        
        p3=al.new_list()
        u3=al.new_list()
        a=0
        while tags is not None and a<3 and a<num:
            al.add_last(p3,al.get_element(tags,a))
            a+=1
        b=max(0,num-3)
        while tags is not None and b<num:
            al.add_last(u3,al.get_element(tags,b))
            b+=1
        
        dist_sig="Desconocido"
        if ini+1<total_points:
            sig=al.get_element(ruta,ini+1)
            edge=vt.get_edge(vert,sig)
            if edge is not None:
                dist_sig=edge.get("weight","Desconocido")
        
        al.add_last(detalle,{
            "nombre": name,
            "lat": lat,
            "lon": lon,
            "n_individuos": num,
            "primeros_3": p3,
            "ultimos_3": u3,
            "dist_sig": dist_sig
        })
        ini+=1
    
    return {
        "mensaje": f"Primer nodo donde aparece la grulla: {primer}",
        "primer_nodo": primer,
        "distancia_total": total_distance,
        "total_puntos": total_points,
        "detalle": detalle,
        "ruta": ruta
    }


def req_2(catalog, gps_origen, gps_destino, radio):

    lat_o = float(gps_origen[0])
    lon_o = float(gps_origen[1])
    lat_d = float(gps_destino[0])
    lon_d = float(gps_destino[1])

    grafo = catalog["graph_distance"]
    lista_vertices = dg.vertices(grafo)

    nodoA = None
    nodoB = None
    bestA = 999999999
    bestB = 999999999

    i = 0
    while i < al.size(lista_vertices):
        vid = al.get_element(lista_vertices, i)
        vert = dg.get_vertex(grafo, vid)
        info = vert["value"]

        lat = info["lat"]
        lon = info["lon"]

        dA = haversine(lon_o, lat_o, lon, lat)
        dB = haversine(lon_d, lat_d, lon, lat)

        if dA < bestA:
            bestA = dA
            nodoA = vid

        if dB < bestB:
            bestB = dB
            nodoB = vid

        i += 1


    if nodoA is None or nodoB is None:
        return {"mensaje": "No se pudieron identificar puntos migratorios."}

    visit = bfs.bfs(grafo, nodoA)

    if not bfs.has_path_to(nodoB, visit):
        return {
            "mensaje": "No existe ningun camino entre los puntos.",
            "ruta": None
        }

    stack_path = bfs.path_to(nodoB, visit)

    lista_camino = al.new_list()
    temp = st.new_stack()

    last_inside = None

    while not st.is_empty(stack_path):
        v = st.pop(stack_path)
        st.push(temp, v)
        al.add_last(lista_camino, v)

    
    stack_path["elements"] = temp["elements"]
    stack_path["size"] = temp["size"]

    j = 0
    elems = lista_camino["elements"]
    while j < lista_camino["size"]:
        vid = al.get_element(elems, j)
        vert = dg.get_vertex(grafo, vid)
        info = vert["value"]

        lat = info["lat"]
        lon = info["lon"]

        d = haversine(lon_o, lat_o, lon, lat)
        if d <= radio:
            last_inside = vid

        j += 1

    total_distance = 0
    prev = None

    j = 0
    while j < lista_camino["size"]:
        v = al.get_element(elems, j)

        if prev is not None:
            vert_prev = dg.get_vertex(grafo, prev)
            edge = vt.get_edge(vert_prev, v)
            if edge is not None:
                total_distance += edge["weight"]

        prev = v
        j += 1

    return {
        "mensaje": "Ruta encontrada",
        "ultimo_dentro_radio": last_inside,
        "distancia_total": total_distance,
        "total_puntos": lista_camino["size"],
        "ruta": lista_camino
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
            valor = st.pop(post_reversed)
            vertex_info = dg.get_vertex(nicho_biologico, valor)
            if vertex_info is not None:
                vertex_info = vertex_info["value"]
                vertex_x = vertex_info["tag_identifiers"]
                evento = vertex_info["events"]["elements"][0] 

                dict_clean = {
                "id": evento["event-id"],
                "lon": evento["location-long"],
                "lan": evento["location-lat"],
                "pajaros": al.size(vertex_x),
                "first": al.sub_list(vertex_x, 1, 2),
                "last": al.sub_list(vertex_x, al.size(vertex_x) - 2, 3),
                "adyacentes": dg.edges_vertex(nicho_biologico, valor)
            }

                pajaros += al.size(vertex_x)
                al.add_last(first, dict_clean)
        answer["vertices"] = vertices
        answer["pajaros"] = pajaros
        answer["fisrt"] = al.sub_list(first,0,4)
        answer["last"] = al.sub_list(first,al.size(first)-5,5)
        return answer
    else:
        return ("Se presentaron ciclos dentro del grafo a realizar dfo")
    # TODO: Modificar el requerimiento 3

def req_4(catalog,punto):
    """
    Retorna el resultado del requerimiento 4
    """
    lon = float(punto[1])
    lat = float(punto[0])
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
    # TODO: Modificar el requerimiento 4
    pass

def req_5(catalog, pto_origen, pto_destino, seleccion):
    """
    Retorna el resultado del requerimiento 5
    """
    
    if seleccion.upper() == "WATER":
        grafo = catalog["graph_water"]
    else:
        grafo = catalog["graph_distance"]

    lat_origen = float(pto_origen[0])
    lon_origen = float(pto_origen[1])
    lat_destino = float(pto_destino[0])
    lon_destino = float(pto_destino[1])

    vertexs = dg.vertices(grafo)
    nodoA = None
    nodoB = None
    bestA = 999999999
    bestB = 999999999

    i = 0
    while i < al.size(vertexs):
        vid = al.get_element(vertexs, i)
        v = dg.get_vertex(grafo, vid)
        info = v["value"]
        
        latv = info["lat"]
        lonv = info["lon"]
        
        dA = haversine(lon_origen, lat_origen, lonv, latv)
        dB = haversine(lon_destino, lat_destino, lonv, latv)

        if dA < bestA:
            bestA = dA
            nodoA = vid
        if dB < bestB:
            bestB = dB
            nodoB = vid
        print (nodoA)
        print(nodoB)
        i += 1

    if nodoA is None or nodoB is None:
        return {
            "mensaje": "No fue posible identificar nodos migratorios cercanos",
            "cost": "Unknown",
            "total_points": 0,
            "total_segments": 0,
            "first_nodes": al.new_list(),
            "last_nodes": al.new_list()
        }

    estructura = dj.dijkstra(grafo, nodoA)

    if not dj.has_path_to(nodoB, estructura):
        return {
            "mensaje": "No existe un camino óptimo entre los puntos",
            "cost": "Unknown",
            "total_points": 0,
            "total_segments": 0,
            "first_nodes": al.new_list(),
            "last_nodes": al.new_list()
        }

    path_stack = dj.path_to(nodoB, estructura)
    path = al.new_list()

    while not st.is_empty(path_stack):
        al.add_last(path, st.pop(path_stack))

    total_points = al.size(path)
    total_segments = total_points - 1

    rout_info = al.new_list()

    i = 0
    while i < al.size(path):
        nid = al.get_element(path, i)
        v = dg.get_vertex(grafo, nid)
        info = v["value"]

        lat_ok = lp.get(info, "lat")
        if lat_ok is not None:
            lat = lat_ok
        else:
            lat = "Unknown"
        
        lon_ok = lp.get(info, "lon")
        if lon_ok is not None:
            lon = lon_ok
        else:
            lon = "Unknown"
        
        tags_ok = lp.get(info, "tag_identifiers")
        if tags_ok is not None:
            tags = tags_ok
        else:
            tags = al.new_list()

        tsize = al.size(tags)

         
        first3 = al.new_list()
        j = 0
        while j < 3 and j < tsize:
            al.add_last(first3, al.get_element(tags, j))
            j += 1


        last3 = al.new_list()
        start = tsize - 3
        if start < 0:
            start = 0
        j = start
        while j < tsize:
            al.add_last(last3, al.get_element(tags, j))
            j += 1

        events_ok = lp.get(info, "events_count")
        if events_ok is not None:
            event_num = events_ok
        else:
            event_num = "Unknown"
             

        detalle = {
            "id": nid,
            "lat": lat,
            "lon": lon,
            "num_grullas": tsize,
            "first3": first3,
            "last3": last3,
            "events": event_num,
            "dnext": "Unknown"
        }

        al.add_last(rout_info, detalle)
        i += 1

    i = 0
    while i < al.size(rout_info) - 1:
        actual = al.get_element(rout_info, i)
        sigue = al.get_element(rout_info, i + 1)

        idA = actual["id"]
        idB = sigue["id"]

        vA = dg.get_vertex(grafo, idA)
        edge = vt.get_edge(vA, idB)

        if edge is not None:
            actual["dnext"] = edge["weight"]
        else:
            actual["dnext"] = "Unknown"

        i += 1

    first5 = al.new_list()
    i = 0
    while i < 5 and i < al.size(rout_info):
        al.add_last(first5, al.get_element(rout_info, i))
        i += 1

    last5 = al.new_list()
    total = al.size(rout_info)
    start = 0
    if total > 5:
        start = total - 5

    j = start
    while j < total:
        al.add_last(last5, al.get_element(rout_info, j))
        j += 1

    return {
        "mensaje": "Ruta óptima encontrada.",
        "cost": dj.dist_to(nodoB, estructura),
        "total_points": total_points,
        "total_segments": total_segments,
        "first_nodes": first5,
        "last_nodes": last5,
        "full_route": rout_info
    }

def req_6(catalog):
    grafo = catalog["graph_distance"]
    vertex_list = dg.vertices(grafo)
    visitados = lp.new_map(al.size(vertex_list), 0.5, None)
    subredes = al.new_list()
    subred_id = 1

    i = 0
    while i < vertex_list["size"]:
        nid = al.get_element(vertex_list, i)
        if not lp.contains(visitados, nid):
            stack = st.new_stack()
            st.push(stack, nid)
            al_add = al.new_list()
            while not st.is_empty(stack):
                v = st.pop(stack)
                if not lp.contains(visitados, v):
                    lp.put(visitados, v, subred_id)
                    al.add_last(al_add, v)
                    vert = dg.get_vertex(grafo, v)
                    ady = dg.adjacents(vert)
                    j = 0
                    while j < al.size(ady):
                        vecino = al.get_element(ady, j)
                        if not lp.contains(visitados, vecino):
                            st.push(stack, vecino)
                        j += 1
            total_individuos = 0
            max_lat = -999
            min_lat = 999
            max_lon = -999
            min_lon = 999
            for idx in range(al.size(al_add)):
                v = al.get_element(al_add, idx)
                vert = dg.get_vertex(grafo, v)
                info = vert["value"]
                lat = info["lat"] if "lat" in info else "Desconocido"
                lon = info["lon"] if "lon" in info else "Desconocido"
                tags = info["tag_identifiers"] if "tag_identifiers" in info else al.new_list()
                total_individuos += al.size(tags)
                if lat != "Desconocido":
                    max_lat = max(max_lat, lat)
                    min_lat = min(min_lat, lat)
                if lon != "Desconocido":
                    max_lon = max(max_lon, lon)
                    min_lon = min(min_lon, lon)
            puntos_subred = al.new_list()
            total_nodos = al.size(al_add)
            indices = list(range(min(3, total_nodos))) + list(range(max(total_nodos - 3, 0), total_nodos))
            for idx in indices:
                v = al.get_element(al_add, idx)
                vert = dg.get_vertex(grafo, v)
                info = vert["value"]
                lat = info["lat"] if "lat" in info else "Desconocido"
                lon = info["lon"] if "lon" in info else "Desconocido"
                tags = info["tag_identifiers"] if "tag_identifiers" in info else al.new_list()
                n_individuos = al.size(tags)
                primeros3 = al.new_list()
                ultimos3 = al.new_list()
                for a in range(min(3, n_individuos)):
                    al.add_last(primeros3, al.get_element(tags, a))
                for b in range(max(0, n_individuos - 3), n_individuos):
                    al.add_last(ultimos3, al.get_element(tags, b))
                al.add_last(puntos_subred, {
                    "nid": v,
                    "lat": lat,
                    "lon": lon,
                    "n_individuos": n_individuos,
                    "primeros_3": primeros3,
                    "ultimos_3": ultimos3
                })
            al.add_last(subredes, {
                "subred_id": subred_id,
                "max_lat": max_lat,
                "min_lat": min_lat,
                "max_lon": max_lon,
                "min_lon": min_lon,
                "total_puntos": al.size(al_add),
                "puntos": puntos_subred,
                "total_individuos": total_individuos
            })
            subred_id += 1
        i += 1

    if al.size(subredes) == 0:
        return {"mensaje": "No se identificaron subredes hídricas", "subredes": None}

    subredes_list = subredes["elements"]
    subredes_list.sort(key=lambda x: (-x["total_puntos"], x["subred_id"]))
    top_subredes = al.new_list()
    for idx in range(min(5, len(subredes_list))):
        al.add_last(top_subredes, subredes_list[idx])

    return {
        "total_subredes": al.size(subredes),
        "top_subredes": top_subredes
    }
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
