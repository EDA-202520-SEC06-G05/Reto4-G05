from DataStructures.Map import map_linear_probing as map
from DataStructures.List import array_list as lt
from DataStructures.Queue import queue as q
from DataStructures.Stack import stack as st
from DataStructures.Graph import digraph as G

def bfs(my_graph, source):
    visited= map.new_map(
        num_elements=G.order(my_graph),
        load_factor=0.5)
    map.put(visited,source,{
        "edge_from": None,
        "dist_to": 0})
    return bfs_vertex(my_graph, source, visited)

def bfs_vertex(my_graph, source, visited_map):
    cola = q.new_queue()
    q.enqueue(cola, source)
    while not q.is_empty(cola):
        v=q.dequeue(cola)
        adj=G.adjacents(my_graph, v)
        for i in range(lt.size(adj)):
            w=lt.get_element(adj, i)
            if not map.contains(visited_map, w):
                info_v=map.get(visited_map, v)
                dist=info_v["dist_to"] + 1
                map.put(visited_map, w,{
                    "edge_from":v,
                    "dist_to":dist})
                q.enqueue(cola, w)
    return visited_map

def has_path_to(key_v, visited_map):
    return map.contains(visited_map,key_v)

def path_to(key_v, visited_map):
    if not has_path_to(key_v,visited_map):
        return None
    camino=st.new_stack()
    actual=key_v
    while actual is not None:
        st.push(camino, actual)
        info=map.get(visited_map, actual)
        actual=info["edge_from"]
    return camino