# Main program

# import modules
import sys
import numpy as np
import time
import matplotlib.pyplot as plt
import Window
from comtypes.client import GetModule
from comtypes.client import CreateObject
from scipy.signal import find_peaks
from scipy.signal import medfilt
from PyQt5 import QtGui, QtWidgets
import threading
import pyqtgraph as pg
# ---------------------------------------------------------------------------------------
# Define the functions to control the Keysight oscilloscope
# Run GetModule once to generate comtypes.gen.VisaComLib.
if not hasattr(sys, "frozen"):
    GetModule("C:\Program Files (x86)\IVI Foundation\VISA\VisaCom\GlobMgr.dll")

import comtypes.gen.VisaComLib as VisaComLib

# Initialize the oscilloscope, capture data, and analyze.
def do_query_number(query):
    myScope.WriteString("%s" % query, True)
    result = myScope.ReadNumber(VisaComLib.ASCIIType_R8, True)
    check_instrument_errors(query)
    return result
def do_query_ieee_block(query):
    myScope.WriteString("%s" % query, True)
    result = myScope.ReadIEEEBlock(VisaComLib.BinaryType_UI1, \
    False, True)
    check_instrument_errors(query)
    return result
def check_instrument_errors(command):
    while True:
        myScope.WriteString(":SYSTem:ERRor?", True)
        error_string = myScope.ReadString()
        if error_string: # If there is an error string value.
            if error_string.find("+0,", 0, 3) == -1: # Not "No error".
                print("ERROR: %s, command: '%s'" % (error_string, command))
                print("Exited because of error.")
                sys.exit(1)
            else: # "No error"
                break
        else: # :SYSTem:ERRor? should always return string.
            print("ERROR: :SYSTem:ERRor? returned nothing, command: '%s'" \
            % command)
            print("Exited because of error.")
            sys.exit(1)
def do_command(command) -> object:
    myScope.WriteString("%s" % command, True)
    check_instrument_errors(command)
def do_query_numbers(query):
    myScope.WriteString("%s" % query, True)
    result = myScope.ReadList(VisaComLib.ASCIIType_R8, ",;")
    check_instrument_errors(query)
    return result
# Send a query, check for errors, return string:
def do_query_string(query):
    myScope.WriteString("%s" % query, True)
    result = myScope.ReadString()
    check_instrument_errors(query)
    return result

# ---------------------------------------------------------------------------------------
# Main program
rm = CreateObject("VISA.GlobalRM", interface=VisaComLib.IResourceManager)
myScope = CreateObject("VISA.BasicFormattedIO", interface=VisaComLib.IFormattedIO488)
# Input the LAN address of oscilloscope
#myScope.IO = rm.Open("TCPIP0::169.254.187.83::INSTR")
myScope.IO = rm.Open('USB0::2391::6040::MY58103447::INSTR')
# Clear the interface.
myScope.IO.Clear()
print("Interface cleared.")
# Set the Timeout to 15 seconds.
myScope.IO.Timeout = 15000  # 15 seconds.
print("Timeout set to 15000 milliseconds.")

#Set the main demostration program
class MAIN(Window.Window):
    def __init__(self, parent=None):
        super(MAIN, self).__init__(parent)
        self.display_img('check',self.fig_metal)
        self.th0 = threading.Thread(target=self.datacp)
        self.buttonstrat()

    def trigger(self):
        self.th0.start()
        pass

    def buttonstrat(self):
        self.StartButton.clicked.connect(self.trigger)

    def calT(self, data, clip=10, distance=10, width=10):
        data_proc = medfilt(data, kernel_size=1)
        peaks, _ = find_peaks(data_proc[clip:], distance=distance, width=width)
        valleys, _ = find_peaks(-data_proc[clip:], distance=distance, width=width)
        plt.plot(data)
        plt.plot(data_proc)
        plt.plot(peaks + clip, data_proc[clip + peaks], "x")
        plt.plot(valleys + clip, data_proc[clip + valleys], "o")
        plt.savefig('plot.jpg')

        polar_points = np.sort(np.concatenate([peaks, valleys]))
        half_T = np.diff(polar_points).mean()
        print('half_T is: ', half_T)
        T = 2 * half_T
        return T

    def calL(self, T):
        # given the system inductance (H) and capacitance (F)
        Ls = 0
        Cs = 0
        Tp = 0 * T
        C = 0
        return C

    def show_result(self, period):
        # given the initial period of the system
        T0 = 0
        # calculate the a
        a = (T0-period)/period
        if a > 0.01:
            self.display_img('withmetal', self.fig_metal)
            print("1")
        else:
            self.display_img('withoutmetal', self.fig_metal)
            print("2")
        return None

    def datacp(self):
        (wav_form,
         acq_type,
         wfmpts,
         avgcnt,
         x_increment,
         x_origin,
         x_reference,
         y_increment,
         y_origin,
         y_reference
         ) = do_query_numbers(":WAVeform:PREamble?")
        print("Waveform points desired: %d" % wfmpts)
        print("Waveform average count: %d" % avgcnt)
        print("Waveform X increment: %1.12f" % x_increment)
        print("Waveform X origin: %1.9f" % x_origin)
        print("Waveform X reference: %d" % x_reference)  # Always 0.
        print("Waveform Y increment: %f" % y_increment)
        print("Waveform Y origin: %f" % y_origin)
        print("Waveform Y reference: %d" % y_reference)  # Always 125.
        # Get numeric values for later calculations.
        x_increment = do_query_number(":WAVeform:XINCrement?")
        x_origin = do_query_number(":WAVeform:XORigin?")
        y_increment = do_query_number(":WAVeform:YINCrement?")
        y_origin = do_query_number(":WAVeform:YORigin?")
        y_reference = do_query_number(":WAVeform:YREFerence?")
        # Get the waveform data.
        # Get the number of waveform points available.
        do_command(":WAVeform:POINts 500")
        qresult = do_query_string(":WAVeform:POINts?")
        print("Waveform points available: %s" % qresult)
        self.Alldata = np.array(range(500))
        while 1:
            do_command(":SINGle")
            time.sleep(2.35)
            data_bytes = do_query_ieee_block(":WAVeform:DATA?")
            nLength = len(data_bytes)
            voltage = []
            for i in range(0, nLength):
                # time_val = x_origin + (i * x_increment)
                voltage.append((data_bytes[i] - y_reference) * y_increment + y_origin)

            print("Number of data values: %d" % len(voltage))
            pX = np.arange(0, len(voltage))
            pY = np.array(voltage, dtype=np.float)

            takendata = pY[1:500]
            period = self.calT(takendata)
            inductance = self.calL(period)
            final = self.show_result(period)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MAIN()
    window.show()
    sys.exit(app.exec())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
