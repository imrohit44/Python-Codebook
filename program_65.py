def knapsack(items, capacity):
    memo = {}

    def solve(index, current_capacity):
        if index >= len(items) or current_capacity <= 0:
            return 0, []
        
        if (index, current_capacity) in memo:
            return memo[(index, current_capacity)]

        item = items[index]
        weight, value = item['weight'], item['value']

        # Case 1: Exclude the current item
        max_value_exclude, items_exclude = solve(index + 1, current_capacity)
        
        # Case 2: Include the current item if capacity allows
        if weight <= current_capacity:
            max_value_include, items_include = solve(index + 1, current_capacity - weight)
            max_value_include += value
            items_include = [item] + items_include
            
            if max_value_include > max_value_exclude:
                memo[(index, current_capacity)] = (max_value_include, items_include)
                return max_value_include, items_include

        memo[(index, current_capacity)] = (max_value_exclude, items_exclude)
        return max_value_exclude, items_exclude

    return solve(0, capacity)

if __name__ == "__main__":
    items = [
        {'id': 'A', 'weight': 5, 'value': 10},
        {'id': 'B', 'weight': 4, 'value': 8},
        {'id': 'C', 'weight': 6, 'value': 12},
        {'id': 'D', 'weight': 3, 'value': 7}
    ]
    capacity = 10
    
    max_value, selected_items = knapsack(items, capacity)
    print(f"Max value: {max_value}")
    print(f"Selected items: {[item['id'] for item in selected_items]}")