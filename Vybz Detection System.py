#!/usr/bin/env python

import pyaudio
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
import threading
import Tkinter
from Tkinter import TclError
from Tkinter import *
from twilio.rest import Client


account_sid = "AC55edeb6dccd92e62fccbf2c216534d0e"
auth_token = "0d12a6cdd8ed82baa178d85dc00e5d31"

client = Client (account_sid, auth_token)



CHUNK = 1024 * 9             # samples per frame
FORMAT = pyaudio.paInt16     # audio format (bytes per sample?)
CHANNELS = 1                 # single channel for microphone
RATE = 48000                # samples per second
COUNTER_THRESHOLD = 5     # counter threshold for printing message
STD_THRESHOLD = 93

global run_loop
run_loop = False

p = pyaudio.PyAudio()

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

root = Tkinter.Tk()

def Vybz():
        error_count = 0
        counter = 0
        mssg_counter = 0
        
        while run_loop:
            # binary data
            try:
                    data = stream.read(CHUNK)
            except:
                    error_count += 1
            #convert data to integers, make np array, then offset it by 127
            data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
            
            #create np array and offset by 128
            data_np = np.array(data_int, dtype='b')[::2] + 128

            print int(np.std(data_int))
    
            if (np.std(data_int) < STD_THRESHOLD):
                counter += 1
                if counter > COUNTER_THRESHOLD:
                    # TODO - print the big message on the website
                    print("You're being too loud your RA can hear you!")
                    v.set("You're being too loud your RA can hear you!")
                    mssg_counter += 1
                    if mssg_counter == 5:
                            client.messages.create(
                                    to = "+16514915677",
                                    from_ = "+13142691567",
                                    body = "You're being too loud your RA can hear you!"
                                )
                    

            else:
                counter = 0
                v.set("Party on!")

def startLoop():
        global run_loop
        run_loop = True
        thread = threading.Thread(target=Vybz)
        thread.start()

def stopLoop():
        global run_loop
        run_loop = False

B = Tkinter.Button(root, text="Are you being too noisy?", command=startLoop)
C = Tkinter.Button(root, text="Stop", command=stopLoop)
v = StringVar()
D = Tkinter.Label(root, text="Party on!")
Label(D, textvariable=v).pack()


B.pack()
C.pack()
D.pack()

root.title("The Vybz")
root.geometry("400x100")
root.mainloop();
