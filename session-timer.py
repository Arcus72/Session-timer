
import tkinter as tk
import tkinter.messagebox
from time import sleep
from winsound import Beep
import pyuac

class Timer():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("420x230")
        self.root.resizable(False,False)
        self.root.title("Time Counter")
        self.root.configure(bg="#292929")

        self.hour=tk.StringVar()
        self.minute=tk.StringVar()
        self.second=tk.StringVar()

        self.hour.set("00")
        self.minute.set("00")
        self.second.set("00")

        self.isOn = False
        self.isPoused = True

        self.listOfFramesFromPhases = []

        self.isWebsitesLocked = False

        self.isYouTubeRestricted = tk.IntVar()
        self.isTwitchRestricted = tk.IntVar()

        tk.Label(self.root,  bg="#292929", fg="white", width=1, text=":", font=("Arial",35,"")).place(x=70,y=18)
        tk.Label(self.root,  bg="#292929", fg="white", width=1, text=":", font=("Arial",35,"")).place(x=145,y=18)

        tk.Entry(self.root, width=2, font=("Arial",35,""), textvariable=self.hour).place(x=20,y=20)
        tk.Entry(self.root, width=2, font=("Arial",35,""),textvariable=self.minute).place(x=95,y=20)
        tk.Entry(self.root, width=2, font=("Arial",35,""), textvariable=self.second).place(x=170,y=20)

        self.youtubeCheckbox = tk.Checkbutton(self.root, bg="#292929" , font=("Arial",12,""), fg="white", selectcolor="black",activebackground="#292929", activeforeground="white", text="YouTube", variable=self.isYouTubeRestricted)
        self.youtubeCheckbox.place(x=80,y=100)

        self.twitchCheckbox = tk.Checkbutton(self.root, bg="#292929" , font=("Arial",12,""), fg="white",selectcolor="black", activebackground="#292929", activeforeground="white", text="Twitch", variable=self.isTwitchRestricted )
        self.twitchCheckbox.place(x=80,y=120)

        self.btn = tk.Button(self.root, width=8, fg="white", text='Start', bg="#0A6EB1", font=("Arial",14,""), bd="0" ,command= self.submit)
        self.btn.place(x = 85,y = 170)

        tk.Frame(self.root, width=4, bg="black", height=200).place(x=250,y=20)

        self.phases = tk.Frame(self.root, width=145,height=180, bg="#292929")
        self.phases.place(x=265,y=20)

        self.root.mainloop()

    def submit(self):
        if self.isPoused == False:
            self.setPlayButton()
            self.isPoused = True
        else:
            self.setPouseButton()
            self.isPoused = False

        if self.isOn == False:
            self.isOn = True
            self.isPoused = False
            self.startCountdown()

    def startCountdown(self):
        try:
            temp = int(self.hour.get())*3600 + int(self.minute.get())*60 + int(self.second.get())
        except:
            tkinter.messagebox.showinfo("Sesstion timer", "Enter the correct numeric value")
            return 1

        threshholdForPhases = temp // 60 * 60

        if self.isYouTubeRestricted.get() == 1 or self.isTwitchRestricted.get() == 1:
            self.isWebsitesLocked = True
            self.lockWebsites()

        self.startSound()
        self.createPhases(temp)
        self.lockCheckbutton()

        while temp != -1:
            if self.isPoused == False:
                if threshholdForPhases == temp:
                    self.reduceMinuteFromPhases()
                    threshholdForPhases -= 60

                min, sec = divmod(temp, 60)
                hour, min = divmod(min, 60)

                self.hour.set("{0:02}".format(hour))
                self.minute.set("{0:02}".format(min))
                self.second.set("{0:02}".format(sec))
                temp -= 1

            self.root.update()
            sleep(1)

        self.isWebsitesLocked == True and self.unlockWebsites()
        self.unlockCheckbutton()
        tkinter.messagebox.showinfo("Time Countdown", "Time's up")


    def reduceMinuteFromPhases(self):
        time = self.listOfFramesFromPhases[0].timeRemain
        time -= 1

        if time == 0:
            if self.listOfFramesFromPhases[0].winfo_children()[1]["text"] == "focus":
                self.breakSound()
            else:
                self.focusSound()
            self.removeCurrentPhase()

            if len(self.listOfFramesFromPhases) != 0:
                self.listOfFramesFromPhases[0].winfo_children()[2].config(bg="#0A6EB1")
        else:
            self.listOfFramesFromPhases[0].winfo_children()[0]["text"] = str(time)+" min"
            self.listOfFramesFromPhases[0].timeRemain = time

    def removeCurrentPhase(self):
        self.listOfFramesFromPhases[0].destroy()
        self.listOfFramesFromPhases.pop(0)

    def lockWebsites(self):
        file = open("C:\Windows\System32\drivers\etc\hosts", "w")
        if self.isYouTubeRestricted.get() == 1:
            file.write("127.0.0.1	www.youtube.com\n")
        if self.isTwitchRestricted.get() == 1:
            file.write("127.0.0.1	www.twitch.tv\n")
        file.close()

    def unlockWebsites(self):
        file = open("C:\Windows\System32\drivers\etc\hosts", "w")
        file.close()

    def startSound(self):
        freq = 500
        for i in range(2):
            Beep(freq, 50)
        freq+= 100

    def focusSound(self):
        freq = 900
        for i in range(4):
            Beep(freq, 50)
            freq+= 100

    def breakSound(self):
        freq = 1000
        for i in range(4):
            Beep(freq, 50)
            freq-= 100

    def lockCheckbutton(self):
        self.youtubeCheckbox.config(state= "disabled")
        self.twitchCheckbox.config(state= "disabled")

    def unlockCheckbutton(self):
        self.youtubeCheckbox.config(state= "normal")
        self.twitchCheckbox.config(state= "normal")

    def setPouseButton(self):
        self.btn.config(text="Pouse")
        self.btn.config(bg="#e67e22")

    def setPlayButton(self):
        self.btn.config(text="Play")
        self.btn.config(bg="#0A6EB1")

    def createPhases(self,temp):
        listOfphases = []
        min, sec = divmod(temp,60)

        while min//35 != 0:
            min -= 35
            listOfphases.append([30,"focus"])
            listOfphases.append([5,"break"])

        if min != 0:
            listOfphases.append([min,"focus"])

        if sec != 0:
            listOfphases[len(listOfphases)-1][0] += 1
        else:
            listOfphases[0][0] += 1

        for i in range(len(listOfphases)):
            self.insertLapse(i ,listOfphases[i][0],listOfphases[i][1])
        self.listOfFramesFromPhases[0].winfo_children()[2].config(bg="#0A6EB1")

    def insertLapse(self,i,time, text):
        self.listOfFramesFromPhases.append(tk.Frame(self.phases, width=145, height=30 ,bg="#292929"))
        self.listOfFramesFromPhases[i].pack()
        self.listOfFramesFromPhases[i].timeRemain = time

        time = str(time)+" min"

        tk.Label(self.listOfFramesFromPhases[i], text=time, bg="#292929", fg="white", font=("Arial",16,"")).place(x=0,y=0)
        tk.Label(self.listOfFramesFromPhases[i], text=text,bg="#292929", fg="white", font=("Arial",16,"")).place(x=80,y=0)
        tk.Frame(self.listOfFramesFromPhases[i], bg="#3A3A3A", width=145, height=5).place(x=0,y=25)


if not pyuac.isUserAdmin():
    pyuac.runAsAdmin()
else:
    Timer()
