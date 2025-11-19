"""
Inspect ResourceNameEnum to understand available resources
"""

from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

def inspect_resources():
    print("=== ResourceNameEnum Inspection ===")
    
    # Get all attributes that don't start with underscore
    resource_items = []
    for attr_name in dir(ResourceNameEnum):
        if not attr_name.startswith('_'):
            attr_value = getattr(ResourceNameEnum, attr_name)
            resource_items.append((attr_name, attr_value))
    
    # Sort and display
    resource_items.sort()
    for name, value in resource_items:
        print(f"{name:30} -> {value}")
    
    print(f"\nTotal resources: {len(resource_items)}")

if __name__ == "__main__":
    inspect_resources()