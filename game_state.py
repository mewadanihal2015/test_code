from player import Player

class GameState:
    def __init__(self, input_manager):
        self.input_manager = input_manager
        self.players = {}
        self.next_player_id = 1

    def add_player(self, controller_id):
        player = Player(self.next_player_id, controller_id)
        self.players[self.next_player_id] = player
        self.next_player_id += 1
        print(f"[GAME] Player {player.player_id} joined")

    def remove_player(self, controller_id):
        for pid, player in list(self.players.items()):
            if player.controller_id == controller_id:
                del self.players[pid]
                print(f"[GAME] Player {pid} left")

    def update(self):
        for player in self.players.values():
            player.update(self.input_manager)
