from configure import auth_key
from datetime import datetime
from distutils.command.upload import upload
from pytube import YouTube
from urllib.parse import urlencode
from zipfile import ZipFile
from random import random
from PIL import Image

import asyncio
import base64
import json
import os
import pyaudio
import requests
import sys
import time
import websockets
import streamlit as st
import pandas as pd
import numpy as np

# API key
api_key = st.secrets['api_key']
# Print title
st.title("Speakr")
# Format bar
bar = st.progress(0)

# Global variables
# ***
global orig1, delta1
orig1 = 0
delta1 = 0

# Print the image of the logo
st.markdown("<p style='text-align:center;''><img src='https://media.discordapp.net/attachments/936829125891596388/937203364201132082/output-onlinepngtools.png?width=749&height=587' class='center' width='270rem' height='200rem'></p>", unsafe_allow_html=True)

# Button update function
def buttonUpdate(newData):
    global orig1, delta1
    delta1 = newData - orig1 
    orig1 = newData
    
    #Metrics
    #***
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.metric(label="Um's", value=orig1, delta=delta1)
    with col2:
        st.metric(label="Uh's", value="90", delta="0")
    with col3:
        st.metric(label="Hmm's", value="127", delta="-12")
    with col4:
        st.metric(label="Mhm's", value="69", delta="50")
    with col5:
        st.metric(label="Like's", value="20", delta="-31")

    #Chart
    #***
    df = pd.DataFrame(np.random.rand(30, 5),columns=('col %d' % i for i in range(5)))
    st.bar_chart(df)

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
                        st.sidebar.markdown(json.loads(result_str)['text'])
                        # Print out the text to the streamlit app
                        #st.markdown(json.loads(result_str)['text'])
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

#Empty container
st.empty()
st.write("????")

data_button = st.button('Show me my data!')
file_upload_button = st.button('Upload a file')

if(int(datetime.utcnow().timestamp()) % 2 == 1):
    test_val = True
else:
    test_val = False

st.error("Humanity Lived")

if file_upload_button:
    uploaded_file = st.file_uploader('Choose File')
    #if uploaded_file is not None:
#        buttonUpdate(420)

if data_button:
    with st.spinner('processing data...'):
        bar1 = st.progress(20)
        time.sleep(1)
        bar1.progress(40)
        time.sleep(1)
        bar1.progress(60)
        time.sleep(1)
        bar1.progress(80)
        time.sleep(1)
        bar1.progress(100)
        time.sleep(1)
    st.success('Done!')
    st.info("INFORMATION")
    #st.balloons()
    buttonUpdate(420)