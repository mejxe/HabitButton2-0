from customtkinter import *
import webbrowser
from timer import Timer

GRAY = "#303030"
FONT = ("Work Sans", 15, "normal")

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
                               fg_color="#3c007a", command=lambda *args: self.return_endpoint('code'), hover_color = '#2A0944', corner_radius=10)
        self.code.grid(column=2, row=1, padx=5, pady=5)


        self.math = CTkButton(self.root, width=50, height=25, text="Math", font=FONT, bg_color=GRAY,
                               fg_color="#0055ab", command=lambda *args: self.return_endpoint('math'), hover_color="dark blue", corner_radius=10)
        self.math.grid(column=3, row=1, padx=5, pady=10)

        self.auto = CTkButton(self.root, command=self.open_timer, width=20, height=20, text="Timer", font=FONT, bg_color=GRAY,
                               fg_color="#7D1935", hover_color="#480e1f", corner_radius=10)
        self.auto.grid(column=2, row=2, columnspan=1)

        self.study.bind("<Button-1>", lambda *args: self.go_to('study'))

        self.code.bind("<Button-1>", lambda *args: self.return_endpoint('code'))
        self.code.bind("<Button-3>", lambda *args: self.go_to('code'))

        self.math.bind("<Button-1>", lambda *args: self.return_endpoint('math'))
        self.math.bind("<Button-3>", lambda *args: self.go_to('math'))


        self.root.mainloop()

    def return_endpoint(self, endpoint):
        self.selection = endpoint
        self.root.destroy()
        self.root.quit()


    def send_select(self):
        return self.selection

    def go_to(self, web):
        endpoints = {
            "study": "https://pixe.la/v1/users/mejxe/graphs/studygraph.html",
            "math": "https://pixe.la/v1/users/mejxe/graphs/mathgraph.html",
            "code": "https://pixe.la/v1/users/mejxe/graphs/codegraph.html"
        }
        webbrowser.open(endpoints[web])

    # POMODORO
    def open_timer(self):

        endpoints = [
            "study", "math", "code"
        ]
        self.timer = Timer(endpoints, self.root)
        if self.timer.commits > 0:
            self.selection = self.timer.ret
            self.auto_commits = self.timer.commits

