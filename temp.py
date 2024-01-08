import datetime

import requests

username = "mejxe"
token = "dsadjigojrtio63"
login = {
    "token": token,
    "username": username,
    "agreeTermsOfService":"yes",
    "notMinor":"yes"
}
headers = {
    "X-USER-TOKEN": token
}
# log = requests.post(f'https://pixe.la/v1/users/{username}/graphs', json=login)
# print(log.text)

graph_data = {
    "id": "mathgraph",
    "name": "Math Tracker",
    "unit": "commits",
    "type": "int",
    "color": "ichou"
}

graph = requests.post(f'https://pixe.la/v1/users/{username}/graphs', headers=headers, json=graph_data)
#print(graph.text)
while True:
    userinput = input("How many projects completed? ")
    try:
        int(userinput)
        break
    except:
        pass

date_now = datetime.datetime.strftime(datetime.date.today(), "%Y%m%d")

value_data = {
    "date": date_now,
    "quantity": userinput

}

value_add = requests.put(f"https://pixe.la/v1/users/mejxe/graphs/graph2/{date_now}", headers=headers, json=value_data)
print(value_add.text)
