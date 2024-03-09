import eel
import serial_com
#import rfcontroller # This import should be commented out when testing on a PC
import json
import pyautogui
import threading
#import ir_transmitter_code  # Import the Python file containing the adapted Arduino code
from gtts import gTTS
import os
from serial_com import send_command, TVCommand  # Import the send_command function and TVCommand enum from serial_com.py

# Expose functions for controlling the TV
@eel.expose 
def powerOnOff():
    serial_com.send_command_with_delay(0x4, 0x8)

@eel.expose 
def muteUnmute():
    serial_com.send_command_with_delay(0x4, 0x9)

@eel.expose 
def volumeUp():
    serial_com.send_command_with_delay(0x4, 0x2)

@eel.expose 
def volumeDown():
    serial_com.send_command_with_delay(0x4, 0x3)

@eel.expose 
def channelUp():
    serial_com.send_command_with_delay(0x4, 0x0)

@eel.expose 
def channelDown():
    serial_com.send_command_with_delay(0x4, 0x1)


#controller = rfcontroller.RFController() # Comment this out when developing on desktop
screenWidth, screenHeight = pyautogui.size()
pyautogui.FAILSAFE = False


@eel.expose
def togglePlug(command):
    print(command) # For testing on a PC, this line should be uncommented, and the following line should be commented out
    #controller.sendcode(command) # This line should be commented out when testing on PC, the library is not available on PC

# Below, some lines are commented out because to autostart on the pi we had to include full file paths. When working on the
# software from a PC, uncomment the shortened paths and comment out the absolute paths that include the /home/pi/...
@eel.expose
def storeConfig(setting, value):
    config = {}
    with open('config.json', 'r') as openfile:
    #with open('/home/pi/ALS-Assistive-Tech/config.json', 'r') as openfile:
        config  = json.load(openfile)
    with open('config.json', 'w') as writefile:
    #with open('/home/pi/ALS-Assistive-Techp/config.json', 'w') as writefile:
        config[setting] = value
        json.dump(config, writefile)

@eel.expose
def loadConfig():
    with open('config.json', 'r') as openfile:
    #with open('/home/pi/ALS-Assistive-Tech/config.json', 'r') as openfile:
        config = json.load(openfile)
        eel.loadConfig(config)

@eel.expose
def resetMouse():
    pyautogui.moveTo(0, screenHeight)

@eel.expose
def speak_from_text(text):
    speak_text(text)  # The function defined above


# At the end of your main script or when the Eel server shuts down
def cleanup():
    serial_com.ser.close()
    print("Serial port closed")

# Start the eel web server
if __name__ == "__main__":
    try:
        eel.init('web', allowed_extensions=[".js",".html"])
        resetMouse()
        eel.start('C:/TV_Remote_Testing_Today/ALS-Assistive-Tech-TV-Remote/web/index.html', port=8001, cmdline_args=['--start-fullscreen'])
    finally:
        cleanup()

# Call send_commands() after server starts
serial_com.send_commands()


# At the end of your main script or when the Eel server shuts down
def cleanup():
    serial_com.ser.close()
    print("Serial port closed")

def speak_text(text):
    # Create a tts object
    tts = gTTS(text=text, lang='en', slow=False)
    
    # Save the audio file
    tts.save("output.mp3")
    
    # Play the audio file
    os.system("mpg123 output.mp3")  # use 'mpg123 output.mp3' or a suitable alternative.

# Example usage:
speak_text("Hello world, this is a test of Google Text to Speech")
    
