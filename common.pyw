import requests

header = {
    "X-USER-TOKEN": "dsadjigojrtio63"
}

data = {
    "unit": "hours"
}

s=requests.put('https://pixe.la/v1/users/mejxe/graphs/mathgraph', headers=header, json=data)

print(s.text)