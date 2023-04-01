import pyaudio
import speech_recognition as sr
import mysql.connector
import audioop
import json
import os


# set up audio recording
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
THRESHOLD = 3000
SILENCE_LIMIT = 2

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# set up speech recognition
r = sr.Recognizer()
r.energy_threshold = THRESHOLD
r.pause_threshold = SILENCE_LIMIT

# set up database connection
try:
    mydb = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USERNAME"),
        password=os.environ.get("DB_PASSWORD"),
        database= os.environ.get("DB_DATA")
    )
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")
    exit()

# record audio until there is no sound
frames = []
silence_count = 0
while True:
    data = stream.read(CHUNK)
    frames.append(data)
    rms = audioop.rms(data, 2)  # compute RMS energy of audio data
    if rms < THRESHOLD:
        silence_count += 1
    else:
        silence_count = 0
    if silence_count > SILENCE_LIMIT * RATE / CHUNK:
        break

# stop audio recording
stream.stop_stream()
stream.close()
p.terminate()

# convert audio to text using Google Cloud Speech-to-Text API
audio = sr.AudioData(b''.join(frames), RATE, 2)
try:
    text = r.recognize_google(audio)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
    exit()

# execute SQL query using the text
try:
    mycursor = mydb.cursor()
    query = "SELECT JSON_OBJECT( 'id', id, 'latitude', CAST(latitude AS CHAR), 'longitude', CAST(longitude AS CHAR), 'district', district, 'state', state, 'pincode', pincode, 'temperature', CAST(temperature AS CHAR), 'humidity', CAST(humidity AS CHAR), 'air_Quality', CAST(air_Quality AS CHAR), 'timestamp', timestamp, 'range', CAST(`range` AS CHAR)) AS data FROM record WHERE (`state` = %s OR `district` = %s) AND `range` < 0.5"

    params = (text, text)
    mycursor.execute(query, params)
    result = mycursor.fetchall()
    new_data = [eval(d[0]) for d in result]

    # Initialize the text-to-speech engine
    #engine = pyttsx3.init()

    # Set the speaking rate (optional)
    #engine.setProperty('rate', 150)

    # Set the speaking voice (optional)
    #voices = engine.getProperty('voices')
    #engine.setProperty('voice', voices[1].id)  # Change the index to select a different voice

    # Speak out the message
    #message = "There are total " + str(len(new_data)) + " points with low range."
    #engine.say(message)
    #engine.runAndWait()


    #print(new_data)
    response = {
        "success": True,
        "text": text,
        "queried_data": new_data
    }
    print(json.dumps(response))  # Serialize the response as a JSON object

except mysql.connector.Error as err:
    print(f"Error executing SQL query: {err}")
    response = {
        "success": False,
        "error": f"Error executing SQL query: {err}"
    }
    print(json.dumps(response))  # Serialize the response as a JSON object

