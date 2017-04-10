import Tkinter

class MyApp(Tkinter.Frame):
    def say_hi(self):
        print "Hello, World"

    def createWidgets(self):
        self.QUIT = Tkinter.Button(self)
        self.QUIT["text"] = "Quit"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.hi_there = Tkinter.Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack(side="right")

    def createButtons(self):
        self.buttonHelloWorld = Tkinter.Button(self)
        self.buttonHelloWorld["text"] = "Hello"
        self.buttonHelloWorld["bg"] = "green"
        self.buttonHelloWorld["command"] = self.say_hi
        self.buttonHelloWorld.pack()



    def __init__(self, master=None):
        Tkinter.Frame.__init__(self, master)
        self.pack()
        #self.createWidgets()
        self.createButtons()


root = Tkinter.Tk()
app = MyApp(master=root)
app.mainloop()
root.destroy()
