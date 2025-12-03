from DataStructures.Graph import dfo_structure as df
from DataStructures.Map import map_linear_probing as map
from DataStructures.Graph import digraph as dg
from DataStructures.List import array_list as al
from DataStructures.Queue import queue
from DataStructures.Stack import stack

def dfo (my_graph):
    g_order = dg.order(my_graph)
    aux_structure = df.new_dfo_structure(g_order)
    vertices = dg.vertices(my_graph)
    i = 1
    while i <= al.size(vertices):
        v = al.get_element(vertices, i)
        entry = map.get(aux_structure["marked"], v)
        if entry is None:
            dfs_vertex(my_graph, v, aux_structure)
        i += 1
    return aux_structure


def dfs_vertex(my_graph, key_v, aux_structure):
    map.put(aux_structure["marked"], key_v, True)
    queue.enqueue(aux_structure["pre"], key_v)
    adj_list = dg.adjacents(my_graph, key_v)
    j = 1
    while j <= al.size(adj_list):
        w = al.get_element(adj_list, j)
        entry = map.get(aux_structure["marked"], w)
        if entry is None:
            dfs_vertex(my_graph, w, aux_structure)
        j += 1
    queue.enqueue(aux_structure["post"], key_v)
    stack.push(aux_structure["reversepost"], key_v)