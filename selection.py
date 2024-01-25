import json

from customtkinter import *
import webbrowser
from timer import Timer
from api_comms import Pixela
from gui import Gui

GRAY = "#303030"
FONT = ("Work Sans", 15, "normal")
graph_endpoints = {"study": "https://pixe.la/v1/users/mejxe/graphs/studygraph",
                   "math": "https://pixe.la/v1/users/mejxe/graphs/mathgraph",
                   "code": "https://pixe.la/v1/users/mejxe/graphs/codegraph"}


class Select:
    def __init__(self):
        self.root = CTk()
        self.root.config(background=GRAY, pady=20, padx=20)
        self.root.geometry("260x130+960+540")
        self.root.resizable(False, False)
        self.root.title("Select")
        self.auto_commits = 0
        set_appearance_mode("dark")
        set_default_color_theme("blue")


        self.study = CTkButton(self.root, width=50, height=25, text="Study", font=FONT, bg_color=GRAY,
                               fg_color="#26842c", hover_color="dark green", corner_radius=10, state="disabled")
        self.study.grid(column=1, row=1, padx=5, pady=5)


        self.code = CTkButton(self.root, width=50, height=25, text="Code", font=FONT, bg_color=GRAY,
                               fg_color="#3c007a", command=lambda *args: self.connect_endpoint('code'), hover_color = '#2A0944', corner_radius=10)
        self.code.grid(column=2, row=1, padx=5, pady=5)


        self.math = CTkButton(self.root, width=50, height=25, text="Math", font=FONT, bg_color=GRAY,
                               fg_color="#0055ab", command=lambda *args: self.connect_endpoint('math'), hover_color="dark blue", corner_radius=10)
        self.math.grid(column=3, row=1, padx=5, pady=10)

        self.auto = CTkButton(self.root, command=self.open_timer, width=20, height=20, text="Timer", font=FONT, bg_color=GRAY,
                               fg_color="#7D1935", hover_color="#480e1f", corner_radius=10)
        self.auto.grid(column=2, row=2, columnspan=1)

        self.study.bind("<Button-1>", lambda *args: self.go_to('study'))

        self.code.bind("<Button-1>", lambda *args: self.connect_endpoint('code', 'code'))
        self.code.bind("<Button-3>", lambda *args: self.go_to('code'))

        self.math.bind("<Button-1>", lambda *args: self.connect_endpoint('math', 'math'))
        self.math.bind("<Button-3>", lambda *args: self.go_to('math'))


        self.root.mainloop()

    def connect_endpoint(self, endpoint):
        with open("timer_commits.json", "r") as loaddata:
            data = json.load(loaddata)
        pixela = Pixela(graph_endpoints[endpoint], graph_name=endpoint, auto_commits=data[endpoint])
        quantity = pixela.get_pixel_attributes()
        self.open_button_gui(quantity=quantity, pixela=pixela)
        return pixela

    def open_button_gui(self, quantity, pixela):
        gui = Gui(int(quantity), pixela)


    def go_to(self, web):
        endpoints= {"study": "https://pixe.la/v1/users/mejxe/graphs/studygraph.html",
                    "math": "https://pixe.la/v1/users/mejxe/graphs/mathgraph.html",
                    "code": "https://pixe.la/v1/users/mejxe/graphs/codegraph.html"}
        webbrowser.open(endpoints[web])

    # POMODORO
    def open_timer(self):
        self.timer = Timer(graph_endpoints.keys(), self.root)
        if not self.timer.winfo_exists():
            with open("timer_commits.json", "r") as dataload:
                data = json.load(dataload)
                if int(data["math"]) != 0:
                    with open("timer_commits.json", "r") as loaddata:
                        data = json.load(loaddata)
                    s = Pixela(graph_endpoints["math"], graph_name="math", auto_commits=data["math"])
                    quantity = s.get_pixel_attributes()
                    gui = Gui(int(s.quantity), pixela=s)

                if int(data["code"]) != 0:
                    with open("timer_commits.json", "r") as loaddata:
                        data = json.load(loaddata)
                    s2 = Pixela(graph_endpoints["code"], graph_name="code", auto_commits=data["code"])
                    quantity = s2.get_pixel_attributes()
                    gui2 = Gui(int(s2.quantity), pixela=s2)
