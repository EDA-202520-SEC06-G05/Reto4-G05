from DataStructures.List import array_list as al
import math

TOMBSTONE = "__EMPTY__"

def new_map(num_elements, load_factor, prime):
    if load_factor <= 0:
        raise ValueError("load_factor debe ser > 0")
    capacity = max(11, int(math.ceil(num_elements / load_factor)))
    table = al.new_list()
    for _ in range(capacity):
        al.add_last(table, {"key": None, "value": None})
    my_map = {
        "capacity": capacity,
        "table": table,
        "size": 0,
        "limit_factor": load_factor,
        "current_factor": 0
    }
    return my_map

def hash_value(my_map, key):
    return abs(hash(key)) % my_map["capacity"]

def find_slot(my_map, key, index):
    table = my_map["table"]["elements"]
    capacity = my_map["capacity"]
    first_avail = None
    while True:
        entry = table[index]
        if entry["key"] is None:
            if first_avail is None:
                first_avail = index
            return False, first_avail
        if entry["key"] == TOMBSTONE:
            if first_avail is None:
                first_avail = index
        if entry["key"] == key:
            return True, index
        index = (index + 1) % capacity

def rehash(my_map):
    old_table = my_map["table"]["elements"]
    old_capacity = my_map["capacity"]
    new_capacity = old_capacity * 2
    table = al.new_list()
    for _ in range(new_capacity):
        al.add_last(table, {"key": None, "value": None})
    my_map["table"] = table
    my_map["capacity"] = new_capacity
    my_map["size"] = 0
    for entry in old_table:
        if entry["key"] is not None and entry["key"] != TOMBSTONE:
            put(my_map, entry["key"], entry["value"])
    my_map["current_factor"] = my_map["size"] / my_map["capacity"]
    return my_map

def put(my_map, key, value):
    idx = hash_value(my_map, key)
    found, pos = find_slot(my_map, key, idx)
    if found:
        my_map["table"]["elements"][pos]["value"] = value
        return my_map
    my_map["table"]["elements"][pos] = {"key": key, "value": value}
    my_map["size"] += 1
    my_map["current_factor"] = my_map["size"] / my_map["capacity"]
    if my_map["current_factor"] > my_map["limit_factor"]:
        rehash(my_map)
    return my_map

def get(my_map, key):
    idx = hash_value(my_map, key)
    found, pos = find_slot(my_map, key, idx)
    if not found:
        return None
    entry = my_map["table"]["elements"][pos]
    if entry["key"] == key:
        return entry["value"]
    return None

def contains(my_map, key):
    return get(my_map, key) is not None

def remove(my_map, key):
    idx = hash_value(my_map, key)
    found, pos = find_slot(my_map, key, idx)
    if not found:
        return False
    entry = my_map["table"]["elements"][pos]
    if entry["key"] != key:
        return False
    entry["key"] = TOMBSTONE
    entry["value"] = None
    my_map["size"] -= 1
    my_map["current_factor"] = my_map["size"] / my_map["capacity"]
    return True

def key_set(my_map):
    lista = al.new_list()
    table = my_map["table"]["elements"]
    for slot in table:
        if slot["key"] is not None and slot["key"] != TOMBSTONE:
            al.add_last(lista, slot["key"])
    return lista

def value_set(my_map):
    lista = al.new_list()
    table = my_map["table"]["elements"]
    for slot in table:
        if slot["key"] is not None and slot["key"] != TOMBSTONE:
            al.add_last(lista, slot["value"])
    return lista

def size(my_map):
    return my_map["size"]

def is_empty(my_map):
    return my_map["size"] == 0