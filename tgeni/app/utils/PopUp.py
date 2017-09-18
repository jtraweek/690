'''
Created on Sep 15, 2017

@author: Default
'''
from tkinter import Tk, RIGHT, BOTH, RAISED,N , TOP
from tkinter.ttk import Frame, Button, Style, Label

root = Tk()
class Confirm(Frame):
  
   
    def __init__(self,foo):
        super().__init__() 
        self.initUI()
        self.func=foo      
       

    def Yes(self):                          #function
        self.func()
        root.destroy()

    def No(self):                          #function
        root.destroy()
        
    def initUI(self):
      
        self.master.title("Confirmation")
        self.style = Style()
        self.style.theme_use("default")
        
        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)
        
        lbl = Label(frame, text="Are you sure?", width=20)
        lbl.pack(side=TOP, anchor=N, padx=5, pady=60)
        
        self.pack(fill=BOTH, expand=True)
        
        noButton = Button(self, text="No", command = self.No)
        noButton.pack(side=RIGHT, padx=5, pady=5)
        yesButton = Button(self, text="YES", command = self.Yes)
        yesButton.pack(side=RIGHT)
              
        root.geometry('300x200+300+300')
 
