import pygame
import time
import serial

ser = serial.Serial('/dev/rfcomm0', 9600)

pygame.init()

direction = 'R'
direction_LR = 'R'
loop_counter = 0
divider = 10

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

#default values of robot not moving anyway
speed = 74
turn = 56
joystick_values = []

# -------- Main Program Loop -----------
while done == False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()

        # Main part of the program, joystick axis values are being read then CCR3 register value
        # is being calculated and finally it if sent via serial to the robot.
        for i in range(axes):
            axis = joystick.get_axis(i)
            joystick_values.append(joystick.get_axis(i))
        # print(joystick_values[0])

        '''
        joystick_values[0] - right <-> left
        joystick_values[1] - front <-> back
        '''
        #ccr_speed = 74 + int(joystick_values[0] * 15) # not used here, calculated in STM32
        #ccr_turn = 56 + int(joystick_values[1] * 15)  # not used here, calculated in STM32

        speed = 50 + int(joystick_values[1] * 50) # joystick values are from -1 to 1
        turn = 50 + int(joystick_values[0] * 50)
        # print(speed) #debugggg

        # Calculate speed values
        if joystick_values[1] <= 0:
            direction = 'F'
            speed = int((-100) * joystick_values[1])
            if speed == 100:
                speed -= 1
            elif 0 < speed < 10:
                speed = 10

        elif joystick_values[1] > 0:
            direction = 'R'
            speed = int(100 * joystick_values[1])
            if speed == 100:
                speed -= 1
            elif 0 < speed < 10:
                speed = 10
        else:
            print('***Error: Unknown speed joystick value!***')

        # Calculate turn values
        if joystick_values[0] <= 0:
            direction_LR = 'L'
            turn = int((-100) * joystick_values[0])
            if turn == 100:
                turn -= 1
            elif 0 < turn < 10:
                turn = 0
            # print(turn)

        elif joystick_values[0] > 0:
            direction_LR = 'R'
            turn = int(100 * joystick_values[0])
            if turn == 100:
                turn -= 1
            elif 0 < turn < 10:
                turn = 0
        else:
            print('***Error: Unknown turn joystick value!***')

        # Create string variables for speed to be sent to robot
        if direction == 'R':
            if speed == 0:
                message_speed = 'sr00'
                message_speed_byte = b'sr00'
            else:
                message_speed = str('sr' + str(speed))
                message_speed_byte = str.encode(message_speed)
            if loop_counter % divider == 0:
                ser.write(message_speed_byte)
        elif direction == 'F':
            if speed == 0:
                message_speed = 'sf00'
                message_speed_byte = b'sf00'
            else:
                message_speed = str('sf' + str(speed))
                message_speed_byte = str.encode(message_speed)
            if loop_counter % divider == 0:
                ser.write(message_speed_byte)
        else:
            message_speed = 'sf00'
            message_speed_byte = b'sf00'
            if loop_counter % divider == 0:
                ser.write(message_speed_byte)

        # Create string variables for turn to be sent to robot
        if direction_LR == 'R':
            if turn == 0:
                message_turn = 'tr00'
                message_turn_byte = b'tr00'
            else:
                message_turn = str('tr' + str(turn))
                message_turn_byte = str.encode(message_turn)
            if loop_counter % divider == 0:
                ser.write(message_turn_byte)
            # print(message_turn)

        elif direction_LR == 'L':
            if turn == 0:
                message_turn = 'tl00'
                message_turn_byte = b'tl00'
            else:
                message_turn = str('tl' + str(turn))
                message_turn_byte = str.encode(message_turn)
            if loop_counter % divider == 0:
                ser.write(message_turn_byte)
        else:
            message_turn = 'tl00'
            message_turn_byte = b'tl00'
            if loop_counter % divider == 0:
                ser.write(message_turn_byte)

        # print(message_speed)
        joystick_values.clear()
        # time.sleep(0.01)
        loop_counter += 1
        '''
        buttons = joystick.get_numbuttons()

        for i in range(buttons):
            button = joystick.get_button(i)

       
        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()

        for i in range(hats):
            hat = joystick.get_hat(i)
        '''
    # Limit to 20 frames per second
    #clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()