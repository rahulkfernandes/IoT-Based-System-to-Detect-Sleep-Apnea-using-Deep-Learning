import socket
import csv
from const import Server_IP, Server_Port
import pandas as pd


def TCP_Reciever2():
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((Server_IP, Server_Port))
        
        while True:
            msg = s.recv(576)
            msg_string = msg.decode("UTF-8")
            #print(msg_string)
            #msg_split = msg_string[1:-1]
            msg_list = msg_string.split(',',3)
            try:
                #Setting initial value of the counter to zero
                rowcount = 0
                #iterating through the whole file
                for row in open("Recieved_readings.csv"):
                    rowcount+= 1

                ecg = [rowcount,msg_list[0],msg_list[1],msg_list[2]]
                with open("Recieved_readings.csv", 'a', encoding="UTF-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(ecg)
                #print(f"{ecg}"[1:-1])
            
            except IndexError:
                print("IndexError!")
                continue
            
    except KeyboardInterrupt:
        s.close()
        exit()



#UDP DOES NOT WORK!!
#def UDP_reciever():

#    try:
#        msgFromServer = "Recieved" #Acknowlodgement message
#        bytesToSend = msgFromServer.encode("UTF-8")
#        UDPServerSocket =socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
#        UDPServerSocket.bind((LocalIP,LocalPort))#

#        print("UDP Reciever Running")


#        while True:
#            bytesAddressPair = UDPServerSocket.recvfrom(BUFFER_SIZE)
#            message = bytesAddressPair[0]
#            address = bytesAddressPair[1]
            
#            with open("Recieved_readings.csv", 'a', encoding="UTF-8") as f:
#                writer = csv.writer(f)
#                writer.writerow(message.decode("UTF-8"))
#            print (message.decode("UTF-8"))
            
#            UDPServerSocket.sendto(bytesToSend,address)
#    except KeyboardInterrupt:
#        UDPServerSocket.close()
#        sys.exit()