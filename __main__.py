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


from . import snake_tomato
from.snake_tomato import runApp

if __name__ == "__main__":
    #import sys
    #major_vers = sys.version_info[0]
    #if major_vers == 3:
        #import tkinter as tk
    #elif major_vers == 2:
        #import Tkinter as tk
        
    #root = tk.Tk()
    #app = snake_tomato.SnakeTomato(master=root,height=200,width=200)
    #app.mainloop()
    runApp()
