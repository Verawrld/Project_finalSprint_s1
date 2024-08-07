# Initialize Variables

# Define Booleans for flagging if a point has been passed - Used to solve bringing person back to start problem
point_c_passed = False
point_e_passed = False
point_g_passed = False

# Led Configurations - Seem to have errors setting certain variables
led = led_ctrl
media = media_ctrl
define = rm_define
l1, l2 = 0, 255
second, delay = 1, .1

# RGB red-yellow Matrix
RGB_RY = [
    [],  # empty list box
    [l2, l1, l1],  # RGB Red
    [l2, l2, l1],  # RGB Yellow
    [l2, l1, l1],  # RGB Red
    [l2, l2, l1],  # RGB Yellow
    [l2, l1, l1],  # RGB Red
    [l2, l2, l1],  # RGB Yellow
    [l2, l1, l1],  # RGB Red
    [l2, l2, l1],  # RGB Yellow
]

# RGB-Y Matrix
RGB = [
    [],  # empty list box
    [l2, l1, l1],  # RGB Red
    [l2, l2, l1],  # RGB Yellow
    [l1, l1, l2],  # RGB Blue
    [l1, l2, l1],  # RGB Green
    [l2, l1, l1],  # RGB Red
    [l2, l2, l1],  # RGB Yellow
    [l1, l1, l2],  # RGB Blue
    [l1, l2, l1],  # RGB Green
]


# Functions


# Simply move into the room and position to aim at a marker
def move_into_room():
    if point_c_passed == True and point_e_passed == False and point_g_passed == False:  # if all conditions are true; if only point c has been passed
        print("moving into room 1")
        chassis_ctrl.move_with_distance(0, 2.33)  # Moves into room
        chassis_ctrl.move_with_distance(90,
                                        2.33)  # Moves right (horizontally) towards marker - BUT, GIMBAL WILL NOT BE AIMING MARKER. WE WILL FIX ELSEWHERE
        # Find the marker, and shoot once.
        scan_for_marker()
        time.sleep(5)



    elif point_e_passed == True and point_g_passed == False:  # If point e is passed but not point g
        print("moving into room 2")
        chassis_ctrl.move_with_distance(0, 2.33)  # Moves into room
        chassis_ctrl.move_with_distance(90,
                                        1.94)  # Moves right (horizontally) towards marker - BUT, GIMBAL WILL NOT BE AIMING MARKER. WE WILL FIX ELSEWHERE
        chassis_ctrl.move_with_distance(0, 4.584)  # Moves forward to person scan position
        time.sleep(5)


    elif point_g_passed == True:  # If point g is passed (we know all prev points have been passed, negate conditions for simplicity)
        print("passing room 3")
        pass  # Room 224 will always be poison room - If changes can re-implement Room 224 move logic here


# Move out of the room and reposition at last entry point
def move_out_of_room():
    if point_c_passed and not point_e_passed and not point_g_passed:  # if all conditions are true; if only point c has been passed
        print("moved out of room 1")
        chassis_ctrl.move_with_distance(-90, 2.33)  # Moves left (horizontally) towards room exit
        chassis_ctrl.move_with_distance(180, 2.33)  # Moves backwards out of room back to room entry point

    elif point_e_passed and not point_g_passed:  # If point e is passed but not point g
        chassis_ctrl.move_with_distance(180, 4.584)  # Moves backwards to person scan position
        chassis_ctrl.move_with_distance(-90, 2.33)  # Moves left (horizontally) towards room exit
        chassis_ctrl.move_with_distance(180, 1.94)


    elif point_g_passed:  # If point g is passed (we know all prev points have been passed, negate conditions for simplicity)
        pass  # Room 224 will always be poison room - If changes can re-implement Room 224 move logic here


# Scan for marker method
def scan_for_marker():
    print("Scan for marker fucntion called")
    # Turn on detection and scan left and right until you hit a marker.
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)
    gimbal_ctrl.yaw_ctrl(-100)  # Move gimbal left to try to find on left side
    gimbal_ctrl.yaw_ctrl(90)  # Move gimbal right to try and find on right side


