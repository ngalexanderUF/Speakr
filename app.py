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

st.progress(0)
#st.image("output-onlinepngtools.png", width = 350)
st.markdown("<p style='text-align:center;''><img src='https://media.discordapp.net/attachments/936829125891596388/937203364201132082/output-onlinepngtools.png?width=749&height=587' class='center' width='270rem' height='200rem'></p>", unsafe_allow_html=True)


#***
global orig1, delta1, orig2, delta2, orig3, delta3, orig4, delta4, orig5, delta5
orig1 = 0
delta1 = 0
orig2 = 0
delta2 = 0
orig3 = 0
delta3 = 0
orig4 = 0
delta4 = 0
orig5 = 0
delta5 = 0

def umCounter(transc):
    umCount = 1
    checkNext = False
    prevSpace = True

    for c in transc: 
        if (checkNext) and (prevSpace):
            if (c == "m") or (c == "M"):
                umCount += 1
                checkNext = False
            else:
                checkNext = False
        if (c == "u") or (c == "U"):
            checkNext = True
        elif (c == " "):
            prevSpace = True
            checkNext = False
        else:
            prevSpace = False
            checkNext = False

    return (umCount)

def uhCounter(transc):
    uhCount = 0
    checkNext = False
    prevSpace = True

    for c in transc: 
        if (checkNext) and (prevSpace):
            if (c == "h") or (c == "H"):
                uhCount += 1
                checkNext = False
            else:
                checkNext = False
        if (c == "u") or (c == "U"):
            checkNext = True
        elif (c == " "):
            prevSpace = True
            checkNext = False
        else:
            prevSpace = False
            checkNext = False

    return (uhCount)


def likeCounter(transc):
    likeCount = 0
    word = ""
    prevSpace = True
    startCheck = False
    count = 0

    for c in transc: 
        if (startCheck):
            if (count < 3):
                word += c
                count += 1
            else: 
                if (word.lower() == "like"):
                    likeCount += 1
                word = ""
                prevSpace = False
                startCheck = False
                count = 0
        else:
            if(c == "L") or (c == "l"):
                word += "l"
                startCheck = True
            elif (c == " "):
                prevSpace = True
                startCheck = False
            else:
                prevSpace = False
                startCheck = False
        
    return (likeCount)


def hmmCounter(transc):
    hmmCount = 0
    word = ""
    prevSpace = True
    startCheck = False
    count = 0

    for c in transc: 
        if (startCheck):
            if (count < 2):
                word += c
                count += 1
            else: 
                if (word.lower() == "hmm"):
                    hmmCount += 1
                word = ""
                prevSpace = False
                startCheck = False
                count = 0
        else:
            if(c == "h") or (c == "H"):
                word += "h"
                startCheck = True
            elif (c == " "):
                prevSpace = True
                startCheck = False
            else:
                prevSpace = False
                startCheck = False
        
    return (hmmCount)


def mhmCounter(transc):
    mhmCount = 0
    word = ""
    prevSpace = True
    startCheck = False
    count = 0

    for c in transc: 
        if (startCheck):
            if (count < 2):
                word += c
                count += 1
            else: 
                if (word.lower() == "mhm"):
                    mhmCount += 1
                word = ""
                prevSpace = False
                startCheck = False
                count = 0
        else:
            if(c == "m") or (c == "M"):
                word += "m"
                startCheck = True
            elif (c == " "):
                prevSpace = True
                startCheck = False
            else:
                prevSpace = False
                startCheck = False
        
    return (mhmCount)




def buttonUpdate(data1,data2,data3,data4,data5):
    global orig1, delta1
    delta1 = data1 - orig1 
    orig1 = data1

    global orig2, delta2
    delta2 = data2 - orig2 
    orig2 = data2

    global orig3, delta3
    delta3 = data3 - orig3 
    orig3 = data3

    global orig4, delta4
    delta4 = data4 - orig4 
    orig4 = data4

    global orig5, delta5
    delta5 = data5 - orig5 
    orig5 = data5



    #Metrics
    #***
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.metric(label="Um's", value=orig1, delta=delta1)
    with col2:
        st.metric(label="Uh's", value=orig2, delta=delta2)
    with col3:
        st.metric(label="Like's", value=orig3, delta=delta3)
    with col4:
        st.metric(label="Hmm's", value=orig4, delta=delta4)
    with col5:
        st.metric(label="Mhm's", value=orig5, delta=delta5)


    #Chart
    #***
    # print (np.random.rand(30, 5))
    finalTextNum = 0
    filepath = 'transcribe.srt.txt'
    with open(filepath) as fp:
        line = fp.readline()
        count = 0
        while line:
            if (count%4 == 0):
                finalTextNum = line
            # print("Line {}: {}".format(count, line.strip()))
            line = fp.readline()
            count += 1
    # print("\nFinal text num")
    # print(finalTextNum)

    # to get the number of lines per section divide the finalTextnum by 30 (since 30 columns in the graph)
    sectionNum = int((int(finalTextNum)/30)) * 4



    everything = []

    with open(filepath) as fp:
        line = fp.readline()
        count = 0
        while line:
            if (count%4 == 2):
                finalTextNum = line
                # print("Line {}: {}".format(count, line.strip()))
                everything.append(line)
                
            line = fp.readline()
            count += 1

    sectionSize = int(len(everything)/30)

    counter = 0
    dictCount = 0
    stringer = ""
    Dict = {} 
    for x in everything:
        if (counter < sectionSize):
            stringer += x
        else:
            # print (stringer)
            Dict[dictCount] = stringer
            stringer = ""
            dictCount += 1
            counter = 0
        counter += 1


    realDict = []
    um = 0
    uh = 0
    like = 0
    hmm = 0
    mhm = 0
    dicCount = 0

    for x in range(0,len(Dict)):
        realDict.append([umCounter(Dict[x]), uhCounter(Dict[x]), likeCounter(Dict[x]), hmmCounter(Dict[x]), mhmCounter(Dict[x])])

    
    df = pd.DataFrame(realDict,columns=['um', 'uh', 'like', 'hmm', 'mhm'])
    st.bar_chart(df)
    
    #***
