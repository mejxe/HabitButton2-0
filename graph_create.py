import requests
import os
"""
Graph managing shortcut,
run only if you want to make, update or delete an endpoint
"""



graph_data = {
            "id": "japgrah",
            "name": "Japanese",
            "unit": "hours",
            "type": "int",
            "color": "momiji"
}
token = os.environ.get("token")
headers = {
            "X-USER-TOKEN": token
        }

def create():
    graph = requests.post(f'https://pixe.la/v1/users/mejxe/graphs', headers=headers,
                          json=graph_data)
    print(graph.text)

def delete(graph_endpoint):
    graph = requests.delete(graph_endpoint, headers=headers)
    print(graph.text)


def update(graph_endpoint):
    graph = requests.put(graph_endpoint, headers=headers, json=graph_data)
    print(graph.text)

def update_user(user):
    print(requests.put(f"https://pixe.la/v1/users/{user}", headers=headers, json={"thanksCode":"22c5698062c595820b6b815ae2cd76b83da9eda658402bce3bc0a066c0ddb250"}).text)

create()