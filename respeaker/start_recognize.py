'''
Bing Speech To Text (STT) with Voice Activity Detect (VAD)

Requirements:
+ pyaudio - `pip install pyaudio`
+ py-webrtcvad - `pip install webrtcvad`

'''

from bing_voice import *
from apiai import *
from mqtt import *
from spi import SPI

import webrtcvad
import collections
import sys
import signal
import pyaudio

# get a key from https://www.microsoft.com/cognitive-services/en-us/speech-api
BING_KEY = '338a43b317ff4518b2416b37c19e31fc'
APIAI_TOKEN = '549f1420d83945c89a193dc0619e2248'
HA_MQTT_TOPIC = 'respeaker/ha/cmd'
TRIGGER_WORD = 'home'

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_DURATION_MS = 30  # supports 10, 20 and 30 (ms)
PADDING_DURATION_MS = 1000
CHUNK_SIZE = int(RATE * CHUNK_DURATION_MS / 1000)
CHUNK_BYTES = CHUNK_SIZE * 2
NUM_PADDING_CHUNKS = int(PADDING_DURATION_MS / CHUNK_DURATION_MS)
NUM_WINDOW_CHUNKS = int(240 / CHUNK_DURATION_MS)

vad = webrtcvad.Vad(2)
bing = BingVoice(BING_KEY)
apiai = Apiai(APIAI_TOKEN)
mqtt = Mqtt()
spi = SPI()

pa = pyaudio.PyAudio()
stream = pa.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, start=False, frames_per_buffer=CHUNK_SIZE)
got_a_sentence = False
leave = False
got_trigger = False;

def handle_int(sig, chunk):
    global leave, got_a_sentence
    
    leave = True
    got_a_sentence = True
    
signal.signal(signal.SIGINT, handle_int)

while not leave:
    ring_buffer = collections.deque(maxlen=NUM_PADDING_CHUNKS)
    triggered = False
    voiced_frames = []
    ring_buffer_flags = [0] * NUM_WINDOW_CHUNKS
    ring_buffer_index = 0
    buffer_in = ''
    
    print("* recording")
    stream.start_stream()
    while not got_a_sentence and not leave:
        chunk = stream.read(CHUNK_SIZE)
        active = vad.is_speech(chunk, RATE)
        sys.stdout.write('1' if active else '0')
        ring_buffer_flags[ring_buffer_index] = 1 if active else 0
        ring_buffer_index += 1
        ring_buffer_index %= NUM_WINDOW_CHUNKS
        if not triggered:
            ring_buffer.append(chunk)
            num_voiced = sum(ring_buffer_flags)
            if num_voiced > 0.5 * NUM_WINDOW_CHUNKS:
                sys.stdout.write('+')
                triggered = True
                voiced_frames.extend(ring_buffer)
                ring_buffer.clear()
        else:
            voiced_frames.append(chunk)
            ring_buffer.append(chunk)
            num_unvoiced = NUM_WINDOW_CHUNKS - sum(ring_buffer_flags)
            if num_unvoiced > 0.9 * NUM_WINDOW_CHUNKS:
                sys.stdout.write('-')
                triggered = False
                got_a_sentence = True

        sys.stdout.flush()

    sys.stdout.write('\n')
    data = b''.join(voiced_frames)
    
    stream.stop_stream()
    print("* done recording")

    # recognize speech using Microsoft Bing Voice Recognition
    try:
        text = bing.recognize(data, language='en-US')
		
        print(text)
		
        if "header" in text and "lexical" in text["header"]:
			recognizedText = text["header"]["lexical"]
			print('Bing:' + recognizedText.encode('utf-8'))
			
			if(recognizedText == TRIGGER_WORD):
				print("Triggre word detected")
				got_trigger = True
				spi.write("on\n");
			elif got_trigger:
				result = apiai.recognize(recognizedText)
				print(result)
				print("")
				
				print(result["result"]["metadata"]["intentName"])
				print(result["result"]["parameters"]["room"])
				print(result["result"]["parameters"]["op"])
				
				jsonCmd = json.dumps({
					"cmd": result["result"]["parameters"]["op"],
					"room": result["result"]["parameters"]["room"]
				})
		
				mqtt.publishcmd(HA_MQTT_TOPIC, jsonCmd)
				
				got_trigger = False
				spi.write("off\n");
        else:
			print('Cannot recognize audio')
    except UnknownValueError:
        print("Microsoft Bing Voice Recognition could not understand audio")
    except RequestError as e:
        print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
        
    got_a_sentence = False
        
stream.close()