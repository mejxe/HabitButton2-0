from customtkinter import *
import random
import string
import json
import CTkMessagebox
import time

FONT = ("Work Sans Light", 40, "normal")
BFONT = ("Work Sans", 15, "normal")
CFONT = ("Work Sans", 17, "normal")
GRAY = "#303030"
token = "".join(random.choices(string.ascii_letters+string.digits, k=7))
class GraphCreator():
    def __init__(self):
        self.root = CTk()
        self.root.title("Graph Creator")
        self.root.geometry("600x450")
        self.root.configure(fg_color=GRAY)
        self.root.resizable(False,False)

        self.frame = CTkFrame(self.root, width=550, height=400, bg_color='#464646', fg_color="#464646")
        self.frame.pack(pady=20)
        self.register_label = CTkLabel(self.frame, text="Create an User Profile", font=FONT)
        self.register_label.place(x=10, y=5)
        self.username = CTkEntry(self.frame)
        self.username.place(x=10, y=80)
        self.username_label = CTkLabel(self.frame, text="Username (min. 6 characters and no specials)", font=BFONT)
        self.username_label.place(x=160,y=80)
        self.terms = CTkLabel(self.frame, text="Do you accept TOS?", font=BFONT)
        self.terms.place(x=10, y=120)
        self.terms_var = IntVar()
        self.terms_yes = CTkRadioButton(self.frame, text="Yes", variable=self.terms_var, value=1)
        self.terms_no = CTkRadioButton(self.frame, text="No", variable=self.terms_var, value=0)
        self.terms_yes.place(x=30, y=160)
        self.terms_no.place(x=100, y=160)
        self.minor_var = IntVar()
        self.minor = CTkLabel(self.frame, text="Are you above 16 y/o?", font=BFONT)
        self.minor.place(x=10, y=220)
        self.minor_yes = CTkRadioButton(self.frame, text="Yes", variable=self.minor_var, value=1)
        self.minor_no = CTkRadioButton(self.frame, text="No", variable=self.minor_var, value=0)
        self.minor_yes.place(x=30, y=260)
        self.minor_no.place(x=100, y=260)
        self.create = CTkButton(self.frame, text="Create User", command=self.create_user)
        self.create.place(x=30, y=320)
        self.root.mainloop()


    def create_user(self):
        if len(self.username.get()) > 5:
            data_dict = {"Username:":self.username.get(),
                         "Token":token}
            with open("user_data.json", "w") as userdata:
                json.dump(data_dict, userdata, indent=4)
                CTkMessagebox.CTkMessagebox(self.root, title="Success", icon="check", message="User created, rerun the app.")
                self.root.after(3000, exit)
        else:
            CTkMessagebox.CTkMessagebox(self.root, title="Error", icon="cancel", message="Username Too Short")




