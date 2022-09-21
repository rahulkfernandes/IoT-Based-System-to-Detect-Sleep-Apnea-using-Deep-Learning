import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import max30100
import threading

class Oxymeter:
    
    def __init__(self):
        self.pulse = 0
        self.spo2 = 0
        self.formatted_values = ''
        self.mx30 = max30100.MAX30100()
        self.mx30.set_mode(max30100.MODE_SPO2)
        print ("Oxymeter Initialised")

    def read_oxy(self):
        self.mx30.read_sensor()
        self.mx30.ir, self.mx30.red

        self.pulse = int(self.mx30.ir / 100)
        self.spo2 = int(self.mx30.red / 100)

        if ((self.mx30.ir != self.mx30.buffer_ir) or
            (self.mx30.red != self.mx30.buffer_red)):
            
    
            self.formatted_values = f"{self.spo2}, {self.pulse}"

        print ("Oxygen sensor read")

    def __str__(self):
        return self.formatted_values

class ECG():

    def __init__(self):
        self.ecg = 0
        self.formatted_values = ''
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

        cs = digitalio.DigitalInOut(board.D5)

        mcp = MCP.MCP3008(spi, cs)

        self.ecg_channel = AnalogIn(mcp, MCP.P0)
        print ("ECG Sensor initialised!")
    
    def read_ecg(self):
        self.ecg = self.ecg_channel.voltage
        self.formatted_values = f"{self.ecg}"

        print ("ECG sensor read")

    def __str__(self):
        return self.formatted_values
