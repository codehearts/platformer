from physical_objects import physicalobject, simpleai
from resources import demo_sprites

# @TODO We need our own test_object tileset

# Bestiary of all non-playable characters in the game
look_up = {
    # No gravity
    'test_object_1': {
        'class': physicalobject.PhysicalObject,
        'img': demo_sprites.floating,
        'mass': 0
    },
    
    # No gravity
    'test_object_2': {
        'class': physicalobject.PhysicalObject,
        'img': demo_sprites.floating,
        'mass': 0
    },
    
    # No gravity
    'test_object_3': {
        'class': physicalobject.PhysicalObject,
        'img': demo_sprites.floating,
        'mass': 0
    },
    
    # 1 mass
    'test_object_4': {
        'class': physicalobject.PhysicalObject,
        'img': demo_sprites.floating,
        'mass': 1
    },
    
    # Incredibly heavy
    'test_object_5': {
        'class': physicalobject.PhysicalObject,
        'img': demo_sprites.floating,
        'mass': 10000
    },
    
    # 100 mass
    'test_object_6': {
        'class': simpleai.SimpleAI,
        'img': demo_sprites.floating,
        'mass': 100
    }
}