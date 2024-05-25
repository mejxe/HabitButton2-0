import os

import streak_beta_script
import json
import datetime
import requests
import api_comms
graph_endpoints = {"study": "https://pixe.la/v1/users/mejxe/graphs/studygraph",
                   "math": "https://pixe.la/v1/users/mejxe/graphs/mathgraph",
                   "code": "https://pixe.la/v1/users/mejxe/graphs/codegraph",
                   "japan":"https://pixe.la/v1/users/mejxe/graphs/japgrah"}

date_now = datetime.datetime.strftime(datetime.date.today(), "%Y%m%d")
headers = {"X-USER-TOKEN": os.environ.get("token")}




streak_beta_script.daily_run()
for name,endpoint in graph_endpoints.items():
    pix = api_comms.Pixela(endpoint,name)
    pix.get_pixel_attributes()



