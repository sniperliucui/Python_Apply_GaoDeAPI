# -*- coding: utf-8 -*-

"""
@author: liu cui
@software: PyCharm
@file: 高德API.py
@time: 2021/1/5 15:59
"""

from pprint import pprint
import requests
import json
import pandas as pd
import time
import warnings

start = time.time()


def getlntlat(cityName):
    key = "f939ebb07272452ce577174ccf20ff79"
    url = "https://restapi.amap.com/v3/geocode/geo?parameters"
    parameters = {"key": key,
                  "address": cityName}
    res = requests.get(url=url, params=parameters)
    json_data = json.loads(res.text)
    # pprint(json_data)
    if (json_data["geocodes"] != []) and (json_data["geocodes"][0]["city"] != []):
        return json_data["geocodes"][0]["province"], cityName, json_data["geocodes"][0]["location"]
    else:
        return 0


def parse():
    input_path = "./dataset/china_city_list.csv"  # 输入城市名：上海市
    cityNames = []
    df = pd.read_csv(input_path, encoding="gbk")
    for i in df.values:
        b = i[1]
        cityNames.append(b)
    return cityNames


def output_data():
    i = 0
    df = pd.DataFrame(columns=['province', 'city', 'lng', 'lat'])
    cityNames = parse()
    for cityName in cityNames:
        if getlntlat(cityName) != 0:
            province, city, location = getlntlat(cityName)
            df.loc[i] = [province, city, float(location.split(',')[0]), float(location.split(',')[1])]
        i = i + 1
    df.to_csv("./dataset/city_lntlat_gaode.csv", encoding="gbk")


if __name__ == '__main__':

    output_data()
    print("Success!!!")

    end = time.time()
    print("Running Time is %f" % (end - start))