def vision_recognized_marker_letter_F(msg):
    print("Marker F called")
    # Since you found the marker, turn detection off.
    vision_ctrl.disable_detection(rm_define.vision_detection_marker)
    vision_ctrl.detect_marker_and_aim(rm_define.marker_letter_F)
    gun_ctrl.fire_once()
    print("Marker F called")


def vision_recognized_marker_number_one(msg):
    print("Marker one called")
    # Since you found the marker, turn detection off.
    vision_ctrl.disable_detection(rm_define.vision_detection_marker)
    vision_ctrl.detect_marker_and_aim(rm_define.marker_number_one)  # Aims in attempt to find marker F

    # set up code to do something with the chassis and the gimbal
    chassis_ctrl.rotate_with_degree(rm_define.clockwise, 180)
    gimbal_ctrl.pitch_ctrl(20)
    chassis_ctrl.rotate_with_degree(rm_define.clockwise, 180)
    print("Marker one finished")


def vision_recognized_marker_number_two(msg):
    print("Marker 2 Called")
    vision_ctrl.disable_detection(rm_define.vision_detection_marker)
    # Change LED colors
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 224, 0, 255, rm_define.effect_always_on)
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 69, 215, 255, rm_define.effect_always_on)
    led_ctrl.turn_off(rm_define.armor_all)
    print("Marker 2 Finished")


def vision_recognized_marker_number_three(msg):
    # set up code to do something with both the chassis and the gimbal and the LED lights
    print("Marker 3 Called")
    vision_ctrl.disable_detection(rm_define.vision_detection_marker)
    chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90)
    gimbal_ctrl.pitch_ctrl(10)
    chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)

    # Change LED colors
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 224, 0, 255, rm_define.effect_always_on)
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all, 69, 215, 255, rm_define.effect_always_on)
    led_ctrl.turn_off(rm_define.armor_all)
    print("Marker 3 Finished")


# Fucntion to scan for people - TEST ON ITS OWN
def scan_for_person():
    # Enable person detection.
    vision_ctrl.enable_detection(rm_define.vision_detection_people)
    # Move the gimbal to scan for the person.
    gimbal_ctrl.yaw_ctrl(-90)
    gimbal_ctrl.yaw_ctrl(+180)


# Function to do something when a person is recognized
def vision_recognized_people(msg):
    # Again, since you found a person, turn off the detection.
    vision_ctrl.disable_detection(rm_define.vision_detection_people)
    # Make a sound.  Once complete it will return back to the main
    # program where it was called.
    media_ctrl.play_sound(rm_define.media_sound_solmization_1C)


