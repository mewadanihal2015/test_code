"""
High-level input manager that maps controller inputs to game actions.
Designed to work alongside controllers.py
"""

from collections import defaultdict

# Example action mapping (can be customized per controller type)
DEFAULT_BINDINGS = {
    "JUMP": ("button", 0),      # A / Cross
    "SHOOT": ("button", 1),     # B / Circle
    "DASH": ("button", 2),      # X / Square
    "PAUSE": ("button", 7),     # Start
    "MOVE_X": ("axis", 0),      # Left stick X
    "MOVE_Y": ("axis", 1),      # Left stick Y
}

class PlayerInput:
    def __init__(self, controller_id, bindings=None):
        self.controller_id = controller_id
        self.bindings = bindings or DEFAULT_BINDINGS
        self.actions = defaultdict(float)

    def handle_button(self, button, pressed):
        for action, (atype, index) in self.bindings.items():
            if atype == "button" and index == button:
                self.actions[action] = 1.0 if pressed else 0.0

    def handle_axis(self, axis, value, deadzone=0.2):
        if abs(value) < deadzone:
            value = 0.0

        for action, (atype, index) in self.bindings.items():
            if atype == "axis" and index == axis:
                self.actions[action] = value

    def get(self, action):
        return self.actions.get(action, 0.0)


class InputManager:
    def __init__(self):
        self.players = {}

    def add_player(self, controller_id):
        self.players[controller_id] = PlayerInput(controller_id)
        print(f"[PLAYER ASSIGNED] Controller {controller_id}")

    def remove_player(self, controller_id):
        self.players.pop(controller_id, None)
        print(f"[PLAYER REMOVED] Controller {controller_id}")

    def button_event(self, controller_id, button, pressed):
        if controller_id in self.players:
            self.players[controller_id].handle_button(button, pressed)

    def axis_event(self, controller_id, axis, value):
        if controller_id in self.players:
            self.players[controller_id].handle_axis(axis, value)

    def get_player_action(self, controller_id, action):
        if controller_id in self.players:
            return self.players[controller_id].get(action)
        return 0.0
