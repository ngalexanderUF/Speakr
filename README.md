# Speakr
SwampHacks2022
Team members: Alexander Ng, Kevin Zhang, Taise Miyazumi, Tyler Wong


## Demo Video 
https://youtu.be/jTd-uNEC_PA

## Introduction
Welcome to Project Speakr: Utilizing AssemblyAI's Speech to text function, this program aims to improve your public speaking skills and make you aware of your filer word habits.

#### Project Description
Our project has three main functions for the detection of filler words and resultant analytics. The three functions comprise of a real-time speech-to-text transcription feature, a local file upload, and a transcription of a YouTube video derived from its url. After transcribing the videos, there will be data/statistics generated for the user to output the frequency with which the user used filler words, displayed neatly on a bar graph delineated by the sectionalized duration of the video. From there, the user would utilize this data to keep track of their improvements in speaking and communication.

#### Built With
We utilized Streamlit as our front-end interface for the website interaction. On the back-end we called into the AssemblyAi API and passed in a media source either from a local drive or YouTube. We used python coding language overall to interact with the text files and perform data manipulation to achieve the data analytics.


#### Challenge
The team that builds the best project using the AssemblyAI API. 


## Getting Started
#### Prerequisites
Have Python3 and pip downloaded

How to install and run!

1) Clone the repo
```sh
git clone https://github.com/ngalexanderUF/Speakr.git
```

2) Obtain your AssemblyAI API key by signing up with Assembly.AI


3) Install necessary tools
```sh
pip3 install pytube
```

4) Install PyAudio
```sh
pip install PyAudio
```

5) Install websocket
```sh
pip install websocket-client
```

6) Use Pip to install libraries from Streamlit app
```sh
pip install -r requirements.txt
```

7) Launce the streamlit on a localhost
```sh
streamlit run app.py
```
