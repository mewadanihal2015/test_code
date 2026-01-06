"""
Controller action maps for different controller types
"""

XBOX_MAP = {
    "JUMP": ("button", 0),     # A
    "SHOOT": ("button", 1),    # B
    "DASH": ("button", 2),     # X
    "PAUSE": ("button", 7),    # Start
    "MOVE_X": ("axis", 0),
    "MOVE_Y": ("axis", 1),
}

PLAYSTATION_MAP = {
    "JUMP": ("button", 1),     # Cross
    "SHOOT": ("button", 2),    # Circle
    "DASH": ("button", 0),     # Square
    "PAUSE": ("button", 9),    # Options
    "MOVE_X": ("axis", 0),
    "MOVE_Y": ("axis", 1),
}

GENERIC_MAP = XBOX_MAP
