import datetime
import requests
import json
import os

class Pixela:
    def __init__(self):
        self.username = "mejxe"
        self.token = os.environ.get("token")
        self.graph_data = {
            "id": "studygraph",
            "name": "Study Tracker",
            "unit": "hours",
            "type": "int",
            "color": "shibafu"
        }
        self.graph_endpoints = ["https://pixe.la/v1/users/mejxe/graphs/studygraph",
                                "https://pixe.la/v1/users/mejxe/graphs/mathgraph",
                                "https://pixe.la/v1/users/mejxe/graphs/codegraph"]
        self.graph_title = ["Code Tracker","Study Tracker", "Math Tracker"]
        self.headers = {
            "X-USER-TOKEN": self.token
        }
        self.quantities = []
        self.date_now = datetime.datetime.strftime(datetime.date.today(), "%Y%m%d")
        # PIXEL ATTRIBUTES


    def get_pixel_attributes(self):
        for i in range(len(self.graph_endpoints)):
            req = requests.get(f"{self.graph_endpoints[i]}/{self.date_now}",
                               headers=self.headers)
            response = req.json()
            print(response)

            try:
                my_dict = {self.graph_endpoints[i]:response["quantity"]}
                self.quantities.append(my_dict)
            except KeyError:

                if response["message"] == "Specified pixel not found.":
                    my_dict = {self.graph_endpoints[i]:"0"}
                    self.quantities.append(my_dict)

                elif response["isRejected"]:

                    while True:
                                s = requests.get(f"{self.graph_endpoints[i]}/{self.date_now}", headers=self.headers)

                                if "message" in s.json():
                                    if s.json()["message"] == "Specified pixel not found.":
                                        my_dict = {self.graph_endpoints[i]: "0"}
                                        self.quantities.append(my_dict)
                                        print('not found')
                                        break

                                if 'isRejected' in s.json():
                                    print('rejected')
                                    pass

                                else:
                                    if "quantity" in s.json():
                                        my_dict = {self.graph_endpoints[i]:s.json()["quantity"]}
                                        self.quantities.append(my_dict)
                                        print("success")
                                        break

                                    else: raise Exception(TimeoutError)

            with open('commits.json', "r") as data_file:
                data = json.load(data_file)
                data_to_update = self.quantities[i]
                data.update(data_to_update)

            with open('commits.json', "w") as data_file:
                json.dump(data, data_file, indent=2)

        print(self.quantities)






    def graph_create(self):
        graph = requests.post(f'https://pixe.la/v1/users/{self.username}/graphs', headers=self.headers, json=self.graph_data)
        print(graph.text)

    def create_pixel(self):
        for i in range(len(self.graph_endpoints)):
            data = {
                "date": self.date_now,
                "quantity": str(self.quantities[i][self.graph_endpoints[i]])
                }
            while True:
                req = requests.post(f"{self.graph_endpoints[i]}", json=data, headers=self.headers)
                response = req.json()
                print(response)
                if "isRejected" in response:
                    print(response)
                else:
                    break

            self.calculate_study()


    def calculate_study(self):
        with open("commits.json", "r") as data_file:
            data = json.load(data_file)
            self.study_time = {"study": (int(data['math']) + int(data['code']))}
            data.update(self.study_time)
        with open('commits.json', "w") as data_file:
            json.dump(data, data_file, indent=2)
        self.upload_study()


    def upload_study(self):
        data = {
            "date": self.date_now,
            "quantity": str(self.study_time["study"])
        }
        while True:
            req = requests.post("https://pixe.la/v1/users/mejxe/graphs/studygraph", json=data, headers=self.headers)
            response = req.json()
            print(response)
            if "isRejected" in response:
                print(response)
            else:
                break

    def update_pixel(self):
        print(self.quantity)
        data = {
            "quantity":str(self.quantity)
        }
        for graph_endpoint in self.graph_endpoints:
            while True:
                try:
                    req = requests.put(f"{graph_endpoint}/{self.date_now}", json=data, headers=self.headers)
                    response = req.json()
                    print(response)
                    if response["isRejected"]:
                        print(response)
                    else:
                        break
                except KeyError:
                    break



# DELETE
    def clear_pixel(self):
        data = {
            "date": self.date_now,
        }
        req = requests.delete(f"{self.graph_endpoint}/{self.date_now}", headers=self.headers)
        while not req.json()["isSuccess"]:
            try:
                p = requests.delete(f"{self.graph_endpoint}/{self.date_now}",
                                    headers=self.headers)
                _ = p.json()["isRejected"]
            except KeyError:
                print("Success")
                break
        self.quantity = 0


    def quantity_up(self, graph_endpoint):
        with open("commits.json", "r") as data_file:
            data = json.load(data_file)
            quantity = int(data[self.graph_endpoints[graph_endpoint]])
            quantity += 1
            self.quantity = quantity
            data_to_update = {self.graph_endpoints[graph_endpoint]: quantity}
            data.update(data_to_update)

        with open('commits.json', "w") as data_file:
            json.dump(data, data_file, indent=2)
        return quantity

    def json_clear(self):
        with open('commits.json', 'r') as data_file:
            data = json.load(data_file)
            data_to_update = {self.graph_name: 0}
            data.update(data_to_update)
        with open('commits.json', 'w') as data_file:
            json.dump(data, data_file, indent=2)
        self.quantity = 0


