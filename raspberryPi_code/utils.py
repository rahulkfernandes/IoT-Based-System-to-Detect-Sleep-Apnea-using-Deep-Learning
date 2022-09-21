import os.path
import os
import csv
import socket
import subprocess
import sys
from const import SERVER_IP, BUFFER_SIZE, localIP, localPort1, localPort2

def create_csv (fields):

    if (os.path.exists("./Sensor_Readings.csv")==True):
        os.remove("./Sensor_Readings.csv")
        print ("File Replaced")
    
    with open("Sensor_Readings.csv", 'w', encoding="utf-8") as f:
        write = csv.writer(f)
        write.writerow(fields)
        f.close()

def output_to_csv (readings):
    with open("Sensor_Readings.csv", 'a', newline='') as f_object:
        writer_object = csv.writer(f_object)
        writer_object.writerow(readings)

#UDP DOES NOT WORK
#def UDP_sender (readings):
#    sensor_readings = readings[1:-1]
#    bytesToSend = sensor_readings.encode("UTF-8")
#    serverAddressPort = (SERVER_IP,localPort1)
#    UDPClientSocket =  socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
#    UDPClientSocket.sendto(bytesToSend,serverAddressPort)
#    msgFromServer = UDPClientSocket.recvfrom(BUFFER_SIZE)
#    return msgFromServer[0].decode("UTF-8")

