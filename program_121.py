import ctypes

class FixedSizeAllocator:
    def __init__(self, obj_size, num_objects):
        self.obj_size = obj_size
        self.num_objects = num_objects
        self.buffer = bytearray(obj_size * num_objects)
        self.free_list_head = 0
        
        for i in range(num_objects - 1):
            ctypes.c_size_t.from_buffer(self.buffer, i * obj_size).value = (i + 1) * obj_size
        ctypes.c_size_t.from_buffer(self.buffer, (num_objects - 1) * obj_size).value = -1

    def allocate(self):
        if self.free_list_head == -1:
            return None
        
        ptr = self.free_list_head
        self.free_list_head = ctypes.c_size_t.from_buffer(self.buffer, self.free_list_head).value
        return self.buffer[ptr:ptr + self.obj_size]

    def deallocate(self, ptr):
        offset = ptr.address - self.buffer.address
        ctypes.c_size_t.from_buffer(self.buffer, offset).value = self.free_list_head
        self.free_list_head = offset

class MyObject:
    def __init__(self, value):
        self.value = value

if __name__ == '__main__':
    allocator = FixedSizeAllocator(obj_size=16, num_objects=10)
    
    obj_ptr = allocator.allocate()
    if obj_ptr:
        ctypes.c_int.from_buffer(obj_ptr).value = 42
        print(f"Allocated value: {ctypes.c_int.from_buffer(obj_ptr).value}")
        allocator.deallocate(obj_ptr)
        print("Deallocated.")