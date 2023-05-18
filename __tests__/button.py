import RPi.GPIO as GPIO

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin number
button_pin = 21

# Set up the GPIO pin as an input with a pull-up resistor
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define a function to handle button presses
def handle_button_press():
    print("Button pressed!")
    # Do something based on the button press

while True:
    # Your existing code in the while loop

    # Check the button state
    if GPIO.input(button_pin) == GPIO.LOW:
        handle_button_press()

# Clean up GPIO on program exit
GPIO.cleanup()
