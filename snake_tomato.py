# Simple Python app for Pomodoro Method
# Copyright (C) 2018  Stefan H. Reiterer stefan.harald.reiterer@gmail.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Imports
from __future__ import print_function
import time, sched
import threading
import multiprocessing

# tkinter version trouble ...
import sys
major_vers = sys.version_info[0]
if major_vers == 3:
    import tkinter as tk
    from tkinter import dialog as Dialog
    from tkinter import filedialog as tkFileDialog
    from tkinter import messagebox as tkMessageBox 
    from tkinter import simpledialog as tkSimpleDialog
elif major_vers == 2:
    import Tkinter as tk
    import Dialog 
    import tkFileDialog
    import tkMessageBox 
    import tkSimpleDialog 
    
class SnakeTomato(tk.Frame,object): # object derivation needed to use super in py2
    
    def __init__(self,time_interval = 25, pause_interval = 5, unit = 60,master=None,**options):
        """
        Init method. 
        Args:
          time_interval: Working time interval in minutes
          pause_interval: Pause interval in minutes
          master: tk master
          options: tk options
        """
        super(SnakeTomato,self).__init__(master,options)
        self.unit = unit
        
        self.setIntervals(time_interval,pause_interval)
        self.setGUI()
        #self.initTimer()
    
    def setGUI(self):
        
        self.master.title("Snake Tomato")
        
        self.setStartButton(0,1)
        self.setListBox(0,0)
        self.setIntervalField(1,1)
        self.setPauseField(1,2)
        self.setRemainTimeLabel(2,1)
        self.setPlusButton(3,1)
        self.setMinusButton(4,1)
        self.setLoadButton(3,2)
        self.setWriteButton(4,2)
        self.setEntry(5,0)
        
    def setStartButton(self,row,col):
        
        self.startButton = tk.Button(self.master, text="Start", command=self.startWorkTime)
        self.startButton.grid(row=row,column=col)
        
    def setLoadButton(self,row,col):
        
        self.loadButton = tk.Button(self.master, text="Load", command=self.loadToDoList)
        self.loadButton.grid(row=row,column=col)
        
    def setWriteButton(self,row,col):
        
        self.writeButton = tk.Button(self.master, text="Save", command=self.saveToDoList)
        self.writeButton.grid(row=row,column=col)
        
    def setPlusButton(self,row,col):
        
        self.plusButton = tk.Button(self.master, text="+", command=self.addEntry)
        self.plusButton.grid(row=row,column=col)
        
    def setMinusButton(self,row,col):
        
        self.minusButton = tk.Button(self.master, text="-", command=self.deleteEntry)
        self.minusButton.grid(row=row,column=col)
    
    def setEntry(self,row,col):
        self.entry = tk.Entry(self.master)
        self.entry.grid(row=row,column=col)
    
    def setIntervalField(self,row,col):
        self.interval_field = tk.Entry(self.master,width=3)
        self.interval_field.grid(row=row,column=col)
        self.interval_field.delete(0,tk.END)
        self.interval_field.insert(0,self.time_interval//self.unit)
    
    def setPauseField(self,row,col):
        self.pause_field = tk.Entry(self.master,width=3)
        self.pause_field.grid(row=row,column=col)
        self.pause_field.delete(0,tk.END)
        self.pause_field.insert(0,self.pause_interval//self.unit)
    
    def setRemainTimeLabel(self,row,col):
        self.remain_time_text = tk.StringVar()
        self.remain_time_text.set('00:00')
        self.info_field = tk.Label(self.master,width=20,#font=('times', 20, 'bold'), 
                                          #fg='green',bg='black',
                                          text='Remaining Time: ')
        self.remain_time_field = tk.Label(self.master,width=10,font=('digital-7', 20,), 
                                          fg='green',bg='black',
                                          textvariable=self.remain_time_text)
        self.info_field.grid(row=row,column=col)
        self.remain_time_field.grid(row=row,column=col+1)
    
    def setListBox(self,row,col):
        
        self.listbox = tk.Listbox(self.master)
        self.listbox.grid(row=row,column=col)
    
    def addEntry(self):
        item = self.entry.get()
        if item != "":
            self.listbox.insert(tk.END, item)
        self.entry.delete(0,tk.END)
        
    def deleteEntry(self):
        selection = self.listbox.curselection()
        if selection:
            self.listbox.delete(selection[0])
    
    def writeListInBox(self,fname):
        
        with open(fname,'r') as load:
            lines = load.readlines()
            
        self.listbox.delete(0, tk.END) # clear list
        for line in lines:
            self.listbox.insert(tk.END,line.strip())
    
    def writeListToFile(self,fname):
        
        lines = list(self.listbox.get(0, tk.END))
        lines = [line + '\n' for line in lines]
        
        with open(fname,'w') as save:
            save.writelines(lines)
    
    def loadToDoList(self):
        fname = tkFileDialog.askopenfilename(filetypes=(("Text files", "*.txt"),
                                           ("All files", "*.*") ))
        if fname:
            try:
                self.writeListInBox(fname)
            except:                     # <- naked except is a bad idea
                tkMessageBox.showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return
        
    def saveToDoList(self):
        fname = tkFileDialog.asksaveasfilename(filetypes=(("Text files", "*.txt"),
                                           ("All files", "*.*") ))
        if fname:
            try:
                self.writeListToFile(fname)
            except:                     # <- naked except is a bad idea
                tkMessageBox.showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return
    
    
    def setIntervals(self,time_interval,pause_interval):
        
        self.time_interval = time_interval*self.unit
        self.pause_interval = pause_interval*self.unit
    

    def startWorkTime(self):
        
        self.pause = False
        time_interval = int(self.interval_field.get())
        pause_interval = int(self.pause_field.get())
        self.setIntervals(time_interval,pause_interval)
        self.cdThread = threading.Thread(target=self.countdown,args=(self.time_interval,self.takePause))
        self.cdThread.deamon=True
        self.cdThread.start()
    
    def printTime(self,time):
        mins = time//self.unit
        secs = time%self.unit
        
        strings = ['{0:02d}'.format(t) for t in (mins,secs)]
        
        return ':'.join(strings)
    
    def countdown(self,remain_time,finisher):
        
        for k in range(remain_time+1):
            try:
                self.remain_time_text.set(self.printTime(remain_time-k))
            except RuntimeError: # if main thread dead
                sys.exit()
                
            time.sleep(1)
        
        finisher()
    
    def startPauseTime(self):
        
        self.pause = True
        self.cdThread2 = threading.Thread(target=self.countdown,args=(self.pause_interval,self.backToWork))
        self.cdThread2.deamon=True
        self.cdThread2.start()
        
    
    def setLabel(self):
        self.label = tk.Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)
        
    def takePause(self):
        self.pause = True
        if tkMessageBox.showerror("Pause", "Take a Pause!"):
            self.startPauseTime()
            
    def backToWork(self):
        
        if tkMessageBox.showerror("Working", "Go Back to Work!!"):
            pass
    
    def __del__(self):
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = SnakeTomato(master=root,height=200,width=200)
    app.mainloop()

    
