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
try:
    with open("streaks.json","r") as st:
        if not not st.read():
            st.seek(0)
            streaks = json.load(st)
        else:
            do_not_check_cache = True
            streaks = {"study":{},"code":{},"math":{}}
except FileNotFoundError:
    do_not_check_cache = True
    streaks = {"study": {}, "code": {}, "math": {}}

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


def get_pixels(endpoint:str, start_from: str or bool) -> tuple:
    streak_before = 0
    if start_from is not None:
        pars = {"from": start_from}
        req = requests.get(endpoints[endpoint], headers=headers, params=pars)
        streak_before = streaks[endpoint][start_from]
    else:
        req = requests.get(endpoints[endpoint], headers=headers)
    print(req.text, req.url)
    return req.json()["pixels"], streak_before


# def cache_to_dir(type: str, streak_latest_day: str, streak_number: int):
#     streaks[type][streak_latest_day] = streak_number
#     print(streaks)


def streak_counter(graph_pixels: list, streak_before:int = 0) -> tuple:
    if datetime.strftime(datetime.today()- timedelta(days=1), "%Y%m%d") not in graph_pixels:
        return datetime.strftime(datetime.today() - timedelta(days=1), "%Y%m%d"), 0
    streak_going = True
    i: int = len(graph_pixels) - 1
    streak_number: int = 1 + streak_before
    if streak_before != 0:
        streak_number -= 1
    streak_latest_day = graph_pixels[i]
    while streak_going and len(graph_pixels) != 0:
        day_new = datetime.strptime(graph_pixels[i], "%Y%m%d")
        day_bef = datetime.strptime(graph_pixels[i-1], "%Y%m%d")
        if day_new - day_bef == timedelta(days=1):
            graph_pixels.pop()
            streak_number += 1
            i -= 1
            # print(day_new)
        else:
            streak_going = False
            # cache_to_dir(graph_type,streak_latest_day, streak_number)
    return streak_latest_day, streak_number
# just enter the graph name
def calculate(endpoint):
    yesterday = datetime.strftime(datetime.today()-timedelta(days=1) , "%Y%m%d")
    try:
        pixels, streak_before = get_pixels(endpoint, list(streaks[endpoint].keys())[0])
    except KeyError:
        pixels, streak_before = get_pixels(endpoint, None)
    streak_day, streak_number = streak_counter(pixels, streak_before)
    return streak_number, streak_day
def daily_run():
    code_streak, code_day = calculate("code")
    math_streak, math_day = calculate("math")
    study_streak, study_day = calculate("study")
    streaks = {"study":{study_day:study_streak}, "code":{code_day:code_streak},"math":{math_day:math_streak}}


    with open("streaks.json","w") as f:
        json.dump(streaks,f, indent=4)


if __name__ == "__main__":
    daily_run()
