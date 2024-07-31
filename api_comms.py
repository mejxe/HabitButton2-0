import datetime
import requests
import json
import os

class Pixela:
    def __init__(self,graph_endpoint, graph_name, auto_commits=0):
        self.username = "mejxe"
        self.token = os.environ.get("token")
        self.graph_endpoint = graph_endpoint
        self.graph_name = graph_name
        self.headers = {
            "X-USER-TOKEN": self.token
        }
        self.date_now = datetime.datetime.strftime(datetime.date.today(), "%Y%m%d")
        self.auto_commits = auto_commits
        # PIXEL ATTRIBUTES


    def get_pixel_attributes(self):
        req = requests.get(f"{self.graph_endpoint}/{self.date_now}",
                           headers=self.headers)
        response = req.json()
        try:
            self.quantity = (int(response["quantity"]) + self.auto_commits)
        except KeyError:
            self.quantity = 0
            self.create_pixel()
        print(response)
        return self.quantity

    def create_pixel(self):
        # print(self.quantity)
        # if yesterday == "on":
        #     print('yesterday')
        #     self.date_now = datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(days=1), "%Y%m%d")
        # if yesterday == "off":
        #     print("today")
        #     self.date_now = datetime.datetime.strftime(datetime.date.today(), "%Y%m%d")
        # data = {
        #     "date": self.date_now,
        #     "quantity": str(self.quantity)
        #     }
        # req = requests.post(f"{self.graph_endpoint}", json=data, headers=self.headers)

        data = {
            "date":self.date_now,
            "quantity": "0"
        }
        req = requests.post(f"{self.graph_endpoint}", json=data, headers=self.headers)
        print(req.json())


    def update_pixel(self, yesterday:bool=False):
        data = {
            "quantity": str(self.quantity)
        }
        if yesterday:
            self.date_now = datetime.datetime.strftime(datetime.datetime.today() - datetime.timedelta(days=1), "%Y%m%d")
            study_time = requests.get(f"https://pixe.la/v1/users/mejxe/graphs/studygraph/{self.date_now}", headers=self.headers).json()["quantity"]
            self.upload_study(str(int(study_time) + self.quantity))
        req = requests.put(f"{self.graph_endpoint}/{self.date_now}", json=data, headers=self.headers)
        if not yesterday:
            with open("commits.json", "r") as data_file:
                local = json.load(data_file)
                local_update = {self.graph_name: int(self.quantity)}
                local.update(local_update)
            with open("commits.json","w") as data_file:
                json.dump(local,data_file,indent=2)
            self.calculate_study()
        print(req.json())

    def calculate_study(self):
        with open("commits.json", "r") as data_file:
            data = json.load(data_file)
            study_time = 0
            for time in data.values():
                study_time += int(time)
        self.upload_study(study_time)


    def upload_study(self, study_time):
        data = {
            "date": self.date_now,
            "quantity": str(study_time)
        }
        req = requests.post("https://pixe.la/v1/users/mejxe/graphs/studygraph", json=data, headers=self.headers)


# DELETE
    def clear_pixel(self):
        self.quantity = 0

# CLEAR TIMER COMMITS DATA
    def clear_timer(self):
        try:
            with open("timer_commits.json", "r") as dataload:
                data = json.load(dataload)

                clear_commits = {
                    self.graph_name: float(data[self.graph_name]%1),
                               }
                data.update(clear_commits)
            # update data
            with open("timer_commits.json", "w") as loaddata:
                json.dump(data, loaddata, indent=4)
        except KeyError:
            pass


    def increment(self):
        self.quantity = int(self.quantity) + 1
        return self.quantity




