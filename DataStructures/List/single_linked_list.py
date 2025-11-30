from DataStructures.List import list_node as nd
from DataStructures.List import single_linked_list as sl

def new_list():
    newlist = {
        "first": None,
        "last": None,
        "size": 0,
    }
    return newlist


def get_element(my_list, pos):
    searchpos = 0
    node = my_list["first"]
    while searchpos < pos :
        node = node["next"]
        searchpos += 1
    return node["info"] 

def is_present(my_list, element, cmp_function):
    is_in_array = False
    temp = my_list["first"]
    count = 0
    while not is_in_array and temp is not None:
        if cmp_function(element, temp["info"]) == 0:
            is_in_array = True
        else:
            temp = temp["next"]
            count +=1
            
    if not is_in_array:
        count = -1
    return count

def add_first(my_list, element):
    
    nodo = nd.new_single_node(element)
    if my_list ["first"] is None:
        my_list["first"] = nodo
        my_list["last"] = nodo
        
    else:
        nodo["next"] = my_list["first"]
        my_list["first"] = nodo
    my_list["size"] += 1
    
    return my_list

def add_last(my_list, element):
    
    nodo = nd.new_single_node(element)
    if my_list["first"] is None:
        my_list["first"] = nodo
        my_list["last"] = nodo
        
    else:
        my_list["last"]["next"] = nodo
        my_list["last"] = nodo
    my_list["size"] += 1
    
    return my_list

def size(my_list):
    
    return my_list["size"]

def first_element(my_list):

    first_element = None
    if my_list["first"] is None:
        first_element = "IndexError list index out of range"
        
    else:
        first_element = my_list["first"]["info"]
        
    return first_element

def last_element(my_list):
    
    last_element = None
    if my_list["last"] is None:
        last_element = "IndexError list index out of range"
        
    else:
        last_element = my_list["last"]["info"]
        
    return last_element

def is_empty (my_list):
    empty = None
    if my_list["first"] is None:
        empty = True
        
    else:
        empty = False
    return empty

def delete_element(my_list,pos):
    
    if (pos >= 0) and (pos < my_list["size"]):
        if pos == 0:
            my_list["first"] = my_list["first"]["next"]
            my_list["size"] -= 1
            
            if my_list["first"] is None:
                my_list["last"] = None
                my_list["size"] = 0
            
        else:
            nodo = my_list["first"]
            pos -=1
            while pos > 0:
                nodo = nodo["next"]
                pos -= 1
            prev = nodo ["next"]
            nodo["next"] = prev["next"]
            my_list["size"] -= 1
            
            if nodo["next"] is None:
                my_list["last"] = nodo
    else:
        return "IndexError list index out of range"
    return my_list

def remove_first(my_list):
    
    if my_list["first"] is None:
        return "IndexError list index out of range"
    else:
        my_list["first"] = my_list["first"]["next"]
        my_list["size"] -= 1
        if my_list["first"] is None:
            my_list["last"] = None
        
    return my_list

def remove_last(my_list):
    
    if my_list["first"] is None:
        return "IndexError list index out of range"
    
    elif my_list["size"] == 1:
        my_list["first"] = None
        my_list["last"] = None
        my_list["size"] = 0 
        
    else:
        pre_list = my_list["first"]
        while pre_list["next"] is not my_list["last"]:
            pre_list = pre_list["next"]
        pre_list["next"] = None
        my_list["last"] = pre_list
        my_list["size"] -= 1
        
    return my_list

def insert_element(my_list, element, pos):
    
    if (pos >= 0) and (pos <= my_list["size"]):
        if pos == 0:
            add_first(my_list, element)
        elif pos == my_list["size"]:
            add_last(my_list, element)
        else:
            nodo = nd.new_single_node(element)
            contador = 0
            pos_list = my_list["first"]
            pre_list = None
            while pos  > contador :
                pre_list = pos_list
                pos_list = pos_list["next"]
                contador += 1
            pre_list["next"] = nodo
            nodo["next"] = pos_list
        my_list["size"] += 1
    else:
        return "IndexError list index out of range"
    
    return my_list

def change_info(my_list, element, pos ):
    
    if (pos >= 0) and (pos < my_list["size"]):
            nodo = my_list["first"]
            contador = 0
            while contador < pos:
                nodo = nodo["next"]
                contador += 1
            nodo["info"] = element
    else:
        return "IndexError list index out of range"
    return my_list

def exchange(my_list, pos1, pos2):
    if (pos1 >= 0 and pos1 < my_list["size"]) and (pos2 >= 0 and pos2 < my_list["size"]):
        if pos1 == pos2:
            return my_list
        nodo1 = my_list["first"]
        contador1 = 0
        while contador1 < pos1:
            nodo1 = nodo1["next"]
            contador1 += 1

        nodo2 = my_list["first"]
        contador2 = 0
        while contador2 < pos2:
            nodo2 = nodo2["next"]
            contador2 += 1

        reference = nodo1["info"]
        nodo1["info"] = nodo2["info"]
        nodo2["info"]= reference
        return my_list
    else:
        return "IndexError list index out of range"

def sub_list(my_list, pos, num_elements ):
    new = new_list()
    if (pos >= 1) and (pos <= my_list["size"]):  # índices desde 1
        elements = my_list["first"]
        count = 1
        while count < pos and elements is not None:
            elements = elements["next"]
            count += 1
        while num_elements > 0 and elements is not None:
            add_last(new, elements["info"])
            elements = elements["next"]
            num_elements -= 1
    return new

def default_sort_criteria(element1, element2):
    return element1 <= element2

def selection_sort(my_list, sort_criteria):
    
    if my_list["first"] is None or my_list["size"]<=1:
        return my_list
    else:
        current = my_list["first"]
        while current is not None:
            min_node = current
            siguien = current["next"]
            while siguien is not None:
                if not sort_criteria(min_node["info"], siguien["info"]):
                    min_node = siguien
                siguien = siguien["next"]
            
            if min_node is not siguien:
                current["info"], min_node["info"] = min_node["info"], current["info"]
            
            current = current["next"]
        return my_list

def insertion_sort(my_list, sort_criteria):
    
    
    if my_list["first"] is None or my_list["first"]["next"]:
        return my_list
    sort_head = None
    current = my_list["first"]
    while current is not None:
        next_node = current["next"]
            
        if sort_head is None or not sort_criteria(sort_criteria["info"], current["info"]):
            current["next"] = sort_head
            sort_head = current
        else:
            search = sort_head
            while search["next"] is not None and sort_criteria(search["next"]["info"], current["info"]):
                search = search["next"]
                current["next"] = search["next"]
                search["next"] = current
        current = next_node
    my_list["first"] = sort_head
    last_node = sort_head
    while last_node["next"] is not None:
        last_node = last_node["next"]
    my_list["last"] = last_node
    
    return my_list