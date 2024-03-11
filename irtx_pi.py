import RPi.GPIO as GPIO
import pigpio
import time
from enum import Enum

# Enum class for commands
class TVCommand(Enum):
    TURN_ON_OFF = (0x04, 0x08, "TURN_ON_OFF", 1)  # Address, Command, TV Command, Delay
    MUTE_UNMUTE = (0x04, 0x09, "MUTE_UNMUTE", 1)
    VOLUME_UP = (0x04, 0x02, "VOLUME_UP", 1)
    VOLUME_DOWN = (0x04, 0x03, "VOLUME_DOWN", 1)
    CHANNEL_UP = (0x04, 0x00, "CHANNEL_UP", 1)
    CHANNEL_DOWN = (0x04, 0x01, "CHANNEL_DOWN", 1)

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Disable GPIO warnings

# Define the GPIO pin for IR transmitter
IR_TRANSMITTER_PIN = 23

# Initialize the GPIO pin for IR transmitter
GPIO.setup(IR_TRANSMITTER_PIN, GPIO.OUT)

# Set up the pigpio instance
pi = pigpio.pi()

# Define the TinyIRReceiver protocol parameters
TINYIR_FREQ = 38000      # TinyIRReceiver frequency in Hz
TINYIR_HEADER_MARK = 9000  # Header mark in microseconds
TINYIR_HEADER_SPACE = 4500  # Header space in microseconds
TINYIR_BIT_MARK = 560    # Bit mark in microseconds
TINYIR_ONE_SPACE = 1690  # One bit space in microseconds
TINYIR_ZERO_SPACE = 560  # Zero bit space in microseconds

# Function to send a command via IR transmitter with a specified delay
def send_command_with_delay(command):
    """
    Send an IR command with the specified address, command, and delay.

    Args:
        command (tuple): The command tuple (address, command, TV command, delay_seconds).

    Returns:
        None
    """
    address, command_code, tv_command, delay_seconds = command

    # Construct waveform for the command
    wf = [
        pigpio.pulse(1 << IR_TRANSMITTER_PIN, 0, TINYIR_HEADER_MARK),  # Header mark
        pigpio.pulse(0, 1 << IR_TRANSMITTER_PIN, TINYIR_HEADER_SPACE)   # Header space
    ]

    # Add pulses for the address
    for bit in '{:08b}'.format(address)[::-1]:
        wf.append(pigpio.pulse(1 << IR_TRANSMITTER_PIN, 0, TINYIR_BIT_MARK))  # Bit mark
        if bit == '1':
            wf.append(pigpio.pulse(0, 1 << IR_TRANSMITTER_PIN, TINYIR_ONE_SPACE))  # One bit space
        else:
            wf.append(pigpio.pulse(0, 1 << IR_TRANSMITTER_PIN, TINYIR_ZERO_SPACE))  # Zero bit space

    # Add pulses for the command
    for bit in '{:08b}'.format(command_code)[::-1]:
        wf.append(pigpio.pulse(1 << IR_TRANSMITTER_PIN, 0, TINYIR_BIT_MARK))  # Bit mark
        if bit == '1':
            wf.append(pigpio.pulse(0, 1 << IR_TRANSMITTER_PIN, TINYIR_ONE_SPACE))  # One bit space
        else:
            wf.append(pigpio.pulse(0, 1 << IR_TRANSMITTER_PIN, TINYIR_ZERO_SPACE))  # Zero bit space

    # Transmit the waveform
    pi.wave_add_generic(wf)
    wid = pi.wave_create()
    pi.wave_send_once(wid)

    print(f"Sent command: Address={address:02X}, Command={command_code:02X}, TV Command={tv_command}")
    time.sleep(delay_seconds)

# Function to send a command
def send_commands(command_name):
    """
    Send the specified IR command.

    Args:
        command_name (str): The name of the command to send (e.g., 'TURN_ON_OFF', 'VOLUME_UP').

    Returns:
        None
    """
    command = TVCommand[command_name].value
    send_command_with_delay(command)

# If this script is run directly
if __name__ == "__main__":
    try:
        # Send all commands one by one
        for command in TVCommand:
            send_commands(command.name)
            time.sleep(2)  # Add a delay between commands for better reception

    finally:
        # Clean up GPIO pins and pigpio instance
        GPIO.cleanup()
        pi.stop()
