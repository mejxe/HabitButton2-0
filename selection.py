from datetime import *
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
# get the streaks with try/except as a safe measure
with open("streaks.json","r") as file:
    if not not file.read():
        file.seek(0)
        strks = json.load(file)
        try:
            STUDY_STREAK = strks["study"][datetime.strftime(date.today(), "%Y%m%d")]
        except KeyError:
            STUDY_STREAK = 0
        try:
            MATH_STREAK = strks["math"][datetime.strftime(date.today(), "%Y%m%d")]
        except KeyError:
            MATH_STREAK = 0
        try:
            CODE_STREAK = strks["code"][datetime.strftime(date.today(), "%Y%m%d")]
        except KeyError:
            CODE_STREAK = 0

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
        self.study.place(x=5, y=20)

        self.study_streak = CTkLabel(self.root, text=f"🔥 {STUDY_STREAK}", font=(FONT), bg_color=GRAY)
        self.study_streak.place(x=5, y=-10)


        self.code = CTkButton(self.root, width=50, height=25, text="Code", font=FONT, bg_color=GRAY,
                               fg_color="#3c007a",  hover_color = '#2A0944', corner_radius=10)
        self.code.place(x=80, y=20)

        self.code_streak = CTkLabel(self.root, text=f"🔥 {CODE_STREAK}", font=(FONT), bg_color=GRAY)
        self.code_streak.place(x=80, y=-10)


        self.math = CTkButton(self.root, width=50, height=25, text="Math", font=FONT, bg_color=GRAY,
                               fg_color="#0055ab",  hover_color="dark blue", corner_radius=10)
        self.math.place(x=150, y=20)
        self.math_streak = CTkLabel(self.root, text=f"🔥 {MATH_STREAK}", font=(FONT), bg_color=GRAY)
        self.math_streak.place(x=150, y=-10)

        self.auto = CTkButton(self.root, command=self.open_timer, width=20, height=20, text="Timer", font=FONT, bg_color=GRAY,
                               fg_color="#7D1935", hover_color="#480e1f", corner_radius=10)
        self.auto.place(x=78, y=60)

        self.study.bind("<Button-1>", lambda *args: self.go_to('study'))

        self.code.bind("<Button-1>", lambda *args: self.connect_endpoint('code'))
        self.code.bind("<Button-3>", lambda *args: self.go_to('code'))

        self.math.bind("<Button-1>", lambda *args: self.connect_endpoint('math'))
        self.math.bind("<Button-3>", lambda *args: self.go_to('math'))


        self.root.mainloop()

    def connect_endpoint(self, endpoint):
        with open("timer_commits.json", "r") as loaddata:
            data = json.load(loaddata)
        pixela = Pixela(graph_endpoints[endpoint], graph_name=endpoint, auto_commits=data[endpoint])
        quantity = pixela.get_pixel_attributes()
        self.open_button_gui(quantity=quantity, pixela=pixela)

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
                self.timer_commits_upload(graph_name="math", data=data)
                self.timer_commits_upload(graph_name="code", data=data)


    def timer_commits_upload(self, graph_name, data ):
        if int(data[graph_name]) != 0:
            coms = Pixela(graph_endpoints[graph_name], graph_name, data[graph_name])
            coms.get_pixel_attributes()
            coms.create_pixel(yesterday="off")
            coms.clear_timer()
            del coms