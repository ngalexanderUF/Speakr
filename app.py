from configure import auth_key
from datetime import datetime
from distutils.command.upload import upload
from pytube import YouTube
from urllib.parse import urlencode
from zipfile import ZipFile

import asyncio
import base64
import json
import numpy as np
import os
import pandas as pd
import pyaudio
import requests
import streamlit as st
import sys
import time
import websockets

api_key = st.secrets['api_key']

#Formatting
st.markdown("<h1 style='text-align: center; color: white;'>Speakr</h1>", unsafe_allow_html=True)


bar = st.progress(0)
st.image("output-onlinepngtools.png", width = 350)


#***
global orig1, delta1
orig1 = 0
delta1 = 0

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
    
    #***
def live_audio():
    FRAMES_PER_BUFFER = 3200
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    p = pyaudio.PyAudio()

    # starts recording
    stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
    )

    sample_rate = 16000
    word_boost = ["arm", "uhh"]
    params = {"sample_rate": 16000, "word_boost": json.dumps(word_boost)}

    url = f"wss://api.assemblyai.com/v2/realtime/ws?{urlencode(params)}"

    # the AssemblyAI endpoint we're going to hit
    # url = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"


    async def send_receive():
        print(f'Connecting websocket to url ${url}')
        async with websockets.connect(
            url,
            extra_headers=(("Authorization", auth_key),),
            ping_interval=5,
            ping_timeout=20
        ) as _ws:
            await asyncio.sleep(0.1)
            print("Receiving SessionBegins ...")
            session_begins = await _ws.recv()
            print(session_begins)
            print("Sending messages ...")
            async def send():
                while True:
                    try:
                        data = stream.read(FRAMES_PER_BUFFER)
                        data = base64.b64encode(data).decode("utf-8")
                        json_data = json.dumps({"audio_data":str(data)})
                        await _ws.send(json_data)
                    except websockets.exceptions.ConnectionClosedError as e:
                        print(e)
                        assert e.code == 4008
                        break
                    except Exception as e:
                        assert False, "Not a websocket 4008 error"
                    await asyncio.sleep(0.01)
                
                return True
            
            async def receive():
                while True:
                    try:
                        result_str = await _ws.recv()
                        #if json.loads(result_str)['message_type'] == 'FinalTranscript':
                        print(json.loads(result_str)['text'])
                        # st.markdown(json.loads(result_str)['text'])
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

live_button = st.button("Start recording live audio")
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

if live_button:
    live_audio()

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