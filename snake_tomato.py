#!/bin/python
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
import sys
import os

# version trouble ...
major_vers = sys.version_info[0]
if major_vers == 3:
    import tkinter as tk
    from tkinter import dialog as Dialog
    from tkinter import filedialog as tkFileDialog
    from tkinter import messagebox as tkMessageBox 
    from tkinter import simpledialog as tkSimpleDialog
    
    import configparser
    cp_write_mode = 'w'
    from io import open
    
if major_vers == 2:
    import Tkinter as tk
    import Dialog 
    import tkFileDialog
    import tkMessageBox 
    import tkSimpleDialog
    
    import ConfigParser as configparser
    cp_write_mode = 'wb'
    from codecs import open
    
def getScriptDir():
        return os.path.dirname(os.path.realpath(__file__)) + os.sep
    
class SnakeTomato(tk.Frame,object): # object derivation needed to use super in py2
    
    def __init__(self,config_file_name,time_interval = 2, pause_interval = 1, unit = 1,
                 scratch_name = 'scratch',file_format='.txt',master=None,**options):
        """
        Init method. 
        Args:
          time_interval: Working time interval in minutes
          pause_interval: Pause interval in minutes
          master: tk master
          options: tk options
        """
        super(SnakeTomato,self).__init__(master,options)
        
        # set default states
        self.setStates()
        # Set config file
        self.getConfig(config_file_name)
        self.setIntervals(self.work_time_in_units,self.pause_time_in_units)
        
        # Make x Button use inside method
        self.master.protocol("WM_DELETE_WINDOW", self.closeApp)
        
        self.setGUI()
        self.getScratch(self.scratch_file)
        
        
    def setStates(self):
        self.start_pressed = False
        self.reset_pressed = False
    
    def getScratch(self,fname):
        
        if os.path.isfile(fname):
            self.writeListInBox(fname)
        else:
            with open(fname,'w',encoding='utf8'):
                pass
    
    def setGUI(self):
        
        self.master.title("Snake Tomato")
        self.setupMenu()
        
        self.list_box_pos = (6,3)
        
        self.setStartButton(11,0)
        self.setResetButton(11,1)
        self.setIntervalField(9,0)
        self.setPauseField(9,1)
        self.setRemainTimeLabel(7,0)
        self.setPlusButton(5,0)
        self.setMinusButton(5,1)
        #self.setLoadButton(3,2)
        self.setEntry(5,3)
        self.setListBox(*self.list_box_pos)
        self.setCloseButton(11,4)
        self.setWriteButton(11,3)
        self.fillEntries()
    
    def fillEntries(self):
        
        if self.start_pressed:
            self.resetTimer()
        
        self.interval_field.delete(0,tk.END)
        self.interval_field.insert(0,self.time_interval//self.unit)
        self.pause_field.delete(0,tk.END)
        self.pause_field.insert(0,self.pause_interval//self.unit)
        
    def setupMenu(self):
        menubar = tk.Menu(self.master)
        
        mainmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=mainmenu)
        
        mainmenu.add_command(label="Preferences", command=self.openPreferencesWindow)
        mainmenu.add_command(label="Quit", command=self.closeApp)
        
        self.master.config(menu=menubar)
        
    def setStartButton(self,row,col):
        
        self.startButton = tk.Button(self.master, text="Start", command=self.startWorkTime)
        self.startButton.grid(row=row,column=col)
        
    def setResetButton(self,row,col):
        
        self.startButton = tk.Button(self.master, text="Reset", command=self.resetTimer)
        self.startButton.grid(row=row,column=col)
        
    def setLoadButton(self,row,col):
        
        self.loadButton = tk.Button(self.master, text="Load", command=self.loadToDoList)
        self.loadButton.grid(row=row,column=col)
        
    def setWriteButton(self,row,col):
        
        self.writeButton = tk.Button(self.master, text="Save", command=self.saveToDoList)
        self.writeButton.grid(row=row,column=col)
    
    def setCloseButton(self,row,col):
        self.closeButton = tk.Button(self.master, text="Close", command=self.closeApp)
        self.closeButton.grid(row=row,column=col)
    
    def setPlusButton(self,row,col):
        
        self.plusButton = tk.Button(self.master, text="+", command=self.addEntry,width=6)
        self.plusButton.grid(row=row,column=col)
        
    def setMinusButton(self,row,col):
        
        self.minusButton = tk.Button(self.master, text="-", command=self.deleteEntry,width=6)
        self.minusButton.grid(row=row,column=col)
    
    def setEntry(self,row,col):
        self.entry = tk.Entry(self.master)
        self.entry.grid(row=row,column=col,columnspan=2, rowspan=1)
    
    def setIntervalField(self,row,col):
        self.interval_label = tk.Label(self.master,text='Work Time: ')
        self.interval_field = tk.Entry(self.master,width=3)
        self.interval_label.grid(row=row,column=col)
        self.interval_field.grid(row=row+1,column=col)
        
    def setPauseField(self,row,col):
        self.pause_label = tk.Label(self.master,text='Pause Time:')
        self.pause_field = tk.Entry(self.master,width=3)
        self.pause_label.grid(row=row,column=col)
        self.pause_field.grid(row=row+1,column=col)
    
    def setRemainTimeLabel(self,row,col):
        self.remain_time_text = tk.StringVar()
        self.remain_time_text.set('00:00')
        self.info_field = tk.Label(self.master,width=20,#font=('times', 20, 'bold'), 
                                          #fg='green',bg='black',
                                          text='Remaining Time: ')
        self.remain_time_field = tk.Label(self.master,width=10,font=('digital-7', 20,), 
                                          fg='green',bg='black',
                                          textvariable=self.remain_time_text)
        self.info_field.grid(row=row,column=col,columnspan=3)
        self.remain_time_field.grid(row=row+1,column=col,columnspan=3)
    
    def setListBox(self,row,col):
            
        self.listbox = tk.Listbox(self.master,height=self.nr_of_entries)
        self.listbox.grid(row=row,column=col,columnspan=2, rowspan=5)
    
    def openPreferencesWindow(self):
        self.top_window = tk.Toplevel(self.master)
        self.top_window.wm_title('Preferences')
        
        row = 0
        self.top_window.section_labels = dict([])
        self.top_window.labels = dict([])
        self.top_window.entries = dict([])
        
        for section in self.config_dict.keys():
            sec_label = tk.Label(self.top_window,text=section.replace('_',' '),font=('arial', 20,))
            sec_label.grid(row=row,column=1)
            row += 1
            self.top_window.section_labels.update({section:sec_label})
            
            sub_dict = self.config_dict[section]
            label_dict = dict([])
            entry_dict = dict([])
            for key in sub_dict.keys():
                label = tk.Label(self.top_window,text=key.replace('_',' '))
                label.grid(row=row,column=0)
                entry = tk.Entry(self.top_window,width = 50)
                entry.grid(row=row,column=1,columnspan=2)
                entry.insert(0,sub_dict[key][1])
                
                label_dict.update({key:label})
                entry_dict.update({key:entry})
                
                row += 1
                
            self.top_window.labels.update({section:label_dict})    
            self.top_window.entries.update({section:entry_dict})
                
        self.top_window.set_button = tk.Button(self.top_window,text='Set Config',command=self.setPreferences)
        self.top_window.set_button.grid(row=row,column=4)
        
        # has to be placed here ...
        # Reason: It seems that data isn't updated properly across windows
        self.writeListToFile(self.scratch_file) 
    
    def setNrOfEntries(self,nr_of_entries):
        self.nr_of_entries = nr_of_entries
        self.config_dict["defaults"]["nr_of_entries"] = [int,str(self.nr_of_entries)]
    
    def setPreferences(self):
        
        # has to be stored if entries do not work out
        nr_of_entries_buffer = self.nr_of_entries
        
        for section in self.config_dict.keys():
            sub_dict = self.config_dict[section]
            for key in sub_dict.keys():
                cur_entry = self.config_dict[section][key]
                cur_val = cur_entry[0](self.top_window.entries[section][key].get())
                self.config_dict[section][key][1] = cur_val
                self.__dict__.update({key:cur_val})
        
        self.writeConfig()
        self.readConfig()
        self.setIntervals(self.work_time_in_units,self.pause_time_in_units)
        self.getScratch(self.scratch_file)
        
        # Set listbox
        if self.tooMuchEntries(self.nr_of_entries):
            self.setNrOfEntries(nr_of_entries_buffer)
            tkMessageBox.showerror("Too Much Entries!", "Either delete items or set the nr of entries setting higher!\nCurrent setting is set to old value!")
            
        self.refreshListBox()
        
        self.top_window.destroy()
    
    def refreshListBox(self):
        
        self.listbox.destroy()
        self.setListBox(*self.list_box_pos)
        self.writeListInBox(self.scratch_file)
        
    def closeApp(self):
        
        self.writeListToFile(self.scratch_file)
        self.writeConfig()
        self.master.quit()
    
    def tooMuchEntries(self,nr_of_entries):
        
         lines = list(self.listbox.get(0, tk.END))
         if len(lines) > nr_of_entries:
             return True
         
         return False
    
    def addEntry(self):
        
        if self.tooMuchEntries(self.nr_of_entries):
            tkMessageBox.showerror("Too Much Entries!", "Either delete items or set the nr of entries setting higher!")
        else:
            item = self.entry.get()
            if item != "":
                self.listbox.insert(tk.END, item)
                self.listbox.update()
                
            self.entry.delete(0,tk.END)
        
    def deleteEntry(self):
        
        selection = self.listbox.curselection()
        if selection:
            self.listbox.delete(selection[0])
    
    def writeListInBox(self,fname):
        
        with open(fname,'r',encoding='utf8') as load:
            lines = load.readlines()
        
        if len(lines) > self.nr_of_entries:
            self.setNrOfEntries(len(lines))
            tkMessageBox.showerror("Too Much Entries!", "Nr of entries is set higher now!")
            self.listbox.destroy()
            self.setListBox(*self.list_box_pos)
        
        self.listbox.delete(0, tk.END) # clear list
        for line in lines:
            self.listbox.insert(tk.END,line.strip())
    
    def writeListToFile(self,fname):
        
        lines = list(self.listbox.get(0, tk.END))
        lines = [line + '\n' for line in lines]
        
        with open(fname,'w',encoding='utf8') as save:
            save.writelines(lines)
    
    def loadToDoList(self):
        
        fname = tkFileDialog.askopenfilename(filetypes=(("Text files", "*"+self.file_format),
                                           ("All files", "*.*") ))
        if fname:
            try:
                self.writeListInBox(fname)
            except:                     # <- naked except is a bad idea
                tkMessageBox.showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return
        
    def saveToDoList(self):
        
        #fname = tkFileDialog.asksaveasfilename(filetypes=(("Text files", "*"+self.file_format),
                                           #("All files", "*.*") ))
        fname = self.scratch_file
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
        
        if not self.start_pressed:
            
            self.start_pressed = True
            time_interval = int(self.interval_field.get())
            pause_interval = int(self.pause_field.get())
            self.setIntervals(time_interval,pause_interval)

            self.cdThread = threading.Thread(target=self.countdown,args=(self.time_interval,))
            #self.cdThread.deamon=True
            self.cdThread.start()
            self.message_id = self.master.after(self.time_interval*1000,self.takePause)
        
    def printTime(self,time):
        mins = time//self.unit
        secs = time%self.unit
        
        strings = ['{0:02d}'.format(t) for t in (mins,secs)]
        
        return ':'.join(strings)
    
    def countdown(self,remain_time):
        
        for k in range(remain_time+1):
            try:
                self.remain_time_text.set(self.printTime(remain_time-k))
                time.sleep(1)
                if self.reset_pressed: 
                    break
                
            except RuntimeError: # if main thread dead
                sys.exit()
                
        if self.reset_pressed:
            self.reset_pressed = False
            self.remain_time_text.set(self.printTime(0))
    
    def startPauseTime(self):
        
        self.switch_pause = False
        self.cdThread2 = threading.Thread(target=self.countdown,args=(self.pause_interval,))
        self.cdThread2.deamon=True
        self.cdThread2.start()
        self.message_id = self.master.after(self.pause_interval*1000,self.backToWork)
        self.start_pressed = False
        
    def setLabel(self):
        
        self.label = tk.Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)
        
    def takePause(self):
        
        self.pause = True
        if tkMessageBox.showwarning("Pause", "Take a Pause!"):
            self.startPauseTime()
            
    def backToWork(self):
        
        if tkMessageBox.showwarning("Working", "Go Back to Work!!"):
            pass

    def resetTimer(self):
        
        self.reset_pressed = True
        self.start_pressed = False
        
        self.master.after_cancel(self.message_id)
    
    def getConfig(self,config_file):
        
        self.config_file = config_file
        self.defineConfigEntries()
        
        if not os.path.isfile(self.config_file):
            self.writeConfig()
            
        self.readConfig()
    
    def defineConfigEntries(self):
        
        # config dict contains sections and entries with dtypes 
        # and a predefined default value
        ftype = 'txt'
        fname = getScriptDir() + 'scratch' + '.' + ftype
        
        default_unit = 60
        default_work_time = 25
        default_pause_time = 5
        nr_of_entries = 20
        
        self.config_dict = {'scratch':{'file_format':[str,ftype],'scratch_file':[str,fname]},
                            'defaults':{'unit':[int,default_unit],
                                        'work_time_in_units':[int,default_work_time],
                                         'pause_time_in_units':[int,default_pause_time],
                                         'nr_of_entries':[int,nr_of_entries],
                                         }
                            }
    
    def readConfig(self):
        
        config = configparser.RawConfigParser()
        config.read(self.config_file)
        
        for section in self.config_dict.keys():
            sub_dict = self.config_dict[section]
            for key in sub_dict.keys():
                current_val = sub_dict[key][0](config.get(section,key))
                help_dict = {key:current_val}
                self.__dict__.update(help_dict)
                self.config_dict[section][key][1] = current_val 
            
    def writeConfig(self):
        
        config = configparser.RawConfigParser()
        for section in self.config_dict.keys():
            config.add_section(section)

            sub_dict = self.config_dict[section]
            for key in sub_dict.keys():
                config.set(section,key,sub_dict[key][-1])
        
        with open(self.config_file, cp_write_mode,encoding='utf8') as configfile:
            config.write(configfile)
        

def runApp():
    config_file_name = getScriptDir() + 'snake_tomato.cfg'
    root = tk.Tk()
    app = SnakeTomato(config_file_name,master=root,height=200,width=200)
    app.mainloop()


if __name__ == "__main__":
    runApp()

    
