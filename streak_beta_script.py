import os
import requests
from datetime import datetime, timedelta
import json
token = os.environ.get("token")
headers = {
            "X-USER-TOKEN": token
        }
endpoints = {"study": "https://pixe.la/v1/users/mejxe/graphs/studygraph/pixels",
                   "math": "https://pixe.la/v1/users/mejxe/graphs/mathgraph/pixels",
                   "code": "https://pixe.la/v1/users/mejxe/graphs/codegraph/pixels"}


# get the streaks from the cache file
do_not_check_cache = False
with open("streaks.json","r") as st:
    if not not st.read():
        st.seek(0)
        streaks = json.load(st)
    else:
        do_not_check_cache = True
        streaks = {"study":{},"code":{},"math":{}}

# for i, j in enumerate(req.json()["pixels"]):
#     year = j[0:4]
#     month = j[4:6]
#     day = j[6:8]
#     year = int(year)
#     month = int(month)
#     day = int(day)
#     today = datetime.date(year=year,month=month,day=day)
#     year = req.json()["pixels"][i+1][0:4]
#     month = req.json()["pixels"][i+1][4:6]
#     day = req.json()["pixels"][i+1][6:8]
#     year = int(year)
#     month = int(month)
#     day = int(day)
#     next_day = datetime.date(year=year,month=month,day=day)
#     if i < len(req.json()["pixels"])-:
#         if next_day - today == datetime.timedelta(days=1):
#             streak += 1
#         else:
#             streak = 0
#
#     print(streak)


def get_pixels(endpoint:str, start_from: str = None) -> list:
    if start_from is not None:
        json = {"from": start_from}
        req = requests.get(endpoints[endpoint], headers=headers, json=json)
    else:
        req = requests.get(endpoints[endpoint], headers=headers)

    return req.json()["pixels"]


def cache_to_dir(type: str, streak_latest_day: str, streak_number: int):
    streaks[type][streak_latest_day] = streak_number


def streak_counter(graph_pixels: list, graph_type:str) -> tuple:
    streak_going = True
    i: int = len(graph_pixels) - 1
    streak_number: int = 1
    streak_latest_day = graph_pixels[i]
    while streak_going and len(graph_pixels) != 0:
        day_new = datetime.strptime(graph_pixels[i], "%Y%m%d")
        day_bef = datetime.strptime(graph_pixels[i-1], "%Y%m%d")
        # check if the day is in cache
        day_strftime = datetime.strftime(day_new, "%Y%m%d")
        if not do_not_check_cache:
            if day_strftime in streaks[graph_type]:
                streak_number += streaks[graph_type][day_strftime] - 1
                streak_going = False
        if day_new - day_bef == timedelta(days=1):
            graph_pixels.pop()
            streak_number += 1
            i -= 1
            print(day_new)
        else:
            streak_going = False
            cache_to_dir(graph_type,streak_latest_day, streak_number)
    return streak_latest_day, streak_number
# just enter the graph name
def calculate(endpoint):
    yesterday = [datetime.strftime(datetime.today()-timedelta(days=1) , "%Y%m%d")]
    try:
        pixels = get_pixels(endpoint,streaks[endpoint][yesterday])
    except KeyError:
        pixels = get_pixels(endpoint)
    streak_day, streak_number = streak_counter(pixels,endpoint)
    return streak_day, streak_number
def daily_run():
    global streaks
    code_streak, code_day = calculate("code")
    math_streak, math_day = calculate("math")
    study_streak, study_day = calculate("study")
    streaks = {"study":{study_day:study_streak}, "code":{code_day:code_streak},"math":{math_day:math_streak}}

with open("streaks.json","w") as f:
    json.dump(streaks,f, indent=4)



