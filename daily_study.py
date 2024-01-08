import requests
import json
import datetime

with open(r"C:\Users\mejxe\PycharmProjects\habbitTracker\commits.json", "r") as data_file:
    data = json.load(data_file)
    quantity = data["study"]
    data_to_update = {
        "code": 0,
        'math': 0,
        'study': 0

    }
    data.update(data_to_update)

# date_now = datetime.datetime.strftime(datetime.date.today(), "%Y%m%d")
# token = os.environ.get("token")
#
# params = {
#     "quantity": str(quantity),
#     "date": date_now
# }
#
# headers = {
#             "X-USER-TOKEN": token
# }
# while True:
#     response = requests.post("https://pixe.la/v1/users/mejxe/graphs/studygraph", headers=headers, json=params).json()
#     if "isRejected" in response:
#         print(response)
#     else:
#         print(response)
#         break
with open(r"C:\Users\mejxe\PycharmProjects\habbitTracker\commits.json", "w") as data_file:
    json.dump(data, data_file, indent=2)



