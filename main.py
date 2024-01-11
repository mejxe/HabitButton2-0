from api_comms import Pixela
from guiproject import Gui
# graph_endpoints = {"study": "https://pixe.la/v1/users/mejxe/graphs/studygraph",
#                    "math": "https://pixe.la/v1/users/mejxe/graphs/mathgraph",
#                    "code": "https://pixe.la/v1/users/mejxe/graphs/codegraph"}

pixela = Pixela()
pixela.get_pixel_attributes()
quantities = pixela.quantities


ui = Gui(quantities=quantities, pixela=pixela)
