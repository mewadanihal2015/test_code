class Player:
    def __init__(self, player_id, controller_id):
        self.player_id = player_id
        self.controller_id = controller_id

        self.x = 0.0
        self.y = 0.0
        self.speed = 5.0
        self.is_jumping = False

    def update(self, input_manager):
        move_x = input_manager.get_player_action(self.controller_id, "MOVE_X")
        move_y = input_manager.get_player_action(self.controller_id, "MOVE_Y")
        jump = input_manager.get_player_action(self.controller_id, "JUMP")

        self.x += move_x * self.speed
        self.y += move_y * self.speed

        if jump and not self.is_jumping:
            self.is_jumping = True
            print(f"Player {self.player_id} JUMP!")

        if not jump:
            self.is_jumping = False
