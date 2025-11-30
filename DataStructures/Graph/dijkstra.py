from DataStructures.Map import map_linear_probing as lp
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Graph import dijsktra_structure as ds
from DataStructures.Graph import digraph as dp
from DataStructures.List import array_list as al
from DataStructures.Graph import vertex as vt
from DataStructures.Graph import edge as eg
from DataStructures.Stack import stack as st
import math 


def init_structure(graph, source):
    """
    Crea e inicializa la estructura utilizada para construcción del árbol de caminos
    de costo mínimo (Algoritmo de Dijkstra) a partir del vértice source
    """
    structure = ds.new_dijsktra_structure(source,lp.size(graph["vertices"]))
    vertices = dp.vertices(graph)

    for i in range(al.size(vertices)):
        vert = al.get_element(vertices, i)
        lp.put(structure["visited"], vert, {
            "marked": False,
            "edge_from": None,
            "dist_to": math.inf
        })

    lp.put(structure["visited"], source, {
        "marked": False,
        "edge_from": None,
        "dist_to": 0
    })

    pq.insert(structure["pq"], source, 0)
    return structure

def dijkstra(graph,source):
    if lp.contains(graph["vertices"],source):
        structure = init_structure(graph, source)
        while not pq.is_empty(structure["pq"]):
            key_priority = pq.get_first_priority(structure["pq"])
            pq.remove(structure["pq"])
            marked = lp.get(structure["visited"],key_priority)
            marked["marked"] = True
            lp.put(structure["visited"],key_priority,marked)
            adyacentes = dp.adjacents(graph,key_priority)
            i = 0
            while i < al.size(adyacentes):
                sub = al.get_element(adyacentes,i)
                vertice = lp.get(structure["visited"],sub)
                if not vertice["marked"]:
                    nodo = lp.get(graph["vertices"],key_priority)
                    weight = vt.get_edge(nodo,sub)
                    new_distance = marked["dist_to"] + eg.weight(weight)
                    if new_distance < vertice["dist_to"]:
                        verti = lp.get(structure["visited"],sub)
                        verti["dist_to"] = new_distance
                        verti["edge_from"] = key_priority
                        lp.put(structure["visited"],sub,verti)
                        pq.insert(structure["pq"], sub, new_distance)
                i +=1
        return structure

def dist_to(key_v,aux_structure):
    vertice = lp.get(aux_structure["visited"],key_v)
    if vertice is None:
        return None
    return vertice["dist_to"]


def has_path_to(key_v,aux_structure):
    vertice = lp.get(aux_structure["visited"],key_v)
    if vertice is None:
        return None
    return vertice["marked"]

def path_to(key_v,aux_structure):
    if has_path_to(key_v,aux_structure):
        path = st.new_stack()
        st.push(path,key_v)
        while lp.get(aux_structure["visited"],key_v)["edge_from"] is not None:
            key_u = lp.get(aux_structure["visited"],key_v)["edge_from"]
            st.push(path,key_u)
            key_v = key_u
        return path
    else:
        return None
        
