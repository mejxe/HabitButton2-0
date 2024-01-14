from customtkinter import *
import math

colors_code = ['#f4eaff','#d8b1fe','#bf80ff','#a247ff','#860eff',
                           "#6d00dc",'#5500ab','#3c007a','#240049','#080010']
colors_math = ['#daecfe','#a9d3ff','#78bbff','#47a2ff','#168aff',
                   '#006ad5','#0055ab','#003c7a','#002449','#000c18']

FONT = ("Work Sans Light", 70, "normal")
BFONT = ("Work Sans", 15, "normal")
CFONT = ("Work Sans", 17, "normal")
GRAY = "#303030"
class Timer(CTkToplevel):
    def __init__(self, graphs):
        super().__init__()
        self.title("Timer")
        self.geometry("450x350")
        self.configure(fg_color=GRAY)
        self.graphs = graphs
        self.iters = -1

        # Frame

        self.frame = CTkFrame(self, width=400, height=300, bg_color='#464646', fg_color="#464646")
        self.frame.pack(pady=20)
        # Timer widget
        self.clock = CTkLabel(self.frame, text="00:00:00", font=FONT, bg_color="#464646", fg_color="#464646")
        #self.clock.grid(row=0, column=1, columnspan=2, pady=20, sticky="e")
        self.clock.place(x=200, y=70, anchor="center")
        # Timer Buttons

        # start/stop
        self.start = CTkButton(self.frame, width=70, height=35, text="Start.", font=BFONT, corner_radius=10, fg_color="#A619D5", command=self.start_count, state="disabled", hover_color="#17005f")
        #self.start.grid(row=1, column=1,sticky="e", padx=10)
        self.start.place(x=100, y=150, anchor="center")
        # reset
        self.reset = CTkButton(self.frame, width=70, height=35, text="Reset.", font=BFONT, corner_radius=10, fg_color="#40045A", state="disabled",hover_color="red", command=self.over)
        #self.reset.grid(row=1, column=2, sticky="w")
        self.reset.place(x=300, y=150, anchor="center")

        self.pause_button = CTkButton(self.frame, width=70, height=35, text="Pause.", font=BFONT, corner_radius=10, fg_color="#6D0D91", state="disabled",hover_color="red", command=self.pause)
        self.pause_button.place(x=200, y=150, anchor="center")
        # graph
        self.r = IntVar()
        self.r.set(0)

        self.check = CTkRadioButton(self.frame, text="Math", font=CFONT, variable=self.r, value=1, fg_color="#0055ab", hover_color="#0055ab",command=self.enable)
        self.check2 = CTkRadioButton(self.frame, text="Code", font=CFONT, variable=self.r, value=2, fg_color="#3c007a", hover_color="#3c007a",command=self.enable)

        self.check.place(x=150, y=220, anchor="center")
        self.check2.place(x=270, y=220, anchor="center")

        self.mainloop()

    def start_count(self):
        self.strftime = 3600
        print(self.strftime)
        self.pause_button.configure(state="enabled")
        self.reset.configure(state="enabled")
        self.start.configure(state="disabled")
        self.check.configure(state="disabled")
        self.check2.configure(state="disabled")
        self.i = False
        self.counter()
    def counter(self):
        # time assessment
        self.strftime = self.strftime - 1
        hours = math.floor(self.strftime/3600)
        minutes = math.floor(self.strftime/60)
        seconds = self.strftime % 60
        minutes_not_formatted = minutes
        # time formatting
        if hours == 0:
            hours = "00"
        if minutes < 10:
            minutes = f"0{minutes}"
        if seconds < 10:
            seconds = f"0{seconds}"

        self.clock.configure(text=f"{hours}:{minutes}:{seconds}")

        # begin
        self.after_id = self.after(1000, self.counter)

        # color change every 10 minutes
        if minutes_not_formatted % 10 == 0:
            self.color_change()



        # over
        if self.strftime == 0:
            self.over()
            #TODO: count the reps and return to main gui

    # enable/disable start button
    def enable(self):
        if self.r.get() != 0:
            self.start.configure(state="enabled")
        if self.r.get() == 2:
            self.start.configure(fg_color="#F4EAFF")
            self.pause_button.configure(fg_color="#9875BD")
            self.reset.configure(fg_color="#3C007A")
        if self.r.get() == 1:
            self.start.configure(fg_color="#DAECFE")
            self.pause_button.configure(fg_color="#6D94BC")
            self.reset.configure(fg_color="#003C7A")



    def pause(self):
        self.i ^= True
        if self.i:
            self.after_cancel(self.after_id)
            self.pause_button.configure(text="Resume.")
        else:
            self.after(1000, self.counter)
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
        self.clock.configure(text="00:00:00", text_color="white")
        self.start.configure(fg_color="#A619D5")
        self.pause_button.configure(fg_color="#6D0D91")
        self.reset.configure(fg_color="#40045A")
        self.enable()
        self.pause_button.configure(state="disabled")
        self.reset.configure(state="disabled")
        self.check.configure(state="enabled")
        self.check2.configure(state="enabled")