# Decides what action to perform based on room type, then performs action (function name somewhat confusing)
def decide_room_action(room_type):
    if room_type == 1:  # If room is a fire room
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90)  # Rotate chassis so the FRONT is facing the door
        time.sleep(0.5)
        # Enter the room
        move_into_room()
        gimbal_ctrl.yaw_ctrl(180)  # Move gimbal left to try to find on left side
        time.sleep(1)

        # Move out of room and reposition
        move_out_of_room()
        time.sleep(1)
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)  # turn chassis -90 degrees to left to recenter
        gimbal_ctrl.yaw_ctrl(90)  # Move gimbal 90 degrees


    elif room_type == 2:  # If room is a poison room
        # Skip the room. Continue Course
        pass


    elif room_type == 3:  # If room is a person room
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90)  # Rotate chassis so the FRONT is facing the door
        time.sleep(1)
        # Enter the room
        move_into_room()
        time.sleep(1)
        gimbal_ctrl.yaw_ctrl(180)  # Move gimbal left to try to find on left side

        time.sleep(0.5)
        # Find the person
        scan_for_person()
        time.sleep(0.5)

        # Wait so the person is ready
        time.sleep(1)

        # Move out of room and reposition to move to start position
        move_out_of_room()
        time.sleep(0.5)
        chassis_ctrl.rotate_with_degree(rm_define.clockwise,
                                        90)  # turn chassis 90 degrees to right to recenter front facing the start
        gimbal_ctrl.yaw_ctrl(90)  # Move gimbal left to try to find on left side

        if point_c_passed and not point_e_passed and not point_g_passed:  # if all conditions are true; if only point c has been passed
            # Move home from C entry point = (5.47 + 2.29 + 6.56 = 14.32)
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 5)
            time.sleep(5)
            chassis_ctrl.move_with_distance(0, 4.32)

            chassis_ctrl.rotate_with_degree(rm_define.clockwise,
                                            180)  # turn chassis 180 degrees to recenter front facing point c
            gimbal_ctrl.yaw_ctrl(180)  # Move gimbal left to try to find on left side

            # Move back to C entry point
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 4.32)

        elif point_e_passed and not point_g_passed:  # If point e is passed but not point g
            # Move home from E distance = (14.32 + 5.78 + 5.17 = 25.27)
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 0.1)  # moves to d reset point
            time.sleep(5)
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 0.17)  # moves to e room entry

            chassis_ctrl.rotate_with_degree(rm_define.clockwise,
                                            180)  # turn chassis 180 degrees to recenter front facing point c
            gimbal_ctrl.yaw_ctrl(180)  # Move gimbal left to try to find on left side

            # Move back to E entry point
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 0.27)

        elif point_g_passed:  # If point g is passed (we know all prev points have been passed, negate conditions for simplicity)
            # Move home from C distance = (25.27 + 3.95 + 4.66 = 33.88)
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 5)  # gets back near to point d
            time.sleep(5)
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 5)  # gets back near to point f
            chassis_ctrl.move_with_distance(0, 3.88)

            chassis_ctrl.rotate_with_degree(rm_define.clockwise,
                                            180)  # turn chassis 180 degrees to recenter front facing point c
            gimbal_ctrl.yaw_ctrl(180)  # Move gimbal left to try to find on left side

            # Move back to E entry point
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 5)
            chassis_ctrl.move_with_distance(0, 3.88)



    else:
        # Other conditions not accounted for, simply pass
        pass


# Step 14 (Function which is called on step 14) (Donovan): Research something you can do with the robot and implement it here
def rgb_flash_colour_changers():
    media.enable_sound_recognition(rm_define.sound_detection_applause)
    while True:
        led_ctrl.gun_led_on()
        for i in range(1, 5):
            led.set_top_led(define.armor_top_all,
                            RGB[i][0], RGB[i][1], RGB[i][2], define.effect_always_on)
            led.set_bottom_led(define.armor_bottom_all,
                               RGB[i][0], RGB[i][1], RGB[i][2], define.effect_always_on)
            time.sleep(delay)
        if media.check_condition(define.cond_sound_recognized_applause_thrice):
            break
        break


def sound_recognized_applause_thrice(msg):
    led.turn_off(define.armor_all)
    led_ctrl.gun_led_off()
    media.cond_wait(define.cond_sound_recognized_applause_thrice)
    media.disable_sound_recognition(rm_define.sound_detection_applause)


