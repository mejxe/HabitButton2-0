from customtkinter import *
from api_comms import Pixela
import webbrowser
FONT = ("Work Sans", 15, "bold")

class Gui:
    def __init__(self, quantities, pixela):
        self.root = CTk()
        self.root.config(background="gray", width=300, height=500, pady=20, padx=20)
        self.root.resizable(False, False)
        # TABS
        self.tabview = CTkTabview(master=self.root)
        self.tabview.add("Study")
        self.tabview.add("Code")
        self.tabview.add("Math")
        # PARAMETERS
        self.pixela = pixela
        self.quantities = quantities
        self.tabview.grid()
        # COLORS
        self.green = ['#effaef','#c2edc5','#96e09b','#70d577','#44c94d',
                       '#31aa39','#26842c','#1b5e1f','#103813']
        self.blue = ['#daecfe','#a9d3ff','#78bbff','#47a2ff','#168aff',
                       '#006ad5','#0055ab','#003c7a','#002449','#000c18']
        self.purple = ['#f4eaff','#d8b1fe','#bf80ff','#a247ff','#860eff',
                       "#6d00dc",'#5500ab','#3c007a','#240049','#080010']

       # Buttons

        self.studybutton = CTkButton(self.tabview.tab("Study"), height=300, width=300,
                                text=f"Press if your done\nToday: {self.quantities[0][pixela.graph_endpoints[0]]}h", bg_color="gray",
                                fg_color=self.green[int(self.quantities[0][pixela.graph_endpoints[0]])], text_color="black", font=FONT)
        self.studybutton.grid()

        self.mathbutton = CTkButton(self.tabview.tab("Math"), height=300, width=300,
                                     text=f"Press if your done\nToday: {self.quantities[1][pixela.graph_endpoints[1]]}h", bg_color="gray",
                                     fg_color=self.blue[int(self.quantities[1][pixela.graph_endpoints[1]])], text_color="black", font=FONT, command=self.color_change_math)
        self.mathbutton.grid()

        self.codebutton = CTkButton(self.tabview.tab("Code"), height=300, width=300,
                                     text=f"Press if your done\nToday: {self.quantities[2][pixela.graph_endpoints[2]]}h", bg_color="gray",
                                     fg_color=self.purple[int(self.quantities[2][pixela.graph_endpoints[2]])], text_color="black", font=FONT)
        self.codebutton.grid()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()
    # Functionality

    def color_change_study(self):
        quant = self.pixela.quantity_up(0)
        if quant >= 9:
            self.studybutton.configure(fg_color=self.green[8],
                                  text=f"Press if your done\nToday: {quant}", text_color="white")
        else:

            self.studybutton.configure(fg_color=self.green[int(quant)],
                                  text=f"Press if your done\nToday: {quant}h")

    def color_change_code(self):
        quant = self.pixela.quantity_up(2)
        if quant >= 9:
            self.codebutton.configure(fg_color=self.purple[8],
                                       text=f"Press if your done\nToday: {quant}", text_color="white")
        else:

            self.codebutton.configure(fg_color=self.purple[int(quant)],
                                       text=f"Press if your done\nToday: {quant}h")

    def color_change_math(self):
        quant = self.pixela.quantity_up(1)
        if quant >= 9:
            self.mathbutton.configure(fg_color=self.blue[8],
                                       text=f"Press if your done\nToday: {quant}", text_color="white")
        else:

            self.mathbutton.configure(fg_color=self.blue[int(quant)],
                                       text=f"Press if your done\nToday: {quant}h")
    def on_close(self):
        self.pixela.create_pixel()
        self.root.destroy()

