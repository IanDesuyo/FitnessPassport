import requests
import time
from bs4 import BeautifulSoup


# SETTINGS
YEAR = 2020
START_MONTH = 8
END_MONTH = 12
ID = "A123456789"
PASSWORD = "1"

def SportTime(PID, SITNO):
    session = requests.session()
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    }
    # get VIEWSTATE & EVENTVALIDATION
    r = session.get("https://passport.fitness.org.tw/nlogin.aspx", headers=header, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    VIEWSTATE = soup.find(id="__VIEWSTATE")["value"]
    EVENTVALIDATION = soup.find(id="__EVENTVALIDATION")["value"]
    # login
    data = {
        "txtST_PID": PID,
        "txtST_SITNO": SITNO,
        "__VIEWSTATE": VIEWSTATE,
        "__EVENTVALIDATION": EVENTVALIDATION,
        "btnSave.x": 1,
        "btnSave.y": 1,
    }
    r = session.post("https://passport.fitness.org.tw/nlogin.aspx", data=data, headers=header, verify=False)
    # loop
    for i in range(START_MONTH, END_MONTH + 1):
        for j in range(1, 32):
            data = {
                "sport_save_year": YEAR,
                "sport_save_month": i,
                "sport_save_day": j,
                "sport_save_time": 90,
                "sport_ac_action": "S",
                "sport_save_coin": "Y",
            }
            r = session.post("https://passport.fitness.org.tw/sport.passport.ashx", data=data, headers=header, verify=False)
            print(f"{i}/{j}: {r.text}")
            time.sleep(0.05)

SportTime(ID, PASSWORD)
