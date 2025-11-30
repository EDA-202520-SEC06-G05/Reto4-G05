from DataStructures.Map import map_linear_probing as lp
from DataStructures.Graph import vertex as vt
from DataStructures.Graph import edge as ed
from DataStructures.List import array_list as al

def new_graph(order):
    graph = {
        "vertices": lp.new_map(order, 0.7, None),
        "num_edges": 0
    }
    return graph

def insert_vertex(my_graph, key_u, info_u):
    vertex = vt.new_vertex(key_u, info_u)
    lp.put(my_graph["vertices"], key_u, vertex)
    return my_graph

def add_edge(my_graph, key_u, key_v, weight=1.0):
    vertex_u = lp.get(my_graph["vertices"], key_u)
    if vertex_u is None:
        raise Exception("El vertice u no existe")
    vertex_v = lp.get(my_graph["vertices"], key_v)
    if vertex_v is None:
        raise Exception("El vertice v no existe")
    edge_u_and_v = vt.get_edge(vertex_u, key_v)
    if edge_u_and_v is None:
        vt.add_adjacent(vertex_u, key_v, weight)
        my_graph["num_edges"]+=1
    else:
        ed.set_weight(edge_u_and_v, weight)
    return my_graph

def contains_vertex(my_graph, key_u):
    key = lp.get(my_graph["vertices"], key_u)
    if key is not None:
        return True
    else:
        return False

def order(my_graph):
    return my_graph["vertices"]["size"]

def size(my_graph):
    return my_graph["num_edges"]

def degree(my_graph, key_u):
    
    key = lp.get(my_graph["vertices"], key_u)
    if key is None:
        raise Exception("El vertice no existe")
    else:
        return vt.degree(key)

def adjacents(my_graph, key_u):
    lista = al.new_list()
    key = lp.get(my_graph["vertices"], key_u)
    if key is None:
        return lista
    else:
        adjacent = vt.get_adjacents(key)
        table = adjacent["table"]["elements"]
        for each in table:
            al.add_last(each["key"])
        return lista

def vertices(my_graph):
    lista = al.new_list()
    table = my_graph["vertices"]["table"]["elements"]
    for each in table:
        if each["key"] is not None:
            al.add_last(lista, each["key"])
    return lista

def edges_vertex(my_graph, key_u):  
    
    if not contains_vertex(my_graph, key_u):
        raise Exception("El vertice u no existe")
    
    vertex_u = lp.get(my_graph["vertices"], key_u)
    adj_map = vertex_u["adjacents"]
    lista = al.new_list()
    table = adj_map["table"]["elements"]
    for entry in table:
        if entry is not None:
            if entry["key"] is not None:
                al.add_last(lista,(key_u,entry["key"],entry["weight"]))  
    return lista

def get_vertex(my_graph, key_u):
    
    if contains_vertex(my_graph, key_u) == False:
        return None
    else:
        vertex = lp.get(my_graph["vertices"], key_u)
        return vertex

def update_vertex_info(my_graph, key_u, new_info_u):
    
    vertex = get_vertex(my_graph, key_u)
    if vertex is None:
        return my_graph
    
    vertex["value"]["value"] = new_info_u
    lp.put(my_graph["vertices"], key_u, vertex)
    return my_graph

def get_vertex_information(my_graph, key_u):
    
    vertex = get_vertex(my_graph, key_u)
    if vertex is None:
        raise Exception("El vertice no exitse")
    else:
        vertex_info = vertex["value"]
        return vertex_info



