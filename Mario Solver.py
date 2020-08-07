import tkinter as tk
from arena import *

def clear():
    for ring in range(4):
        for col in range(12):
            arena[ring][col].frame.configure(bg="gray")

def solve():
    enemies = list()
    for ring in range(4):
        for col in range(12):
            enemies.append(arena[ring][col].full())
        myArena.setRing(3-ring,enemies)
        enemies.clear()

    
    myArena.solveArena()

class Space:
    def leftClick(self,event):
        if self.frame['bg'] == "red":
            self.frame.configure(bg="gray")
        else:
            self.frame.configure(bg="red")

    def __init__(self,master):
        self.frame = tk.Frame(master, bg='gray',highlightthickness = 2, highlightbackground = 'black')
        self.frame.bind("<Button-1>", self.leftClick)

    def full(self):
        if self.frame['bg'] == "red":
            return True
        else:
            return False
        

root = tk.Tk()
root.geometry("1200x400")
rows, cols = (4, 12) 
arena = [0]*4
for row in range(4):
    arena[row] = list()

tk.Label(root,text="OuterRow").grid(row=0,column=0)
tk.Label(root,text="MiddleOut").grid(row=1,column=0)
tk.Label(root,text="MiddleIn").grid(row=2,column=0)
tk.Label(root,text="InnerRow").grid(row=3,column=0)
root.columnconfigure(0,weight=1)

for row in range(3,-1,-1):
    for column in range(0,12):        
        tile = Space(root)
        arena[row].append(tile)
        root.rowconfigure(row,weight=1)
        root.columnconfigure(column+1,weight=3)
        tile.frame.grid(row=row, column=column+1,sticky="NSEW")

clearBtn = tk.Button(root, text="Clear Board", command=clear)
solveBtn = tk.Button(root, text="Solve Board", command=solve)

clearBtn.grid(row=4,column=0,columnspan=6)
solveBtn.grid(row=4,column = 7,columnspan=6)


myArena = Arena()


root.mainloop()
