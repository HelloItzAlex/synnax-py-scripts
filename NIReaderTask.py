import numpy as np
import synnax as sy
from synnax.hardware import sequence
from synnax.hardware import ni

#connect to client
client = sy.Synnax(
    host="localhost",
    port=9090,
    username="synnax",
    password="seldon",
    secure=False
)
#Mass define channels to read from
readChanNamesNum = {
    "NI_9205_": 32,
    "NI_9253_": 8,
    "NI_9213_": 16,
    "NI_9237_": 4,
    "NI_9485A_": 8,
    "NI_9485B_": 8
}
readChannels = []
for name, count in readChanNamesNum.items():
    readChannels.extend([f"{name}{i}" for i in range(count)])
print(readChannels)
#Mass define channels to write to
writeChanNamesNum = {
    "Safety": 1
}
writeChannels = []
for name, count in writeChanNamesNum.items():
    writeChannels.extend([f"{name}{i}" for i in range(count)])
print(writeChannels)

#Open the reader and writer connection
with client.open_writer(start=sy.TimeStamp.now(),channels=writeChannels,enable_auto_commit=True,) as writer:
    with client.open_streamer(readChannels) as streamer:
        for frame in streamer:
            #Actions take place here 
            writer.write(
                {
                    #write stuff here 
                }
            )