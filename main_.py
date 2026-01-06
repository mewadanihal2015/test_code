import pygame
import time

from controllers import controllers
from input_manager import InputManager
from game_state import GameState

pygame.init()
pygame.joystick.init()

input_manager = InputManager()
game_state = GameState(input_manager)

print("Game running...")

try:
    while True:
        for event in pygame.event.get():

            if event.type == pygame.JOYDEVICEADDED:
                joystick = pygame.joystick.Joystick(event.device_index)
                joystick.init()
                cid = joystick.get_instance_id()

                input_manager.add_player(cid)
                game_state.add_player(cid)

            elif event.type == pygame.JOYDEVICEREMOVED:
                input_manager.remove_player(event.instance_id)
                game_state.remove_player(event.instance_id)

            elif event.type == pygame.JOYBUTTONDOWN:
                input_manager.button_event(event.instance_id, event.button, True)

            elif event.type == pygame.JOYBUTTONUP:
                input_manager.button_event(event.instance_id, event.button, False)

            elif event.type == pygame.JOYAXISMOTION:
                input_manager.axis_event(event.instance_id, event.axis, event.value)

        game_state.update()
        time.sleep(0.016)  # ~60 FPS

except KeyboardInterrupt:
    print("Shutting down...")
finally:
    pygame.quit()
