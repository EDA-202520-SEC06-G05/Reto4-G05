from DataStructures.Map import map_linear_probing as map
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Queue import queue as q


def new_prim_structure(source, order):
    """
    Definición de la estructura utilizada para construcción del MST (Algoritmo Prim Eager)
    a partir del vértice source
    """

    prim_structure = {
    'source': source, # identificador del vertice inicio del MST
    'visited': map.new_map(order, 0.5,None), # tabla de hash con la información para cada vértice v del MST:
                                    # su estado de marcación ('marked'),
                                    # el costo o distancia del arco escogido para llegar al vértice del MST ('dist_to'),
                                    # el vertice que define al arco para llegar al vertice del MST ('edge_from')
    'pq': pq.new_heap(is_min= False), # cola de prioridad orientada a menor donde se guarda cada vértice con su arco de menor costo
}
    return prim_structure

