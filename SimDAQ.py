import numpy as np
import synnax as sy

client = sy.Synnax(
    host="localhost",
    port=9090,
    username="synnax",
    password="seldon",
    secure=False
)

time_channel = client.channels.create(
    name="stream_write_time",
    is_index=True,
    data_type=sy.DataType.TIMESTAMP,
    retrieve_if_name_exists=True,
)

# Create two data channels that will be used to store our data values. We'll need to
# pass in the key of the time channel to these data channels when they are created
data_channel_1 = client.channels.create(
    name="stream_write_data_1",
    index=time_channel.key,
    data_type=sy.DataType.FLOAT32,
    retrieve_if_name_exists=True,
)
data_channel_2 = client.channels.create(
    name="stream_write_data_2",
    index=time_channel.key,
    data_type=sy.DataType.UINT8,
    retrieve_if_name_exists=True,
)

# We'll start our write at the current time. This timestamp should be the same as or
# just before the first timestamp we write.
start = sy.TimeStamp.now()
print("I was here (1)")
# The rate at which we'll send samples to the cluster. sy.Loop  is a utility to help
# regulate the timing.
loop = sy.Loop(sy.Rate.HZ * 25)
print("I was here (2)")

# Open the writer as a context manager. Using a context manager is recommended as the
# context manager will automatically close the writer when we are done writing. We will
# write to both the time and data channels. To choose the channels to write to, you can
# use either the keys or the names of the channels (here, we're using the keys).
with client.open_writer(
    start,
    [time_channel.key, data_channel_1.key, data_channel_2.key],
    enable_auto_commit=True,
) as writer:
    print("I was here (3)")
    i = 0
    while loop.wait():
        print("I was here (4)")

        # Write the data to the Synnax cluster using the writer.
        writer.write(
            {
                time_channel.key: sy.TimeStamp.now(),
                data_channel_1.key: np.sin(i / 10) * 25 + 12.5,
                data_channel_2.key: i % 2,
            }
        )
        i += 1