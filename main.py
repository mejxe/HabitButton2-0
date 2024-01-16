from api_comms import Pixela
from gui import Gui
from selection import Select

graph_endpoints = {"study": "https://pixe.la/v1/users/mejxe/graphs/studygraph",
                   "math": "https://pixe.la/v1/users/mejxe/graphs/mathgraph",
                   "code": "https://pixe.la/v1/users/mejxe/graphs/codegraph"}

while True:
    select = Select()
    try:
        pixela = Pixela(graph_endpoints[select.selection], graph_name=select.selection, auto_commits=select.auto_commits)
        quantity = pixela.get_pixel_attributes()
        ui = Gui(quantity=int(quantity), pixela=pixela)
    except AttributeError:
        exit()