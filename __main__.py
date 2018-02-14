from . import snake_tomato

if __name__ == "__main__":
    import sys
    major_vers = sys.version_info[0]
    if major_vers == 3:
        import tkinter as tk
    elif major_vers == 2:
        import Tkinter as tk
        
    root = tk.Tk()
    app = snake_tomato.SnakeTomato(master=root,height=200,width=200)
    app.mainloop()
