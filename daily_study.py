import os

import streak_beta_script
import json
import datetime
import requests

date_now = datetime.datetime.strftime(datetime.date.today(), "%Y%m%d")
headers = {"X-USER-TOKEN": os.environ.get("token")}

req_math = requests.get(f"https://pixe.la/v1/users/mejxe/graphs/mathgraph/{date_now}",
                           headers=headers)
req_code = requests.get(f"https://pixe.la/v1/users/mejxe/graphs/codegraph/{date_now}",
                           headers=headers)
print(req_code.json())
if "quantity" in req_code.json():
    code_quantity = req_code.json()["quantity"]
else:
    code_quantity = 0
if "quantity" in req_math.json():
    math_quantity = req_math.json()["quantity"]
else:
    math_quantity = 0



with open(r"C:\Users\mejxe\PycharmProjects\habbitTracker\commits.json", "r") as data_file:
    data = json.load(data_file)
    quantity = data["study"]
    data_to_update = {
        "code": int(code_quantity),
        'math': int(math_quantity),
        'study': int(code_quantity) + int(math_quantity)

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

streak_beta_script.daily_run()



