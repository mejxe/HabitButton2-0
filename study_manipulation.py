import requests
import os
import datetime
token = os.environ.get("token")
headers = {
    "X-USER-TOKEN": token}
def reset_study(yesterday:bool):
    if yesterday:
        date_now = datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(days=1), "%Y%m%d")
    else:
        date_now = datetime.datetime.strftime(datetime.date.today(), "%Y%m%d")
    data = {
        "date": date_now,
        "quantity": "0"
    }
    requests.post("https://pixe.la/v1/users/mejxe/graphs/studygraph", json=data, headers=headers)

reset_study(True)