from DataStructures.Graph import prim_structure as pr
from DataStructures.List import array_list as lt
from DataStructures.Graph import digraph as dg
from DataStructures.Map import map_linear_probing as map 
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Graph import vertex as vt

def edges_mst(graph, prim_estructura):
    """
    Retornar la lista con los arcos que componen el MST resultante a partir del
    resultado obtenido por el algoritmo Prim Eager en la estructura prim_estructura
    """
    edges = lt.new_list()
    vertices = dg.vertices(graph)
    for i in range(lt.size(vertices)):
        vert = lt.get_element(vertices, i)
        info_vert = map.get(prim_estructura["visited"], vert)
        if (info_vert is not None) and (info_vert["marked"] is True) and (info_vert["edge_from"] is not None):
            lt.add_last(edges, {"edge_from":info_vert["edge_from"], "to":vert, "dist_to":info_vert["dist_to"]})
        return edges
    
def weight_mst(graph, prim_estructura):
    """
    Retornar el peso del MST resultante a partir del resultado obtenido por
    el algoritmo Prim Eager en la estructura prim_estructura
    """
    weight = 0.0
    vertices = dg.vertices(graph)
    i = 1
    while i <= lt.size(vertices):
        vert = lt.get_element(vertices, i)
        entry = map.get(prim_estructura["visited"], vert)
        if entry is not None:
            info_vert = entry["value"]
            if (info_vert["marked"] is True) and (info_vert["edge_from"] is not None):
                weight += info_vert["dist_to"]
        i += 1
    return weight

def prim_mst(graph, source):
    order = dg.order(graph)
    prim_structure = pr.new_prim_structure(source, order)

    if not dg.contains_vertex(graph, source):
        return prim_structure

    visited = prim_structure["visited"]
    pq_heap = prim_structure["pq"]

    map.put(visited, source, {
        "marked": False,
        "dist_to": 0.0,
        "edge_from": None
    })

    pq.insert(pq_heap, source, 0.0)

    while not pq.is_empty(pq_heap):
        v = pq.get_first_priority(pq_heap)
        pq.remove(pq_heap)

        entry_v = map.get(visited, v)
        if entry_v is None:
            continue
        info_v = entry_v["value"]
        if info_v["marked"]:
            continue
        info_v["marked"] = True

        vertex_v = dg.get_vertex(graph, v)
        if vertex_v is None:
            continue

        adj_map = vt.get_adjacents(vertex_v)
        table = adj_map["table"]["elements"]

        for slot in table:
            if slot is None:
                continue

            w = slot["key"]
            edge_vw = slot["value"]
            weight = edge_vw["weight"]

            entry_w = map.get(visited, w)
            if entry_w is None:
                map.put(visited, w, {
                    "marked": False,
                    "dist_to": weight,
                    "edge_from": v
                })
                pq.insert(pq_heap, w, weight)
            else:
                info_w = entry_w["value"]
                if not info_w["marked"] and weight < info_w["dist_to"]:
                    info_w["dist_to"] = weight
                    info_w["edge_from"] = v
                    pq.insert(pq_heap, w, weight)

    return prim_structure