def start():
    # Define room types before running program on course
    Room1Type = 1  # Fire
    Room2Type = 3  # Skip
    Room3Type = 2  # Person

    # Set the point variables as global variables so they are updated globally
    global point_c_passed
    global point_e_passed
    global point_g_passed

    # Allow the chassis and gimbal to move independently - ONLY NEED TO SET ONCE, UNLESS NEED TO CHANGE AND MOVE DEPENDANTLY
    robot_ctrl.set_mode(rm_define.robot_mode_free)

    # set chassis movement and rotation speed, and gimbal rotation speed
    chassis_ctrl.set_trans_speed(1)
    chassis_ctrl.set_rotate_speed(40)
    gimbal_ctrl.set_rotate_speed(60)

    # Step 1: Start: Move the robot ahead 5.47 meters to B
    chassis_ctrl.move_with_distance(0, 5)
    chassis_ctrl.move_with_distance(0, 0.7)

    # Step 2 (Sara): ZigZag

    # move ahead 8 inches
    chassis_ctrl.move_with_distance(0, 0.203)

    # rotate 90 degrees counterclockwise and move forward 32 inches
    chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)
    chassis_ctrl.move_with_distance(0, 0.813)

    # rotate 90 degrees clockwise to face forward and move forward 14 inches
    chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90)
    chassis_ctrl.move_with_distance(0, 0.356)

    # rotate 90 degrees clockwise and move forward 65 inches
    chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90)
    chassis_ctrl.move_with_distance(0, 1.651)

    # rotate 90 degrees counter clockwise and move forward 17.5 inches
    chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)
    chassis_ctrl.move_with_distance(0, 0.444)

    # rotate 90 degrees counter clockwise and move ahead 21 inches
    chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)
    chassis_ctrl.move_with_distance(0, 0.533)

    # rotate 45 degrees counterclockwise and move forward 59 inches
    chassis_ctrl.rotate_with_degree(rm_define.clockwise, 45)
    chassis_ctrl.move_with_distance(0, 1.499)

    # rotate 45 degrees clockwise and move forward 21 inches
    chassis_ctrl.rotate_with_degree(rm_define.clockwise, 45)
    chassis_ctrl.move_with_distance(0, 0.53)

    # rotate 90 degrees clockwise and move forward 34 inches
    chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90)
    chassis_ctrl.move_with_distance(0, 0.864)

    # rotate 90 degrees counterclockwise and move forward 16 inches
    chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)
    chassis_ctrl.move_with_distance(0, 0.406)

    # recenter gimbal
    gimbal_ctrl.recenter()

    # rest point
    time.sleep(5)

    # Step 3: Move to C (Room1) entry position
    chassis_ctrl.move_with_distance(0, 5)
    chassis_ctrl.move_with_distance(0, 1.56)

    # Set point c passed flag to true
    point_c_passed = True

    # Step 4: Move robot into C (Room1) If needed
    decide_room_action(Room1Type)
    time.sleep(5)

    # Step 5: Move robot to D (reset point 1)
    chassis_ctrl.move_with_distance(0, 5)
    # chassis_ctrl.move_with_distance(0,0.78)
    time.sleep(5)

    # Step 6: Move to door E (Room2) entry position
    chassis_ctrl.move_with_distance(0, 5)
    chassis_ctrl.move_with_distance(0, 0.17)
    time.sleep(3)

    # Set point E passed flag to true
    point_e_passed = True

    # Step 7: Move robot into E (Room2), If needed
    decide_room_action(Room2Type)
    time.sleep(0.5)

    # Step 8: move the robot to F (reset point 2)
    chassis_ctrl.move_with_distance(0, 3.7)  # 3.95
    time.sleep(5)

    # Step 9 (Michelle): Perform 3 tasks with robot at reset point F
    scan_for_marker()

    # Step 10: move the robot G (Room3) entry point
    print("done Michelle step (F) resuming movement")
    chassis_ctrl.move_with_distance(0, 4.66)
    time.sleep(5)

    # Set point G passed flag to true
    point_g_passed = True

    # Step 11: Move robot into G (Room3) If needed
    decide_room_action(Room3Type)
    time.sleep(0.5)

    # Step 12: Move the robot H (end point)
    chassis_ctrl.move_with_distance(0, 5)
    chassis_ctrl.move_with_distance(0, 0.35)
    time.sleep(5)

    # Step 13: Move in reverse back to position D
    chassis_ctrl.move_with_distance(180, 5)
    chassis_ctrl.move_with_distance(180, 5)
    chassis_ctrl.move_with_distance(180, 5)
    chassis_ctrl.move_with_distance(180, 4.25)
    time.sleep(7)

    # Step 14 (Donovan): Research something you can do with the robot and implement it here
    rgb_flash_colour_changers()
    time.sleep(5)

    # Step 15: Move in reverse from position D to starting position A
    chassis_ctrl.move_with_distance(180, 5)
    chassis_ctrl.move_with_distance(180, 5)
    chassis_ctrl.move_with_distance(180, 5)
    chassis_ctrl.move_with_distance(180, 4.13)
    time.sleep(5)

    # Course Completed!
