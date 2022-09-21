import time
from datetime import datetime
import tkinter as tk
import customtkinter
import matplotlib
import pandas as pd

from const import SAMPLES
matplotlib.use("TkAgg")
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from predictor import processing, predict
#from matplotlib.figure import Figure

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

    
def animate(i):
    data = pd.read_csv('Recieved_readings.csv')
    x = data['Sample']
    y1 = data['ECG']
    
    #plt.set_figwidth(10)
    plt.cla()

    plt.plot(x, y1, label='ECG',linewidth=0.2, color='c')   #Comment this line and uncomment next line for light mode
    #plt.plot(x, y1, label='ECG',linewidth=0.2)


    plt.legend(loc='upper left')
    plt.tight_layout()

#plt.tight_layout()
#plt.show()

#Main Class to contain all pages
class App(tk.Tk):
     
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Apnea Detector")
        self.geometry("1280x720")
         
        # creating a container
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {} 
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Main_Page, ML_Page):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(Main_Page)
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
  
#PAGE1
class Main_Page(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)

        #============Show Live ECG Graph=============
        canvas = FigureCanvasTkAgg(plt.gcf(), self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.X, expand=False)
        #toolbar = NavigationToolbar2Tk(canvas, self,pack_toolbar=True)
        #toolbar.pack(side=tk.TOP, fill=tk.X,padx=10,anchor=tk.CENTER,expand=True)
        #toolbar.update()
        
        #===========Import Icon Images================
        add_ml_image = ImageTk.PhotoImage(Image.open("Icons/2010152-200.png").resize((30,30), Image.ANTIALIAS))
        add_save_image = ImageTk.PhotoImage(Image.open("Icons/download-icon-save+icon-1320167995084087448_512.png").resize((30,30), Image.ANTIALIAS))

        #===========Create Two Freames================
        self.frame1 = customtkinter.CTkFrame(master=self,width=640,height=100,corner_radius=10)
        self.frame1.pack(side=tk.BOTTOM,padx=10, pady=10, anchor=tk.CENTER)
        
        self.frame2 = customtkinter.CTkFrame(master=self,width=1280,height=100,corner_radius=10)
        self.frame2.pack(side=tk.BOTTOM,padx=10, pady=10, anchor=tk.CENTER, expand=True)

        #============Create Buttons====================
        self.ML_button = customtkinter.CTkButton(master=self.frame1, image=add_ml_image, text="Run ML Model", width=190, height=40, compound="left", command=lambda : controller.show_frame(ML_Page))
        self.ML_button.pack(side=tk.RIGHT,padx=10,pady=10, anchor=tk.E)

        self.button = customtkinter.CTkButton(master=self.frame1, image=add_save_image, text="Save Image", width=190, height=40, compound="left", command=self.save_graph)
        self.button.pack(side=tk.RIGHT,padx=10,pady=10, anchor=tk.CENTER)

        self.button = customtkinter.CTkButton(master=self.frame1, text="Exit", width=190, height=40, command=self.exit)
        self.button.pack(side=tk.LEFT,padx=10,pady=10, anchor=tk.W)

        #============Display Text=======================
        self.clock_label = customtkinter.CTkLabel(self.frame2,text= "",text_font=("Times New Roman", 25))
        self.clock_label.pack(side=tk.LEFT,padx=100,pady=30, anchor=tk.W)
        
        self.sp02_label = customtkinter.CTkLabel(self.frame2,text= "",text_font=("Times New Roman", 25))
        self.sp02_label.pack(side=tk.RIGHT,padx=100,pady=30, anchor=tk.E)

        self.pulse_label = customtkinter.CTkLabel(self.frame2,text= "",text_font=("Times New Roman", 25))
        self.pulse_label.pack(side=tk.LEFT,padx=100,pady=30, anchor=tk.CENTER)
        
        self.clock()
        
        self.get_pulse() 
        self.get_sp02()
        
    
    #To Display Pluse Rate every 1sec
    def get_pulse(self):
        pulse_data = pd.read_csv("Recieved_readings.csv")
        pulse = pulse_data.at[pulse_data.index[-1],'PulseRate']
        self.pulse_label.config(text=f"Pulse Rate: {pulse}")
        self.pulse_label.after(1000,self.get_pulse)
    
    #To Display Sp02 every 1sec
    def get_sp02(self):
        sp02_data = pd.read_csv("Recieved_readings.csv")
        sp02 = sp02_data.at[sp02_data.index[-1],'SP02']
        self.sp02_label.config(text=f"SP02: {sp02}")
        self.sp02_label.after(1000,self.get_sp02)
    
    #To Display Clock
    def clock(self):
        hh= time.strftime("%I")
        mm= time.strftime("%M")
        ss= time.strftime("%S")
        #day=time.strftime("%A")
        #ap=time.strftime("%p")
        #time_zone= time.strftime("%Z")
        self.clock_label.config(text="Time: " + hh + ":" + mm +":" + ss)
        self.clock_label.after(1000,self.clock)

        #my_lab1.config(text=time_zone+" "+ day)
        
    #Update the Time
    def updateTime(self):
        self.clock_label.config(text= "New Text")

    #To Save Graph Image
    def save_graph(self):
        plt.savefig(f"Saved_Images/ECG_{datetime.now()}.png", dpi=600)
    
    def exit(self):
        exit()
   
    #def on_closing(self, event=0):
    #    self.destroy()

