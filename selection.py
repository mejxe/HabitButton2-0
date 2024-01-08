from customtkinter import *
import webbrowser

GRAY = "#565656"
class Select:
    def __init__(self):
        self.root = CTk()
        self.root.config(background="#565656", width=200, height=200, pady=20, padx=20)
        self.root.resizable(False, False)


    # Buttons

    #
    #     self.code = CTkRadioButton(self.root, text="Code", value="code", variable=self.selection, bg_color='#565656',
    #                                text_color='black', hover_color='purple', border_color='black', fg_color='purple')
    #     self.code.grid(column=0, row=0, padx=10, pady=10)
    #     self.study = CTkRadioButton(self.root, text="Study", value="study", variable=self.selection, bg_color='#565656',
    #                                text_color='black', hover_color='green', border_color='black', fg_color='green')
    #     self.study.grid(column=0, row=1, padx=10, pady=10)
    #     self.math = CTkRadioButton(self.root, text="Math", value="math", variable=self.selection, bg_color='#565656',
    #                                text_color='black', hover_color='blue', border_color='black', fg_color='blue')
    #     self.math.grid(column=0, row=2, padx=10, pady=10)
    #
    #     self.submit = CTkButton(self.root, text="Submit", bg_color="#565656", command=self.get_var)
    #     self.submit.grid(column=0,row=3)
    #
    #
    #     self.root.grid_propagate(False)


        self.study = CTkButton(self.root, text="Study", font=("Bahnshcrift", 15, "bold"), bg_color=GRAY,
                               fg_color="#26842c")
        self.study.grid(column=0, row=1, padx=10, pady=10)


        self.code = CTkButton(self.root, text="Code", font=("Bahnshcrift", 15, "bold"), bg_color=GRAY,
                               fg_color="#3c007a", command=lambda *args: self.return_endpoint('code'))
        self.code.grid(column=0, row=2, padx=10, pady=10)


        self.math = CTkButton(self.root, text="Math", font=("Bahnshcrift", 15, "bold"), bg_color=GRAY,
                               fg_color="#0055ab", command=lambda *args: self.return_endpoint('math'))
        self.math.grid(column=0, row=3, padx=10, pady=10)

        self.study.bind("<Button-1>", lambda *args: self.return_endpoint('study'))
        self.study.bind("<Button-3>", lambda *args: self.go_to('study'))

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
