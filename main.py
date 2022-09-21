
import multiprocessing
from communication import TCP_Reciever2
from utils import create_csv
from app import application



def main():
    create_csv("./Recieved_readings.csv")  
    
   
    process1 = multiprocessing.Process(target=TCP_Reciever2)
    process1.start()
    process2 = multiprocessing.Process(target=application)
    process2.start()
   
    while(True):
        if process2.is_alive()==False:
            process1.terminate()
            print("Reciever Process Terminated!")
            exit()
            
if __name__ == "__main__":
    main()
