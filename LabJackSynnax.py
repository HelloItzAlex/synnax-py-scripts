import numpy as np
import synnax as sy
from synnax.hardware import sequence
from labjack import ljm

#from labjackWorkers import TimestampMillisec64, Signals, readingWorker, loggingWorker, displayWorker

client = sy.Synnax(
    host="localhost",
    port=9090,
    username="synnax",
    password="seldon",
    secure=False
)

cycleAutoChannel = client.channels.create(
    name="cycleAutoChannel",
    data_type="unit8",
    virtual=True,
    retrieve_if_name_exists=True,
)
valveChannel = client.channels.create(
    name="valveChannel",
    data_type="uint8",
    virtual=True,
    retrieve_if_name_exists=True,
)
ch_key = cycleAutoChannel.key
print("I am here")
# Retrieve the control sequence from Synnax.
tsk = client.hardware.tasks.retrieve(name="AutoCycleFill")
sequence = sequence.Sequence(tsk)

print("I am here1")
# Open a stream on the signal channel. Start and stop the control sequence based on what
# gets written to the signal channel.
with client.open_streamer(ch_key) as streamer:
    print("I am here2")
    while True:
        print("I am here3")
        frame = streamer.read()
        if frame[ch_key] == 1:
            sequence.start() 
        elif frame[ch_key] == 0:
            sequence.stop()

#FIRST_AIN_CHANNEL = 0  # 0 = AIN0 ,
#NUMBER_OF_AINS = 14 # Max number of AIN channels required

#handle = ljm.openS("T7", "ANY", "ANY") # T7 device, Any connection, Any identifier
#info = ljm.getHandleInfo(handle)
#deviceType = info[0]

