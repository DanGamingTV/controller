from ev3dev2.sound import Sound

sound = Sound()
tts_enabled = True
scriptname = "/tts/ev3.py"

def debug_log(message):
    # Debugging
    global debug
    if (debug):
        print(message)

def mute_tts():
    global tts_enabled
    tts_enabled = False
    debug_log("TTS Muted")

def unmute_tts():
    global tts_enabled
    tts_enabled = True
    debug_log("TTS Unmuted")

def say(message):
    global scriptname
    global tts_enabled
    message = message.lower()
    message = message.replace("pls", "please")
    message = message.replace("lol", "laughing out loud")
    message = message.replace(":)", "smiley")
    message = message.replace("(:", "smiley")
    message = message.replace(":D", "smiley")
    message = message.replace("d:", "smiley")
    message = message.replace("hell", "heck")
    # Feel free to add your own filtering / formattig here.
    if (tts_enabled):
        tts_speak(message)
    debug_log("ran tts() from {}".format(scriptname))

def tts_speak(message):
    global tts_enabled
    global scriptname
    debug_log("tts_enabled = {}".format(tts_enabled))
    debug_log("ran tts_speak() from {}".format(scriptname))
    sound.speak(message)
