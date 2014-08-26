
__author__ = 'marcodiv'


import Tkinter as T
from numpy.matlib import *
from matplotlib.pyplot import *


def click():
    ss = testo.get()
    if len(ss)<20 :
        try:
            minimo=float(mini.get())
            massimo=float(maxi.get())
            x = arange(minimo, massimo, 0.1)
            strr="plot(x," + ss + ")"
            eval(strr)
            show()
        except SyntaxError:
            testo.delete(0, T.END)
            testo.insert(0, "comando scritto male")
        except NameError:
            testo.delete(0, T.END)
            testo.insert(0, "comando non riconosciuto")
        except ValueError:
            testo.delete(0, T.END)
            testo.insert(0, "Indici non riconosciuti")


root = T.Tk()
root.title('Simple Pythonic Grapher')
l=T.Label(root, text='Plot:')
l.pack(side=T.LEFT)
testo = T.Entry(root, width=30)
testo.pack(side="left")
MyButton = T.Button(root, text='Esegui')
MyButton['background']="#FFFFFF"
MyButton['foreground']="red"
MyButton['command']=click

lm=T.Label(root, text='From:')
lmax=T.Label(root, text='To:')
mini=T.Entry(root, width=15)
maxi=T.Entry(root, width=15)
lm.pack(side="left")
mini.pack(side="left")
lmax.pack(side="left")
maxi.pack(side="left")

MyButton.pack({"side": "left", "padx": 20, "pady": 20})


root.mainloop()