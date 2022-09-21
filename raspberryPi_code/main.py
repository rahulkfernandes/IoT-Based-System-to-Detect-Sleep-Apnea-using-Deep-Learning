from sensors import Oxymeter, ECG
import threading
import time
import sys
import socket
from const import SAMPLE_RATE, OXYMETER_RATE, HEADERSIZE, localIP, localPort1
from utils import create_csv, output_to_csv

oxymeter = Oxymeter()
ecg = ECG()
start_time = time.time()
print("Start Time = ",f"{start_time}")
# reads the oxymeter values every 5 seconds
def read_oxymeter():
    while True:
        oxymeter.read_oxy()
        time.sleep(OXYMETER_RATE)


# reads the ecg values every 0.5 seconds
def read_ecg():
    while True:
        ecg.read_ecg()
        time.sleep(SAMPLE_RATE)

# sends the readings every 0.1 seconds.
def send_reading():
    readings = []
    fields = ["Pulse Rate", "SP02", "ECG"]
    #create_csv(fields)
    
    try:

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((localIP, localPort1))
        s.listen(5)

        while True:
            # now our endpoint knows about the OTHER endpoint.
            clientsocket, address = s.accept()
            print(f"Connection from {address} has been established.")

            #msg = f"{start_time}"
 

            #clientsocket.send(msg.encode("UTF-8"))

            while True:
            
                readings = [oxymeter.pulse, oxymeter.spo2, ecg.ecg]

                msg = f"{readings}"[1:-1]
         
                #msg = f"{len(msg):<{HEADERSIZE}}" + f"{readings}"[1:-1]           

                clientsocket.send(msg.encode("UTF-8"))
                #output_to_csv(readings)
                time.sleep(SAMPLE_RATE)
    except:
        s.close()
        sys.exit()
        
        #print (readings)
        #acknowledgement = UDP_sender(f"{readings}")
        #print (acknowledgement)
        
        

        #time.sleep(SAMPLE_RATE)

thread1 = threading.Thread(target=read_oxymeter)
thread1.start()
thread2 = threading.Thread(target=read_ecg)
thread2.start()
thread3 = threading.Thread(target=send_reading)
thread3.start()