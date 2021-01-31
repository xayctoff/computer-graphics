from source.main.constants import HEIGHT
from source.main.constants import PANEL_WIDTH
from source.main.constants import TITLE
from source.main.constants import WIDTH
from source.main.model.body import Body
from tkinter import *

def main():
    body = Body()
    root = Tk()
    root.geometry(str(WIDTH + PANEL_WIDTH) + "x" + str(HEIGHT))
    root.title(TITLE)
    root.resizable(width=False, height=False)
    root.mainloop()

if __name__ == "__main__":
    main()
