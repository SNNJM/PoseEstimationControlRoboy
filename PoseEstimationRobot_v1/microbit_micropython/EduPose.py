from microbit import *
import edubit

while True:
    data = uart.read()  # Read data from Python script
    if data:
        command = data.decode().strip()
        if command == "UP":
            edubit.set_motor(100)  # Move motor forward
        elif command == "DOWN":
            edubit.set_motor(-100)  # Move motor backward
        else:
            edubit.set_motor(0)  # Stop motor
