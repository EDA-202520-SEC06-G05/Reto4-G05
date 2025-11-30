
from DataStructures.List import single_linked_list as sl

def new_queue():
    queue = {
        "first": None,
        "last": None,
        "size": 0,
    }
    return queue

def enqueue(my_queue, element):
    final_queue = sl.add_last(my_queue, element)
    return final_queue

def dequeue(my_queue):
    if my_queue["size"] == 0:
        raise Exception("EmptyStructureError: queue is empty")
    else:
        result = my_queue["first"]["info"]
        final_queue = sl.remove_first(my_queue)
        return result

def is_empty(my_queue):
    confirmation = sl.is_empty(my_queue)
    return confirmation

def peek(my_queue):
    if my_queue["size"] == 0:
        raise Exception('EmptyStructureError: queue is empty')
    else:
        first = sl.first_element(my_queue)    
        return first

def size(my_queue):
    result = sl.size(my_queue)
    return result



