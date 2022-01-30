import pyaudio
import streamlit as st
import websockets
import asyncio
import base64
import json
from urllib.parse import urlencode
from configure import auth_key
from random import random

# Specify constants
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()

# Create stream
stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)

# Open file for writing the speech-to-text transcriptions
f = open("myfile.txt", "a")

# Initialize the session state
if 'run' not in st.session_state:
    st.session_state['run'] = False

# Define function for beginning the listening process
def start_listening():
    st.session_state['run'] = True

# Define function to stop listening
def stop_listening():
    st.session_state['run'] = False

# Create two columns for buttons, one for start and one for stop
start, stop = st.columns(2)

# Create the two buttons
start.button('Begin listening...', on_click = start_listening)
stop.button('Stop listening...', on_click = stop_listening)

# List of words to boost, plus the params necessary for the url query
word_boost = ["like", "umm", "um", "err", "er", "uhh", "uh", "hmm", "hm", "well", "okay", "totally", "literally"]
params = {"sample_rate": 16000, "word_boost": json.dumps(word_boost)}

# Specialized url 
url = f"wss://api.assemblyai.com/v2/realtime/ws?{urlencode(params)}"

# Define a title for the streamlit app
st.title("Here are our sexy words")

# Define functioning for sending a receiving from the AssemblyAI API
async def send_receive():
   print(f'Connecting websocket to url ${url}')
   # Connect
   async with websockets.connect(
       url,
       extra_headers=(("Authorization", auth_key),),
       ping_interval=5,
       ping_timeout=20
   ) as _ws:
       t = await asyncio.sleep(0.1)
       print("Receiving SessionBegins ...")
       session_begins = await _ws.recv()
       print(session_begins)
       print("Sending messages ...")
       # Sending data to the AssemblyAI API
       async def send():
           # While the program is still listening
           while st.session_state['run']:
               try:
                   # Send the data
                   data = stream.read(FRAMES_PER_BUFFER)
                   data = base64.b64encode(data).decode("utf-8")
                   json_data = json.dumps({"audio_data":str(data)})
                   t = await _ws.send(json_data)
               except websockets.exceptions.ConnectionClosedError as e:
                   print(e)
                   assert e.code == 4008
                   break
               except Exception as e:
                   assert False, "Not a websocket 4008 error"
               t = await asyncio.sleep(0.01)
          
           return True
      
       # Receiving data from the AssemblyAI API
       async def receive():
           # While the program is still listening
           while st.session_state['run']:
               try:
                   # Receive the data
                   result_str = await _ws.recv()
                   # If the message is a sentence or complete thought
                   if json.loads(result_str)['message_type'] == 'FinalTranscript':
                        # Open the text file to append to it
                        f = open("myfile.txt", "a")
                        # Write to the text file
                        f.write(json.loads(result_str)['text'])
                        # Print out the text to the command line
                        print(json.loads(result_str)['text'])
                        # Print out the text to the streamlit app
                        st.markdown(json.loads(result_str)['text'])
                        # Close the text file
                        f.close()
               except websockets.exceptions.ConnectionClosedError as e:
                   print(e)
                   assert e.code == 4008
                   break
               except Exception as e:
                   assert False, "Not a websocket 4008 error"
      
       send_result, receive_result = await asyncio.gather(send(), receive())

asyncio.run(send_receive())



