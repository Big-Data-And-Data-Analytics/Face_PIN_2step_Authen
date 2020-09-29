import tkinter as tk
import cv2
from PIL import ImageTk,Image
LARGE_FONT = ("Courier", 24)
from threading import Thread

import validateUserCredentials
obj_validate = validateUserCredentials.UserCredentialsCls()

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self,width=640,height=500)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_propagate(0)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo,PageTransaction):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent,bg = "#adffde")

        def exit_button():
            self.quitAll()

        label = tk.Label(self, text="Two-Factor Authentication\nATM System", font=LARGE_FONT,fg="#c90251",bg="#adffde")
        label.pack(pady=20, padx=10)

        button = tk.Button(self, text="Create New User",borderwidth=1,font = ("Courier",20), command=lambda: controller.show_frame(PageOne))
        button.configure(background = "#9ee9f7")
        button.pack(pady=20, padx=10)

        button2 = tk.Button(self, text="Existing User",font=("Courier",20), command=lambda: controller.show_frame(PageTwo))
        button2.configure(background = "#9ee9f7")
        button2.pack(pady=20, padx=10)

        button_qwer = tk.Button(self, text="Close", font=("Courier", 15), background="#f78f8f", command=self.quit)
        button_qwer.pack(padx = 10, pady = 20)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        ment = tk.StringVar()
        strPIN = tk.StringVar()  # added by Anurag

        def get_name():
            mtext = ment.get()
            pin = strPIN.get()  # added by anurag
            dict_userCredential = dict()  # create empty dictionary to store user credential

            import capture_face

            if mtext and mtext.strip():

                if pin and pin.strip():

                    isExist = obj_validate.checkUsernameExists(key_username=mtext)

                    if isExist.lower() == "exist":
                        label.configure(text="Username Exist")
                    else:
                        dict_userCredential[mtext] = pin

                        #isSaved = obj_validate.saveUserCredentials(dict_userCredential)
                        t1 = ThreadWithReturnValue(target=obj_validate.saveUserCredentials, args=(dict_userCredential,))

                        #capture_face.start_capture(mtext)
                        t2 = ThreadWithReturnValue(target=capture_face.start_capture, args=(mtext,))

                        t1.start()
                        t2.start()

                        isSaved = t1.join()
                        t2.join()

                        if isSaved.lower()=="done":
                            label.configure(text = "User Created")
                            entry.delete(0, tk.END)  # clear the entry box
                            txtbox_PIN.delete(0, tk.END)
                        else:
                            label.configure(text="User not created")
                else:
                    label.configure(text="PIN Empty")
            else:
                label.configure(text="User Name Empty")

        tk.Frame.__init__(self, parent,bg = "#adffde")
        label = tk.Label(self, text="Create New User", font=LARGE_FONT,fg="#c90251",bg="#adffde")
        label.pack(pady=20, padx=10)

        button1 = tk.Button(self, text="Back to Home",borderwidth=1,font = ("Courier",20), command=lambda: controller.show_frame(StartPage))
        button1.configure(background="#9ee9f7")
        button1.pack(pady=20, padx=10)

        text_label = tk.Label(self, text="Enter User Name", font=LARGE_FONT,fg="#048260",bg="#adffde",bd=-2).pack()
        entry = tk.Entry(self, textvariable=ment, bg = "#56f0cc")
        entry.pack(ipady = 5, ipadx = 5)

        # start- added by Anurag
        lbl_PIN = tk.Label(self, text="Enter PIN", font=LARGE_FONT,fg="#048260",bg="#adffde",bd=-2)
        lbl_PIN.pack(pady=10, padx=10)
        txtbox_PIN = tk.Entry(self, textvariable=strPIN, bg = "#56f0cc")
        txtbox_PIN.pack(ipady = 5, ipadx = 5)
        # end - added by Anurag

        mNameButton = tk.Button(self, text="Save Login Details", borderwidth=1, font=("Courier", 20),background="#9ee9f7", command=get_name)
        mNameButton.pack(pady=20, padx=10)

        button_qwer = tk.Button(self, text="Close", font=("Courier", 15), background="#f78f8f", command=self.quit)
        button_qwer.place(relx=0.5, anchor=tk.CENTER)
        button_qwer.pack(padx = 10, pady = 20)

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):

        # start - added by Anurag
        username = tk.StringVar()
        pin = tk.StringVar()
        # end - added by Anurag

        def authentication():
            str_username = username.get()
            str_pin = pin.get()  # added by anurag

            #isExist = obj_validate.checkUsernameExists(key_username=str_username, key_pin=str_pin)
            t1 = ThreadWithReturnValue(target=obj_validate.checkUsernameExists, kwargs={'key_username':str_username, 'key_pin':str_pin})

            import authenticate
            #pic_name = authenticate.authen()
            t2 = ThreadWithReturnValue(target=authenticate.authen)  # pass function name without brackets

            t1.start()
            t2.start()

            isExist = t1.join()
            pic_name = t2.join()

            if isExist.lower() == "exist":
                if pic_name and pic_name.strip():
                    if pic_name == str_username:
                        label.configure(text = "Welcome "+str(pic_name))
                        button2.configure(text="Proceed to Transactions", command=lambda: controller.show_frame(PageTransaction))

                        lbl_username.pack_forget()  # hides the widget
                        txtbox_username.pack_forget()
                        lbl_pin.pack_forget()
                        txtbox_pin.pack_forget()
                    else:
                        label.configure(text="Username and Face not match")
                else:
                    label.configure(text="Face Not Match")
            else:
                label.configure(text="Incorrect Username or PIN")

        tk.Frame.__init__(self, parent,bg = "#adffde")

        label = tk.Label(self, text="Enter Username & PIN to login", font=LARGE_FONT,fg="#c90251",bg="#adffde")
        label.pack(pady=20, padx=10)

        button1 = tk.Button(self, text="Back to Home",font = ("Courier",15),background="#9ee9f7", command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=20, padx=10)

        # start - added by Anurag
        lbl_username = tk.Label(self, text="User Name", font=LARGE_FONT, fg="#048260", bg="#adffde", bd=-2)
        lbl_username.pack()
        txtbox_username = tk.Entry(self, textvariable=username, bg="#56f0cc")
        txtbox_username.pack(ipady = 5, ipadx = 5)

        lbl_pin = tk.Label(self, text="PIN", font=LARGE_FONT, fg="#048260", bg="#adffde", bd=-2)
        lbl_pin.pack()
        txtbox_pin = tk.Entry(self, textvariable=pin, bg="#56f0cc")
        txtbox_pin.pack(ipady = 5, ipadx = 5)
        # end - added by Anurag

        button2 = tk.Button(self, text="Login",font = ("Courier",15),background="#9ee9f7", command=authentication)
        button2.pack(pady=20, padx=10)

        button_qwer = tk.Button(self, text="Close", font = ("Courier",15),background="#f78f8f", command=self.quit)
        button_qwer.place(relx=0.5, anchor=tk.CENTER)
        button_qwer.pack(pady=20, padx=10)


