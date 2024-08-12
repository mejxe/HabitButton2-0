import requests

def fillPixel(commits_quantity, date, graph_endpoint):
    data = {
            "date": str(date),
            "quantity": str(commits_quantity)
                }
    requests.post(graph_endpoint, json=data)
