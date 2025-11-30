from DataStructures.List import single_linked_list as all

def new_stack ():
    
    new_stack = all.new_list()
    return new_stack 

def push (my_stack, element):
    all.add_first(my_stack, element)
    return my_stack 

def is_empty(my_stack):
    return all.is_empty(my_stack)


def pop (my_stack):
    
    if is_empty(my_stack) != True:
        tope_stack = my_stack["first"]["info"]
        all.remove_first(my_stack)
        
    else:
        tope_stack = ("EmptyStructureError: stack is empty.")
        
    return tope_stack

def top (my_stack):
    
    if is_empty(my_stack) != True:
        tope_stack = my_stack["first"]["info"]
    else:
        tope_stack = ("EmptyStructureError: stack is empty.")
    return tope_stack

def size (my_stack):
    return my_stack["size"]