def youtube_call(url):
    vid = YouTube(url)
    audio = vid.streams.get_audio_only()
    audio.download()


def transcribe():
    with st.spinner('Uploading file...'):
        bar = st.progress(0)
        current_dir = os.getcwd()
        for file in os.listdir(current_dir):
            if file.endswith(".mp4"):
                mp4_file = os.path.join(current_dir, file)
                #print(mp4_file)
        filename = mp4_file
        bar.progress(20)

        def read_file(filename, chunk_size=5242880):
            with open(filename, 'rb') as _file:
                while True:
                    data = _file.read(chunk_size)
                    if not data:
                        break
                    yield data
        headers = {'authorization': api_key}
        response = requests.post('https://api.assemblyai.com/v2/upload',
                                headers=headers,
                                data=read_file(filename))
        audio_url = response.json()['upload_url']
        
        #st.info('3. YouTube audio file has been uploaded to AssemblyAI')
        bar.progress(30)

        endpoint = "https://api.assemblyai.com/v2/transcript"

        json = {
        "audio_url": audio_url,
        "auto_highlights": True, #add
        "disfluencies": True
        }

        headers = {
            "authorization": api_key,
            "content-type": "application/json"
        }

        transcript_input_response = requests.post(endpoint, json=json, headers=headers)

        #st.info('4. Transcribing uploaded file')
        bar.progress(40)

        # 5. Extract transcript ID
        transcript_id = transcript_input_response.json()["id"]
        #st.info('5. Extract transcript ID')
        bar.progress(50)

        # 6. Retrieve transcription results
        endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
        headers = {
            "authorization": api_key,
        }
        transcript_output_response = requests.get(endpoint, headers=headers)
        #st.info('6. Retrieve transcription results')
        bar.progress(60)

        # Check if transcription is complete
        

        while transcript_output_response.json()['status'] != 'completed':
            time.sleep(10)
            transcript_output_response = requests.get(endpoint, headers=headers)
    
    st.success('Transcription complete.')
    bar.progress(100)

    # 7. Print transcribed text
    st.header('Output')
    st.info(transcript_output_response.json()["text"])

    # 8. Save transcribed text to file

    # Save as TXT file
    transcribe_txt = open('transcribe_txt', 'w')
    transcribe_txt.write(transcript_output_response.json()["text"])
    transcribe_txt.close()

    # Save as SRT file
    srt_endpoint = endpoint + "/srt"
    srt_response = requests.get(srt_endpoint, headers=headers)
    with open("transcribe.srt", "w") as _file:
        _file.write(srt_response.text)

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

#Empty container for spacing
st.empty()
st.markdown("Welcome to Project Speakr! Utilizing AssemblyAI's Speech to text function, this program aims to improve your public speaking skills and make you aware of your filler word habits. To begin, you may upload a local file, a YouTube video URL, or start a live recording now! Afterwards, that data will be processed into quantifiable form under 'Show Data'. ")
st.write("\n")

st.warning("Option 1: File upload")
uploaded_file = st.file_uploader('Choose File', type=["mp4"])
if uploaded_file:
    submit_button = st.button('Submit File')
    if submit_button:
        transcribe()

st.write("\n")

st.warning("Option 2: YouTube URL")
url = st.text_input('Enter the URL of the YouTube video:')

st.write("\n")

st.warning("Option 3: Live recording")

# Create two columns for buttons, one for start and one for stop
start, col2, col3, stop = st.columns(4)
# Create the two buttons
start.button('Start Recording', on_click = start_listening)
stop.button('Finish Recording', on_click = stop_listening)

st.write("\n")
data_button = st.button('Show Data')


if url is not None:
    #youtube_call(url)
    #transcribe()
    print(":)")
    #with open("transcription.zip", "rb") as download:
    #    btn = st.download_button(
    #        label="ZIP",
    #        data=download,
    #        file_name="transcription.zip",
    #        mime="application/zip"
    #    )

if data_button:
    with st.spinner('Processing data...'):
        bar1 = st.progress(20)
        time.sleep(0.4)
        bar1.progress(36)
        time.sleep(1)
        bar1.progress(60)
        time.sleep(1)
        bar1.progress(72)
        time.sleep(3)
        bar1.progress(100)
        time.sleep(1)
    st.success('Done!')
    st.header("Speech Analytics")

    f = open("transcribe_txt.txt", "r")
    transc = f.readline()

    buttonUpdate(umCounter(transc),uhCounter(transc),likeCounter(transc),hmmCounter(transc),mhmCounter(transc))
  