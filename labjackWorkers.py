import time
import sys
import os
import datetime
import numpy as np
from labjack import ljm




def TimestampMillisec64():
    return int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)

class Signals(QObject):
    dataOut = pyqtSignal(list)


class readingWorker(QRunnable):
    def __init__(self):
        super().__init__()
        self.readingStatus = False

    def run(self):
        # was 72
        FIRST_AIN_CHANNEL = 0  # 0 = AIN0 , 72 = ?
        NUMBER_OF_AINS = 14 # Max number of AIN channels required

        # Open first found  T7 LabJack
        handle = ljm.openS("T7", "ANY", "ANY")  # T7 device, Any connection, Any identifier


        info = ljm.getHandleInfo(handle)
        deviceType = info[0]

        try:
            ##configuration
            # Ensure triggered stream is disabled.
            ljm.eWriteName(handle, "STREAM_TRIGGER_INDEX", 0)
            # Enabling internally-clocked stream.
            ljm.eWriteName(handle, "STREAM_CLOCK_SOURCE", 0)

            # AIN ranges are +/-10 V and stream resolution index is 0 (default).
            aNames = ["AIN_ALL_RANGE", "STREAM_RESOLUTION_INDEX"]
            aValues = [10.0, 0]

            # set to single ended and auto settling time
            aNames.extend(["AIN_ALL_NEGATIVE_CH", "STREAM_SETTLING_US"])
            aValues.extend([ljm.constants.GND, 0])

            # Stream configuration
            aScanListNames = ["AIN%i" % i for i in range(FIRST_AIN_CHANNEL, FIRST_AIN_CHANNEL + NUMBER_OF_AINS)]  # Scan list names
            print("\nScan List = " + " ".join(aScanListNames))
            numAddresses = len(aScanListNames)
            aScanList = ljm.namesToAddresses(numAddresses, aScanListNames)[0]
            scanRate = 1000
            print("scanRate:", scanRate)
            scansPerRead = int(scanRate / 2)

            # Configure and start stream
            scanRate = ljm.eStreamStart(handle, scansPerRead, numAddresses, aScanList, scanRate)
            
            #curSkip = 0
            while self.readingStatus:
                ret = ljm.eStreamRead(handle)
                data = ret[0]
                deinterleaved = [data[idx::numAddresses] for idx in range(numAddresses)]
                data_array = np.array(deinterleaved)


                time_col = np.full((len(data_array[0]), 1), TimestampMillisec64())

                # transpose data so its organized correctly for csv
                all_data = np.hstack((time_col, data_array.T))
                self.Row = all_data[1].tolist()
                data_q.put(all_data)
                #time.sleep(0.1)

        except ljm.LJMError:
            ljme = sys.exc_info()[1]
            print(ljme)
        except Exception:
            e = sys.exc_info()[1]
            print(e)

        try:
            print("\nStop Stream")

            ljm.eStreamStop(handle)

        except ljm.LJMError:
            ljme = sys.exc_info()[1]
            print(ljme)
        except Exception:
            e = sys.exc_info()[1]
            print(e)


        ljm.close(handle)

    def stop(self):
        self.readingStatus = False

class loggingWorker(QRunnable):
    def __init__(self):
        super().__init__()
        self.loggingStatus = False

    def run(self):
        #now = datetime.now()
        self.time_string = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")+".csv"
        while self.loggingStatus:
            with open("LabJack_Data_"+self.time_string, 'ab') as csvfile:
            #with open("LabJack_Data_"+self.time_string, 'ab') as csvfile:
                #get data array from the queue
                data = data_q.get()
                np.savetxt(csvfile, data, delimiter=",")



    def stop(self):
        self.loggingStatus = False

class displayWorker(QRunnable):

    def __init__(self):
        super().__init__()
        self.displaySignal = Signals()
        self.displayStatus = False
        self.loggingcheck = False

    def run(self):
        while self.displayStatus:
            if self.loggingcheck:
                with open(self.csv_name, 'rb') as f:
                    try:  # catch OSError in case of a one line file
                        f.seek(-2, os.SEEK_END)
                        while f.read(1) != b'\n':
                            f.seek(-2, os.SEEK_CUR)
                    except OSError:
                        f.seek(0)

                    last_line = f.readline().decode()
                    if len(last_line) > 0:
                        vals_strings = last_line.split(",")
                        vals = []
                        for string in vals_strings:
                            vals.append(float(string))
                        self.vals_array = vals
                        self.displaySignal.dataOut.emit(self.vals_array)
                        time.sleep(0.1)
            if not self.loggingcheck:
                
                self.displaydata = data_q.get()
                for i in range(5):
                    self.Row = self.displaydata[i*100].tolist()
                    self.displaySignal.dataOut.emit(self.Row)
                    time.sleep(0.01)


    def stop(self):
        self.displayStatus = False
        self.loggingcheck = False
