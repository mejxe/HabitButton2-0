import time

from customtkinter import *
from api_comms import Pixela
import webbrowser

FONT = ("Work Sans", 25, "normal")
GRAY = "#303030"
class Gui(CTkToplevel):
    def __init__(self, quantity, pixela: Pixela):
        super().__init__()
        self.config(background=GRAY,pady=20, padx=20)
        self.geometry("250x450+960+540")
        self.resizable(False,False)
        if pixela.graph_endpoint == "https://pixe.la/v1/users/mejxe/graphs/studygraph":
            self.title(pixela.graph_title[1])
            self.colors = ['#effaef','#c2edc5','#96e09b','#70d577','#44c94d',
                           '#31aa39','#26842c','#1b5e1f','#103813','#103813']
        elif pixela.graph_endpoint == "https://pixe.la/v1/users/mejxe/graphs/mathgraph":
            self.title(pixela.graph_title[2])
            self.colors = ['#daecfe','#a9d3ff','#78bbff','#47a2ff','#168aff',
                           '#006ad5','#0055ab','#003c7a','#002449','#000c18']
        else:
            self.title(pixela.graph_title[0])
            self.colors = ['#f4eaff','#d8b1fe','#bf80ff','#a247ff','#860eff',
                           "#6d00dc",'#5500ab','#3c007a','#240049','#080010']
        self.pixela = pixela
        self.quantity = quantity
        if self.quantity >= 19:
            self.quantity = 19
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # BUTTON
        self.button = CTkButton(self, height=200, width=200, text=f"{self.quantity} Hours.",corner_radius=30, hover=False, bg_color=GRAY, fg_color="white", text_color="black", font=("Work Sans", 25, "normal"))
        self.button.grid(column=0, row=1)

        self.clear_button = CTkButton(self, height=100, width=100, text="X",hover_color="#950101",corner_radius=30, bg_color=GRAY, fg_color="#7D1935", text_color="black", font=FONT, command=self.reset)
        self.clear_button.grid(column=0, row=2, pady=15, padx=20)

        self.yesterday_var = StringVar(value="off")
        self.yesterday_switch = CTkSwitch(self, height=20, width=20, text="Yesterday.", font=("Work Sans", 14, "normal"),
                                          bg_color=GRAY, fg_color="gray",button_color="white", onvalue="on", offvalue='off', border_color="gray",hover=False, progress_color=GRAY, variable=self.yesterday_var)
        self.yesterday_switch.grid(column=0, row=0, pady=15)

        if self.quantity >= 9:
            self.button.configure(text_color="white")
            self.button.configure(fg_color=self.colors[-1],
                                  text=f"{self.quantity} Hours.", text_color="white")
        else:
            self.yesterday_switch.configure(button_color=self.colors[int(self.quantity)])
            self.button.configure(fg_color=self.colors[int(self.quantity)], text=f"{self.quantity} Hours. ")

        self.button.bind("<Button-1>", self.leftbut)
        self.button.bind("<Button-3>", self.rightbut)
        self.return_label = CTkLabel(self, text="", bg_color=GRAY, font=FONT)
        self.return_label.grid(row=4, column=0, rowspan=3)

        self.mainloop()

    def color_change(self):
        self.quantity = self.pixela.quantity_up()
        if self.quantity >= 9:
            self.button.configure(fg_color=self.colors[-1],
                                  text=f"{self.quantity} Hours.", text_color="white")
        else:
            self.yesterday_switch.configure(button_color=self.colors[int(self.quantity)])
            self.button.configure(fg_color=self.colors[int(self.quantity)], text=f"{self.quantity} Hours. ")

    def reset(self):
        self.quantity = 0
        self.pixela.json_clear()
        self.button.configure(fg_color=self.colors[int(self.quantity)],
                              text=f"{self.quantity} Hours.", text_color="black")

    def leftbut(self, event):
        self.color_change()

    def rightbut(self, event):
        webbrowser.open(self.pixela.graph_endpoint)

    def on_close(self):
        self.pixela.create_pixel(self.yesterday_var.get())
        self.pixela.clear_timer()
        self.destroy()

