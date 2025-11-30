from DataStructures.Map import map_linear_probing as lp
from DataStructures.Graph import digraph as dg
from DataStructures.List import array_list as al
from DataStructures.Stack import stack as st

def dfs(my_graph,source):
    visited_map = lp.new_map(lp.size(my_graph["vertices"]),0.5,None)
    vertice_source= lp.get(my_graph["vertices"],source)
    lp.put(visited_map,vertice_source["key"],{"marked":True,"edge_from":None})
    dfs_vertex(my_graph,vertice_source["key"],visited_map)
    return visited_map

def dfs_vertex(my_graph, vertice_source, visited_map):
    adjacentes_list = dg.adjacents(my_graph,vertice_source)
    if al.size(adjacentes_list)==0:
        return visited_map
    else:
        i = 0
        size = al.size(adjacentes_list)
        while size > i:
            vertice = al.get_element(adjacentes_list,i)
            if not lp.contains(visited_map,vertice):
                lp.put(visited_map,vertice,{"marked":True,"edge_from":vertice_source})
                dfs_vertex(my_graph,vertice,visited_map)
            i+=1
        return visited_map

def has_path_to(key_v, visited_map):
    marked = lp.get(visited_map,key_v)
    if marked is not None:
        if marked["marked"] == True:
            return True
        else:
            return False
    else:
        return "Vertive no existe en el grafo"

def path_to(key_v, visited_map):
    if has_path_to(key_v,visited_map):
        path = st.new_stack()
        st.push(path,key_v)
        while lp.get(visited_map,key_v)["edge_from"] is not None:
            key_u = lp.get(visited_map,key_v)["edge_from"]
            st.push(path,key_u)
            key_v = key_u
        return path
    else:
        return None