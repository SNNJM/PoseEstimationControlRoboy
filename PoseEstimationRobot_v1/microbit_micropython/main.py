from microbit import *
from rekabit import *
import utime

# Initialize UART communication
uart.init(baudrate=115200)

# PID constants
Kp = 0.5  # Proportional constant
Ki = 0.1  # Integral constant
Kd = 0.05 # Derivative constant

# PID control variables
prev_error = 0
integral = 0

# Function to apply PID control to motor speed
def pid_control(target_speed, current_speed):
    global prev_error, integral

    # Calculate error
    error = target_speed - current_speed

    # Proportional term
    P = Kp * error

    # Integral term
    integral += error
    I = Ki * integral

    # Derivative term
    D = Kd * (error - prev_error)

    # Compute PID output (motor speed adjustment)
    output = P + I + D

    # Update previous error for next iteration
    prev_error = error

    # Return the motor speed as an integer (between 0 and 255)
    return min(max(int(output), 0), 255)

# Function to control motor with smooth PID control
def move_motor(direction):
    # Current speed (you can adjust this depending on actual motor speed feedback)
    current_speed = 0
    
    # Define target speeds for each direction
    target_speeds = {
        "FORWARD": 255,
        "REVERSE": -255,
        "LEFT": 255,
        "RIGHT": 255,
        "STOP": 0
    }
    
    target_speed = target_speeds.get(direction, 0)

    # Apply PID control to calculate motor speed
    motor_speed = pid_control(target_speed, current_speed)

    if direction == "FORWARD":
        run_motor(Motor_All, Direction_Forward, motor_speed)
    elif direction == "REVERSE":
        run_motor(Motor_All, Direction_Backward, motor_speed)
    elif direction == "LEFT":
        run_motor(Motor_M1, Direction_Forward, 0)  # Rotate left by controlling one motor
        run_motor(Motor_M2, Direction_Forward, motor_speed)
    elif direction == "RIGHT":
        run_motor(Motor_M1, Direction_Forward, motor_speed)  # Rotate right
        run_motor(Motor_M2, Direction_Forward, 0)
    else:  # STOP
        brake_motor(Motor_M1)
        brake_motor(Motor_M2)

while True:
    if uart.any():
        data = uart.readline().strip()
        command = data.decode('utf-8') if data else ""

        print("Received:", command)  # Debugging

        move_motor(command)  # Control motor based on received command

        if command in ["FORWARD", "REVERSE", "LEFT", "RIGHT"]:
            display.show("1")  # Show "1" when receiving data
        else:
            display.show("0")  # Show "0" when stopped

    utime.sleep(0.1)
