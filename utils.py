import os
import csv



def create_csv(file_path):
    if (os.path.exists(file_path)==True):
        os.remove(file_path)
        print ("FILE REPLACED")
    
        fields = ["Sample","PulseRate","SP02","ECG"]
        with open(file_path, 'w', encoding="utf-8") as f: 
            write = csv.writer(f)
            write.writerow(fields)
            f.close()
        
    else:
        fields = ["Sample","PulseRate","SP02","ECG"]
        with open(file_path, 'w', encoding="utf-8") as f: 
            write = csv.writer(f)
            write.writerow(fields)
            f.close()
