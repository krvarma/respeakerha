Home Automation using [ReSpeaker](https://www.kickstarter.com/projects/seeed/respeaker-an-open-modular-voice-interface-to-hack?token=fe8b1f79), [Arduino MKR1000](https://www.arduino.cc/en/Main/ArduinoMKR1000) and [MQTT](http://mqtt.org/)
==

Probably you all heard about [ReSpeaker](https://www.kickstarter.com/projects/seeed/respeaker-an-open-modular-voice-interface-to-hack?token=fe8b1f79), it is a hackable open hardware voice inteface. It is a development board based on Mediatek’s MT7688 WiFi module and runs on [OpenWrt](https://openwrt.org/). You an program it using Arduino, Python, Node.js, Lua and C/C++. ReSpeaker also supports various hardware add-ons like Groove Expansion, Microphone Array, etc... I am one of the early beta user of ReSpeaker. Here is a link to the Kickstarter Page. 

https://www.kickstarter.com/projects/seeed/respeaker-an-open-modular-voice-interface-to-hack?token=fe8b1f79

ReSpeaker supports speech recognition using Microsoft Cognitive Service, Amazon Alexa Voice Service, Google Speech API, Wit.ai, Houndify, etc... 

Here is a Home Automation project I worked using [ReSpeaker](https://www.kickstarter.com/projects/seeed/respeaker-an-open-modular-voice-interface-to-hack?token=fe8b1f79), [Microsoft Cognitive Service Speech API](https://www.microsoft.com/cognitive-services/en-us/speech-api), [Api.ai](https://api.ai/) and [MQTT](http://mqtt.org/), it controls the lights using voice interface. Basically what it does is, record audio using ReSpeaker, convert to text using Microsoft Cognitive Service Speech to Text, process and the text using Api.ai conversational voice interfaces platform, send MQTT messages to turn on/off different lights.

The project has two hardware components, ReSpeaker and Arduino MKR1000 to which two LEDs are connected (these LEDs represents different lights). 

ReSpeaker recognize the user voice input using Microsoft Cognitive Service Speech API. If a trigger word is detected (configurable), the application turns on the LEDs on the ReSpeaker and then listens for commands. The trigger word I use for this demo is "*jarvis*", but you can using any word you want. For no reason I am using this word. Here is and example of conversation:

1. *Jarvis, turn on turn bedroom light*
2. *Jarvis, turn off turn bedroom light*
3. *Jarvis, turn on turn kitchen light*
4. *Jarvis, turn off turn kitchen light*

Here is a pictorial representation of the application flow

![Pictorial Representation of ReSpeaker Home Automation](https://raw.githubusercontent.com/krvarma/respeakerha/master/images/flow.png)

Parts List
----------
1. [ReSpeaker](https://www.kickstarter.com/projects/seeed/respeaker-an-open-modular-voice-interface-to-hack?token=fe8b1f79)
2. [Arduino MKR1000](https://www.arduino.cc/en/Main/ArduinoMKR1000)
3. [Generic LEDs](http://www.mouser.com/leds-leaded/)
4. [Jumper Wires](http://www.mouser.com/Tools-Supplies/Prototyping-Products/Jumper-Wires/_/N-bkrh0)

Setting up ReSpeaker
--------------------
Follow [this document](https://github.com/respeaker/get_started_with_respeaker/wiki) to get started with ReSpeaker

Using the application
---------------------

1. Wire up the Arduino MKR1000 as per the schematics below
2. Open Arduino IDE and flash the `ha.ino` to MKR1000
3. Connect your ReSpeaker to the network
4. SSH to your ReSpeaker
5. Create a folder to clone the project files
6. Move to the folder and close the repo https://github.com/krvarma/respeakerha.git
7. Got to *respeaker* folder
8. Create an account or log on to Microsoft Cognitive Service Speech API](https://www.microsoft.com/cognitive-services/en-us/speech-api).
9. Get an API Key and replace the variable `BING_KEY` in the Python Script `creds.py`.
10. Create and account or log on to [Api.ai](https://api.ai/)
11. Get Access Token and replace the variable `APIAI_TOKEN` in the Python Script `creds.py`
12. Open Arduino IDE and load respeaker_ha.ino`. Flash this application to your ReSpeaker
13. Got to *respeakerha\respeaker* folder
14. Install required Python package `paho-mqtt` using `pip install paho-mqtt`
15. Install required Python package `monotonic` using `pip install monotonic`
16. Run `start_recognize.py` using `python start_recognize.py`
17. Say *`jarvis`* and wait for the lights on your ReSpeaker to turn on
18. Say `turn on bedroom light/turn off bedroom light/turn on kitchen light/turn off kitchen light

If everything OK, you can turn on/off the lights using voice input.

Schematics
----------

![Schematics](https://raw.githubusercontent.com/krvarma/respeakerha/master/images/schematics.png)

Demo Video
----------

https://www.youtube.com/watch?v=_gFTX7dubsY