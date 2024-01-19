from customtkinter import *
import math
from CTkMessagebox import  CTkMessagebox
import winsound

colors_code = ['#f4eaff','#d8b1fe','#bf80ff','#a247ff','#860eff',
                           "#6d00dc",'#5500ab','#3c007a','#240049','#080010']
colors_math = ['#daecfe','#a9d3ff','#78bbff','#47a2ff','#168aff',
                   '#006ad5','#0055ab','#003c7a','#002449','#000c18']

FONT = ("Work Sans Light", 70, "normal")
BFONT = ("Work Sans", 15, "normal")
CFONT = ("Work Sans", 17, "normal")
GRAY = "#303030"
class Timer(CTkToplevel):
    def __init__(self, graphs, root):
        super().__init__()
        self.title("Timer")
        self.geometry("450x350")
        self.configure(fg_color=GRAY)
        self.graphs = graphs
        self.iters = -1
        self.root = root
        self.commits = 0
        self.reps = 0
        self.pomodoros = 0
        self.ret = None
        self.wm_protocol("WM_DELETE_WINDOW", self.on_close)
        self.resizable(False,False)

        # Frame

        self.frame = CTkFrame(self, width=400, height=300, bg_color='#464646', fg_color="#464646")
        self.frame.pack(pady=20)
        # Timer widget
        self.clock = CTkLabel(self.frame, text="00:00:00", font=FONT, bg_color="#464646", fg_color="#464646")
        self.clock.place(x=200, y=70, anchor="center")
        self.br = CTkLabel(self.frame,text="break.", font=("Work Sans", 13, "normal"))
        self.wk = CTkLabel(self.frame,text="work.", font=("Work Sans", 13, "normal"))
        # Timer Buttons

        # start/stop
        self.start = CTkButton(self.frame, width=70, height=35, text="Start.", command=self.deafult, font=BFONT, corner_radius=10, fg_color="#A619D5", state="disabled", hover_color="#17005f", text_color="black")

        self.start.place(x=100, y=150, anchor="center")
        # reset
        self.reset = CTkButton(self.frame, width=70, height=35, text="Reset.", font=BFONT, corner_radius=10, fg_color="#40045A", state="disabled",hover_color="#8a09c2", command=self.over, text_color="black")

        self.reset.place(x=300, y=150, anchor="center")

        self.pause_button = CTkButton(self.frame, width=70, height=35, text="Pause.", font=BFONT, corner_radius=10, fg_color="#6D0D91", state="disabled",hover_color="#b016ea", command=self.pause, text_color="black")
        self.pause_button.place(x=200, y=150, anchor="center")
        # graph
        self.r = IntVar()
        self.r.set(0)

        self.check = CTkRadioButton(self.frame, text="Math", font=CFONT, variable=self.r, value=1, fg_color="#0055ab", hover_color="#0055ab",command=self.enable, state='normal')
        self.check2 = CTkRadioButton(self.frame, text="Code", font=CFONT, variable=self.r, value=2, fg_color="#3c007a", hover_color="#3c007a",command=self.enable, state='normal')

        self.check.place(x=150, y=220, anchor="center")
        self.check2.place(x=270, y=220, anchor="center")


        self.var = IntVar()
        self.pomodoro_switch = CTkSwitch(self.frame, text="Timer", font=CFONT, button_color="#A619D5", button_hover_color="#8a09c2", progress_color="#40045A", onvalue=1, offvalue=0, variable=self.var, command=self.pomodoro)
        self.pomodoro_switch.place(x=150, y=250)

        self.pomodoro_done = CTkLabel(self.frame,text_color="#AA5656", text="", font=(CTkFont(size=16)))

        self.mainloop()

    def start_count(self):
        self.pause_button.configure(state="normal")
        self.reset.configure(state="normal")
        self.start.configure(state="disabled")
        self.check.configure(state="disabled")
        self.check2.configure(state="disabled")
        self.i = False
        self.iters = 0
        self.pomodoro_switch.configure(state="disabled")

    def deafult(self):
        self.start_count()
        self.counter(2)

    def counter(self, time):
        # time assessment
        self.strftime = time
        hours = math.floor(self.strftime/3600)
        minutes = math.floor(self.strftime/60)
        seconds = self.strftime % 60
        minutes_not_formatted = minutes
        # time formatting
        if hours < 10:
            hours = f"0{hours}"
        if minutes < 10:
            minutes = f"0{minutes}"
        if seconds < 10:
            seconds = f"0{seconds}"
        if self.var.get() == 0:
            self.clock.configure(text=f"{hours}:{minutes}:{seconds}")
        if self.var.get() == 1:
            self.clock.configure(text=f"{minutes}:{seconds}")
        print("siema", self.strftime)

        # begin
        if self.strftime > 0:
            self.after_id = self.after(1000, self.counter, self.strftime-1)

        # POMODORO
        if self.var.get() == 1:
            if self.reps <= 8:
                if self.strftime <= 0:
                    self.pomodoro_count()
            else:
                self.over()
                self.popup()

        # color change every 10 minutes
        if self.var.get() == 0:
            if minutes_not_formatted % 10 == 0 and minutes_not_formatted != 0:
                self.color_change()



        # over
        if self.var.get() == 0:
            if not self.strftime > 0:
                self.over()
                self.popup()

            if self.strftime == 60:
                self.cache(1)

    # enable/disable start button
    def enable(self):
        if self.r.get() != 0:
            self.start.configure(state="normal")
        if self.r.get() == 2:
            self.start.configure(fg_color="#F4EAFF", text_color="black", hover_color="#e2c8ff")
            self.pause_button.configure(fg_color="#9875BD", text_color="white", hover_color="#8d67b6")
            self.reset.configure(fg_color="#3C007A", text_color="white", hover_color="#290053")
        if self.r.get() == 1:
            self.start.configure(fg_color="#DAECFE", text_color="black", hover_color="#acd4fd")
            self.pause_button.configure(fg_color="#6D94BC", text_color="black", hover_color="#5985b3")
            self.reset.configure(fg_color="#003C7A", text_color="black", hover_color="#003163")



    def pause(self):
        self.i ^= True
        if self.i:
            self.after_cancel(self.after_id)
            self.pause_button.configure(text="Resume.")
        else:
            self.after_id = self.after(1000, self.counter, self.strftime-1)
            self.pause_button.configure(text="Pause.")

    def color_change(self):
        self.iters += 1
        colors = []
        if self.r.get() == 1:
            colors = colors_math
        if self.r.get() == 2:
            colors = colors_code
        self.clock.configure(text_color=colors[self.iters])


    def over(self):
        self.after_cancel(self.after_id)
        if self.var.get() == 0:
            self.clock.configure(text="00:00:00", text_color="white")
        else:
            self.clock.configure(text="00:00", text_color="white")
        self.start.configure(fg_color="#A619D5")
        self.pause_button.configure(fg_color="#6D0D91")
        self.reset.configure(fg_color="#40045A")
        self.enable()
        self.pause_button.configure(state="disabled")
        self.reset.configure(state="disabled")
        self.i = False
        self.pause_button.configure(text="Pause.")
        self.wk.place(x=9999,y=9999)
        self.br.place(x=9999,y=0)

    def cache(self, commits):
        self.commits += commits
        if self.r.get() == 1:
            print("math")
            self.ret = "math"

        if self.r.get() == 2:
            print("code")

            self.ret = "code"


    def on_close(self):
        self.root.destroy()

    def popup(self):
        self.attributes('-topmost', 1)
        self.attributes('-topmost', 0)
        self.focus_force()
        self.lift()
        self.deiconify()
        winsound.MessageBeep()
        color = "blue"
        hover_color= "gray"
        if self.r.get() == 1:
            color = "#6D94BC"
            hover_color = "#c5d4e4"
        if self.r.get() == 2:
            color = "#9875BD"
            hover_color = "#d6c8e5"
        mess = CTkMessagebox(master=self,title="Save?",message="Close the timer, so your progress is uploaded.",
                             option_1="Ok", icon_size=(1,1), button_color=color,fade_in_duration=1,
                             cancel_button=None, fg_color="#464646", bg_color=GRAY, width=150, height=80, font=("Work Sans", 12, "normal"),button_hover_color=hover_color)
        if mess.get() == "Ok":
            self.root.destroy()

    def pomodoro(self):
        if self.var.get() == 0:
            self.pomodoro_switch.configure(text="Timer", button_color="#A619D5", progress_color="#40045A", button_hover_color="#8a09c2")
            self.clock.configure(text="00:00:00")
            self.start.configure(command=self.deafult)
            self.br.place(x=99999, y=50)
            self.wk.place(x=99999, y=70)
            self.pomodoro_done.place(x=9999, y=9999)

        if self.var.get() == 1:
            self.pomodoro_switch.configure(text="Pomodoro",button_color="#AA5656",progress_color="#874444", button_hover_color='#5f3030')
            self.clock.configure(text="00:00")
            self.start.configure(command=self.pomodoro_count)
            self.br.place(x=300,y=50)
            self.wk.place(x=302, y=70)
            self.pomodoro_done.place(x=75, y=55)

    def pomodoro_count(self):
        if self.reps % 2 == 0:
            self.wk.configure(text_color="#AA5656")
            self.br.configure(text_color="white")
            self.start_count()
            self.counter(1800)
        elif self.reps % 2 != 0:
            if self.reps == 3:
                self.cache(1)
            if self.reps % 7 == 0 and self.reps != 0:
                self.cache(1)
                self.counter(1200)
                self.wk.configure(text_color="white")
                self.br.configure(text_color="#AA5656")
                self.pomodoros +=1
            else:
                self.counter(300)
                self.wk.configure(text_color="white")
                self.br.configure(text_color="#AA5656")
                self.pomodoros += 1

        if self.pomodoros == 1:
            self.pomodoro_done.configure(text="✓")
        if self.pomodoros == 2:
            self.pomodoro_done.configure(text="✓ ✓")
        if self.pomodoros == 3:
            self.pomodoro_done.configure(text="✓ ✓\n✓")
        if self.pomodoros == 4:
            self.pomodoro_done.configure(text="✓ ✓\n✓ ✓")
        self.reps += 1