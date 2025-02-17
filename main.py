import os
import eel
import irtx_pi  # Import the irtx_pi module
# import rfcontroller # This import should be commented out when testing on a PC
import json
import pyautogui
import threading
# import pyttsx3
from gtts import gTTS

# Function to send power on/off command
@eel.expose
def powerOnOff():
    irtx_pi.send_commands('TURN_ON_OFF')

# Function to send mute/unmute command
@eel.expose
def muteUnmute():
    irtx_pi.send_commands('MUTE_UNMUTE')

# Function to send volume up command
@eel.expose
def volumeUp():
    irtx_pi.send_commands('VOLUME_UP')

# Function to send volume down command
@eel.expose
def volumeDown():
    irtx_pi.send_commands('VOLUME_DOWN')

# Function to send channel up command
@eel.expose
def channelUp():
    irtx_pi.send_commands('CHANNEL_UP')

# Function to send channel down command
@eel.expose
def channelDown():
    irtx_pi.send_commands('CHANNEL_DOWN')

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


# Start the eel web server      
if __name__ == "__main__":
    # eel.init('web', allowed_extensions=[".js",".html"])
    eel.init('/home/pi/ALS-Assistive-Tech/web', allowed_extensions=[".js",".html"])
    resetMouse()
    eel.start('index.html', cmdline_args=['--start-fullscreen'])


def speak_text(text):
    # Create a tts object
    tts = gTTS(text=text, lang='en', slow=False)
    
    # Save the audio file
    tts.save("output.mp3")
    
    # Play the audio file
    # os.system("mpg123 output.mp3")  # use 'mpg123 output.mp3' or a suitable alternative.

# Example usage:
speak_text("Hello world, this is a test of Google Text to Speech")
