class TransformDescriptor:
    def __init__(self, transformer):
        self.transformer = transformer # Function (normalize, denormalize)
        self.name = None

    def __set_name__(self, owner, name):
        self.name = f'_{name}_normalized'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        
        normalized_value = getattr(obj, self.name, None)
        if normalized_value is None:
            return None
            
        return self.transformer[1](normalized_value)

    def __set__(self, obj, value):
        normalized_value = self.transformer[0](value)
        setattr(obj, self.name, normalized_value)

# Transformer functions:
def normalize_name(name):
    return name.lower().replace(' ', '_')

def denormalize_name(normalized):
    return normalized.replace('_', ' ').title()

class UserProfile:
    # Tuple: (Normalization function, Denormalization function)
    username = TransformDescriptor((normalize_name, denormalize_name))

    def __init__(self, name):
        self.username = name

if __name__ == '__main__':
    profile = UserProfile("JAnE dOe")
    
    print(f"Set Value: JAnE dOe")
    print(f"Internal (Normalized): {profile._username_normalized}")
    print(f"Get Value (Denormalized): {profile.username}")