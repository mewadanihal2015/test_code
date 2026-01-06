import pygame
import time

pygame.init()
pygame.joystick.init()

# Store active controllers
controllers = {}

def add_controller(device_index):
    joystick = pygame.joystick.Joystick(device_index)
    joystick.init()
    controllers[joystick.get_instance_id()] = joystick
    print(f"[CONNECTED] {joystick.get_name()} (id={joystick.get_instance_id()})")

def remove_controller(instance_id):
    joystick = controllers.pop(instance_id, None)
    if joystick:
        print(f"[DISCONNECTED] {joystick.get_name()} (id={instance_id})")

# Initialize already connected controllers
for i in range(pygame.joystick.get_count()):
    add_controller(i)

print("Listening for controller input... (Ctrl+C to quit)")

try:
    while True:
        for event in pygame.event.get():

            # Controller connected
            if event.type == pygame.JOYDEVICEADDED:
                add_controller(event.device_index)

            # Controller disconnected
            elif event.type == pygame.JOYDEVICEREMOVED:
                remove_controller(event.instance_id)

            # Button pressed
            elif event.type == pygame.JOYBUTTONDOWN:
                print(f"[BUTTON DOWN] Controller {event.instance_id}, Button {event.button}")

            # Button released
            elif event.type == pygame.JOYBUTTONUP:
                print(f"[BUTTON UP] Controller {event.instance_id}, Button {event.button}")

            # Axis movement
            elif event.type == pygame.JOYAXISMOTION:
                print(f"[AXIS] Controller {event.instance_id}, Axis {event.axis}, Value {event.value:.2f}")

            # D-pad (hat) movement
            elif event.type == pygame.JOYHATMOTION:
                print(f"[HAT] Controller {event.instance_id}, Hat {event.hat}, Value {event.value}")

        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    pygame.quit()
