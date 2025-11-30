from DataStructures.Priority_queue import pq_entry as pqe
from DataStructures.List import array_list as al

def default_compare_higher_value(father_node, child_node):
    if pqe.get_priority(father_node) >= pqe.get_priority(child_node):
        return True
    return False

def default_compare_lower_value(father_node, child_node):
    if pqe.get_priority(father_node) <= pqe.get_priority(child_node):
        return True
    return False

def new_heap(is_min_pq = True):
    
    new = {
        "elements": al.new_list(),
        "size": 0,
        "cmp_function": None
    }
    if is_min_pq == True:
        new["cmp_function"] = default_compare_lower_value
    elif is_min_pq == False:
        new["cmp_function"] = default_compare_higher_value
        
    al.add_last(new["elements"],None)
    return new   

def insert(my_heap,priority,value):
    new_pq = pqe.new_pq_entry(priority,value)
    al.add_last(my_heap["elements"],new_pq)
    my_heap["size"] += 1
    swim(my_heap,my_heap["size"])
    
    return my_heap

def is_empty(my_heap):
    return my_heap["size"] == 0 

def priority(my_heap, i,j):
    cmp_func=my_heap["cmp_function"]
    element_i = al.get_element(my_heap["elements"],i)
    element_j = al.get_element(my_heap["elements"],j)
    return cmp_func(element_i, element_j)

def exchange(my_heap, i, j):
    temp_i = al.get_element(my_heap["elements"],i)
    temp_j = al.get_element(my_heap["elements"],j)
    my_heap["elements"]=al.change_info(my_heap["elements"],i,temp_j)
    my_heap["elements"]=al.change_info(my_heap["elements"],j,temp_i)
    return my_heap

def swim(my_heap, pos):
    centinela = True
    while pos> 1 and centinela:
        parent= pos//2
        if not priority(my_heap, parent, pos):
            my_heap= exchange(my_heap, parent, pos)
            pos= parent
        else:
            centinela = False
    return my_heap

def size(my_heap):
    return my_heap["size"]

def sink(my_heap, pos):
    size = my_heap["size"]
    cmp_func = my_heap["cmp_function"]
    centinela = True
    while 2 * pos <= size and centinela:
        left = 2 * pos
        right = left + 1
        best = left
        if right <= size and cmp_func(al.get_element(my_heap["elements"], right), al.get_element(my_heap["elements"], left)):
            best = right
        if cmp_func(al.get_element(my_heap["elements"], best), al.get_element(my_heap["elements"], pos)):
            exchange(my_heap, pos, best)
            pos = best
        else:
            centinela = False
    return my_heap

def remove(my_heap):
    if my_heap["size"] == 0:
        return None
    else:
        root = my_heap["elements"]["elements"][1]
        last_pos = my_heap["size"]
        my_heap = exchange(my_heap, 1, last_pos)
        delete = al.last_element(my_heap["elements"])
        al.remove_last(my_heap["elements"])
        my_heap["size"] -= 1
        my_heap = sink(my_heap, 1)
        return  delete["value"]

def get_first_priority (my_heap):
    if my_heap["size"] == 0:
        return None
    else:
        return my_heap["elements"]["elements"][1]["value"]

def is_present_value (my_heap,value):
    heap = my_heap["elements"]["elements"]
    contador = -1
    for i in range (1,my_heap["size"] + 1):
        elemento = heap[i]
        if elemento["value"] == value:
            contador = i 
            break
    return  contador

def contains (my_heap, value):
    if is_present_value(my_heap,value) != -1:
        return True 
    else:
        return False

def improve_priority(my_heap, priority, value):
    for i in range(size(my_heap)):
        entry = my_heap["elements"][i]
        if pqe.get_value(entry) == value:
            pqe.set_priority(entry, priority)
            swim(my_heap, i)
            return my_heap   
    return my_heap