class PageTransaction(tk.Frame):

    def __init__(self, parent, controller):
        ment = tk.StringVar()
        import random
        self.number = random.randint(1000, 1000000)
        def withdraw():
            if self.number>=int(ment.get()):
                self.number = self.number-int(ment.get())
                label_balance.configure(text="Transaction Succesful. \nBalance: " +str(self.number))
                entry.delete(0, tk.END)  # clear the entry box
            else:
                label_balance.configure(text="Insuffecient Balance")

        tk.Frame.__init__(self, parent,bg = "#adffde")

        label = tk.Label(self, text="Account Summary", font=LARGE_FONT,fg="#c90251",bg="#adffde")
        label.pack(pady=20, padx=10)

        label_balance = tk.Label(self, text="Current Balance:" + str(self.number), font=LARGE_FONT, fg="#048260", bg="#adffde")
        label_balance.pack(pady=20, padx=10)

        button1 = tk.Button(self, text="Withdraw Amount", font=("Courier", 15), background="#9ee9f7", command=lambda: withdraw())
        button1.pack()
        entry = tk.Entry(self, textvariable=ment, bg="#56f0cc")
        entry.pack(ipady=5, pady=5)

        button_qwer = tk.Button(self, text="Close", font=("Courier", 15), background="#f78f8f", command=self.quit)
        button_qwer.place(relx=0.5, anchor=tk.CENTER)
        button_qwer.pack(padx=10, pady=20)

# below class is used to get value returned from Thread function
class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

app = SeaofBTCapp()
app.resizable(0,0)
app.mainloop()