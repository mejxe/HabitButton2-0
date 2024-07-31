import os
import requests
from datetime import datetime, timedelta
import json
from api_comms import Pixela
token = os.environ.get("token")
headers = {
            "X-USER-TOKEN": token
        }
endpoints = {"study": "https://pixe.la/v1/users/mejxe/graphs/studygraph/pixels",
                   "math": "https://pixe.la/v1/users/mejxe/graphs/mathgraph/pixels",
                   "code": "https://pixe.la/v1/users/mejxe/graphs/codegraph/pixels",
             "japan":"https://pixe.la/v1/users/mejxe/graphs/japgrah/pixels"}


# get the streaks from the cache file
do_not_check_cache = False
try:
    with open("streaks.json","r") as st:
        if not not st.read():
            st.seek(0)
            streaks = json.load(st)
        else:
            do_not_check_cache = True
            streaks = {"study":[],"code":[],"math":[], "japan":[]}
except FileNotFoundError:
    do_not_check_cache = True
    streaks = {"study":[], "code": [], "math": [], "japan":[]}



def get_pixels(endpoint:str, start_from: str or None) -> tuple:
    if start_from is not None:
        pars = {"from": start_from,
                "withBody":"true"}
        req = requests.get(endpoints[endpoint], headers=headers, params=pars)
    else:
        req = requests.get(f"{endpoints[endpoint]}?withBody=true", headers=headers)
    # print(req.json(), req.url)
    return req.json()["pixels"]


# def cache_to_dir(type: str, streak_latest_day: str, streak_number: int):
#     streaks[type][streak_latest_day] = streak_number
#     print(streaks)


# def streak_counter(graph_pixels: list, streak_before:int = 0) -> tuple:
#     if datetime.strftime(datetime.today()- timedelta(days=1), "%Y%m%d") not in graph_pixels:
#         return datetime.strftime(datetime.today() - timedelta(days=1), "%Y%m%d"), 0
#     streak_going = True
#     i: int = len(graph_pixels) - 1
#     streak_number: int = 1 + streak_before
#     if streak_before != 0:
#         streak_number -= 1
#     streak_latest_day = graph_pixels[i]
#     while streak_going and len(graph_pixels) != 0:
#         day_new = datetime.strptime(graph_pixels[i], "%Y%m%d")
#         day_bef = datetime.strptime(graph_pixels[i-1], "%Y%m%d")
#         if day_new - day_bef == timedelta(days=1):
#             graph_pixels.pop()
#             streak_number += 1
#             i -= 1
#             # print(day_new)
#         else:
#             streak_going = False
#             # cache_to_dir(graph_type,streak_latest_day, streak_number)
#     return streak_latest_day, streak_number
def streak_counter(pixels):
    streak = 0
    date = pixels[-1]["date"]
    for i in range(len(pixels)-1,-1,-1):
        previous_date = datetime.strptime(pixels[i-1]["date"],"%Y%m%d")
        curr_date = datetime.strptime(pixels[i]["date"],"%Y%m%d")
        if curr_date - timedelta(days=1) != previous_date or pixels[i-1]["quantity"] == "0":
            if streak != 0:
                streak+=1
                date = pixels[i]["date"]
            return streak, date
        else:
            streak +=1
    return streak, date


# just enter the graph name
# def calculate(endpoint):
#     if not do_not_check_cache:
#         yesterday = (datetime.today()-timedelta(days=1)).date()
#         stored_date = datetime.strptime(streaks[endpoint][0],"%Y%m%d").date()
#         if yesterday != (stored_date - timedelta(days=1)):
#             streak = streaks[endpoint][1] + 1
#             stored_date = stored_date + timedelta(days=1)
#         else:
#             pixels = get_pixels(endpoint, None)
#             streak, stored_date = streak_counter(pixels)
#     else:
#         pixels = get_pixels(endpoint, None)
#         streak, stored_date = streak_counter(pixels)
#     return streak, stored_date
def calculate(endpoint):
    pixels = get_pixels(endpoint, None)
    streak, _ = streak_counter(pixels)
    return streak, datetime.strftime(datetime.today().date(),"%Y%m%d")

def daily_run():
    # for i in endpoints:
    #     ns = Pixela(graph_endpoint=endpoints[i], graph_name=i)
    #     ns.create_pixel()
    code_streak, code_day = calculate("code")
    math_streak, math_day = calculate("math")
    study_streak, study_day = calculate("study")
    jap_streak, jap_day = calculate("japan")
    streaks = {"study":[study_day,study_streak], "code":[code_day,code_streak],"math":[math_day,math_streak], "japan":[jap_day,jap_streak]}


    with open("streaks.json","w") as f:
        json.dump(streaks,f, indent=0)

def test():
    # streak, day_before = get_pixels("japan", None)
    # print(streak_counter(streak,day_before))
    calculate("study")



if __name__ == "__main__":
    daily_run()
