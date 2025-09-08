import sys

class TrackedObject:
    def __init__(self, obj):
        self.obj = obj
        self.ref_count = 1

def inc_ref(tracked_obj):
    if isinstance(tracked_obj, TrackedObject):
        tracked_obj.ref_count += 1

def dec_ref(tracked_obj):
    if isinstance(tracked_obj, TrackedObject):
        tracked_obj.ref_count -= 1

def collect_garbage(tracked_objects):
    collected = [obj for obj in tracked_objects if obj.ref_count <= 0]
    for obj in collected:
        print(f"Collecting: {obj.obj}")
    
    return [obj for obj in tracked_objects if obj.ref_count > 0]

if __name__ == "__main__":
    objects_list = []
    
    obj_a = TrackedObject("Object A")
    obj_b = TrackedObject("Object B")
    
    objects_list.append(obj_a)
    objects_list.append(obj_b)

    inc_ref(obj_a)
    inc_ref(obj_b)
    inc_ref(obj_a)

    dec_ref(obj_a)
    dec_ref(obj_b)

    print("--- Before Collection ---")
    print(f"Object A ref count: {obj_a.ref_count}")
    print(f"Object B ref count: {obj_b.ref_count}")

    objects_list = collect_garbage(objects_list)

    print("--- After Collection ---")
    print(f"Object A is in list: {obj_a in objects_list}")
    print(f"Object B is in list: {obj_b in objects_list}")

    dec_ref(obj_a)
    objects_list = collect_garbage(objects_list)
    
    print(f"Object A is in list: {obj_a in objects_list}")