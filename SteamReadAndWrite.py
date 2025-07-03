import numpy as np
import synnax as sy
from synnax.hardware import sequence
from synnax.hardware import ni

# #connect to client
# client = sy.Synnax(
#     host="localhost",
#     port=9090,
#     username="synnax",
#     password="seldon",
#     secure=False
# )
chanNamesNum = {
    "NI_9205_": 32,
    "NI_9253_": 8,
    "NI_9213_": 16,
    "NI_9237_": 4
}
channels = []
for name, count in chanNamesNum.items():
    channels.extend([f"{name}{i}" for i in range(count)])
print(channels)


# AIN channel creation through loops and arrays 
# numVoltageAINChannels = 32 #Number of AIN channels to create
# AINchannelNames = [f"NI_T7_AIN{i}" for i in range(numAINChannels)] #Creates channel names "LJ_T7_AIN#" based on numAINChannels
# AINchannels = [] #Create array for AINchannels to go into 

# for name in AINchannelNames:
#     tempChannel = client.channels.create(
#         name=name,
#         index=timeChannel.key,
#         data_type=sy.DataType.FLOAT32,
#         retrieve_if_name_exists=True,
#     )
#     AINchannels.append(tempChannel)

# Relay channel creation through loops and arrays (would this be better as a task?)
# numRelayChannels = 1 #Number of channels to create
# relayChannelCMDNames = [f"LJ_T7_CMD{i}" for i in range(numRelayChannels)] #Creates channel names "LJ_T7_CMD#" based on numRelayChannels
# relayChannelSTATENames = [f"LJ_T7_STATE{i}" for i in range(numRelayChannels)] #Creates channel names "LJ_T7_STATE#" based on numRelayChannels
# relayChannelCMD = [] #Create array for AINchannels to go into 
# relayChannelSTATE = [] #Create array for AINchannels to go into 

# Create the CMD channels for 
# for name in relayChannelCMDNames:
#     tempChannel = client.channels.create(
#         name=name,
#         index=timeChannel.key,
#         data_type=np.bool_,
#         retrieve_if_name_exists=True,
#     )
#     relayChannelCMD.append(tempChannel)

# Create the STATE channels for 
# for name in relayChannelSTATENames:
#     tempChannel = client.channels.create(
#         name=name,
#         index=timeChannel.key,
#         data_type=np.bool_,
#         retrieve_if_name_exists=True,
#     )
#     relayChannelSTATE.append(tempChannel)


# channels = ["stream_write_time", "stream_write_data_1", "stream_write_data_2"]

# We will open the streamer with a context manager. The context manager will
# automatically close the streamer after we're done reading.
# with client.open_streamer(channels) as streamer:
#     Loop through the frames in the streamer. Each iteration will block until a new
#     frame is available, then we'll print out the frame of data.
#     while True:
#         print(streamer.read())










# ###################Commented out code####################################

# #AIN channel creation through Synnax shortut (Aarhus doesnt like this due it being possible to make dupicate channels)
# CHANNEL_COUNT = 5
# # Create data channels to store our data. Since we did not call client.channels.create
# # here, the channels are not actually created in the Synnax cluster yet. We will do that
# # in the next step.
# data_channels = [
#     sy.Channel(
#         name=f"Synnax_AIN{i}",
#         index=timeChannel.key,
#         retrieve_if_name_exists=True, <- this part throws an error when being ran. doesnt exist in .Channel, only .channels.create
#         data_type=sy.DataType.FLOAT32,
#     )
#     for i in range(CHANNEL_COUNT)
# ]

# # Notice how we reassign the result of the create call to the data_channels variable.
# # This means that all of the channels will have the correct key given to the channel by
# # the server.
# data_channels = client.channels.create(data_channels)

# # We'll start our write at the current time. This timestamp should be the same as or
# # just before the first timestamp we write.
# start = sy.TimeStamp.now()

# # The rate at which we'll send samples to the cluster. sy.Loop  is a utility to help
# # regulate the timing.
# loop = sy.Loop(sy.Rate.HZ * 25)

# # Open the writer as a context manager. Using a context manager is recommended as the
# # context manager will automatically close the writer when we are done writing. We will
# # write to both the time and data channels. To choose the channels to write to, you can
# # use either the keys or the names of the channels (here, we're using the keys).
# with client.open_writer(
#     start,
#     [timeChannel.key, dataChannel1.key, dataChannel2.key],
#     enable_auto_commit=True,
# ) as writer:
#     i = 0
#     while loop.wait():
#         # Write the data to the Synnax cluster using the writer.
#         writer.write(
#             {
#                 timeChannel.key: sy.TimeStamp.now(),
#                 dataChannel1.key: np.sin(i / 10) * 25 + 12.5,
#                 dataChannel2.key: i % 2,
#             }
#         )
#         i += 1