#PAGE 2
class ML_Page(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)

        #=================Import Icon=================
        add_start_image = ImageTk.PhotoImage(Image.open("Icons/5199939.png").resize((200,200), Image.ANTIALIAS))

        #==============Create Start Button============
        self.run_button = customtkinter.CTkButton(master=self, image= add_start_image,text="", width=400, height=200,compound="top", command=self.ML)
        self.run_button.pack(side=tk.TOP, padx=20,pady=20,anchor=tk.CENTER)

        #================Create Frames================
        self.frame1 = customtkinter.CTkFrame(master=self,width=640,height=100,corner_radius=10)
        self.frame1.pack(side=tk.BOTTOM,padx=10, pady=10, anchor=tk.CENTER)
        
        self.frame2 = customtkinter.CTkFrame(master=self,width=400,height=200,corner_radius=10)
        self.frame2.pack(side=tk.TOP,padx=10, pady=10, anchor=tk.CENTER)

        #==============Display ML Status==============
        self.status_label= customtkinter.CTkLabel(self.frame2, text="CLICK BUTTON TO START")
        self.status_label.pack(side=tk.TOP,padx=110, pady=80, anchor=tk.CENTER)

        #==============Back & Exit Buttons============
        self.back_button = customtkinter.CTkButton(master=self.frame1,text="Back", width=190, height=40, command=lambda : controller.show_frame(Main_Page))
        self.back_button.pack(side=tk.RIGHT,padx=10,pady=10, anchor=tk.CENTER)

        self.button = customtkinter.CTkButton(master=self.frame1, text="Exit", width=190, height=40, command=self.exit)
        self.button.pack(side=tk.LEFT,padx=10,pady=10, anchor=tk.W)

    #Start Model Prediction
    def ML(self):
        #2580000 samples threshold set by developer, minimum is 2560000
        csv_len = pd.read_csv('Recieved_readings.csv')
        if (len(csv_len)<2580000):                              #2580000 is 7hrs 10mins,2560000 is approx 7hrs 5mins and is must for model
            self.status_label.config(text="NO SUFFICIENT DATA") 
    
        else:
            self.status_label.config(text="LOADING")
              
            ecg_data = pd.read_csv('Recieved_readings.csv', skiprows=12000) #Skip first 2 minutes of data to avoid noisy signal
            ecg= ecg_data['ECG']
            dict = {'ECG' : ecg}
            df = pd.DataFrame(dict)
            df.to_csv('Data/ecg.csv',mode='w', index=False)
        
            processed_signal = processing('Data/ecg.csv',SAMPLES)
        #processed_signal = processing("ML_Samples/x01.csv",SAMPLES)
            prediction = predict(processed_signal)

            self.status_label.config(text=f"{prediction}")

            
        
    def exit(self):
        exit()

#==============Driver Code=================
#if __name__ == "__main__": 
def application():                             #Comment this line and uncomment above line to isolate App GUI
    customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("blue")
    plt.style.use('dark_background')           #Comment this line and uncomment next line for light mode
    #plt.style.use('fivethirtyeight')
    app = App()
    ani = FuncAnimation(plt.gcf(), animate, interval=100)
    
    app.mainloop()