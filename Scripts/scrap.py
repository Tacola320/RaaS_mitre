#!/usr/bin/env python
from time import sleep, time
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

column_names = ["conti", "lockbit", "alphv", "matches"]
df = pd.read_excel("<ttps_scrap>.xls", names=column_names)

lists = df['matches'].tolist()

data = {}

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1",
]

for entry in lists:
    url = f"https://attack.mitre.org/techniques/{entry}"
    print(f"Sending request to {url}")
    response = requests.get(
        url,
        allow_redirects=True,
        headers={"User-Agent": user_agents[int(time()) % len(user_agents)]},
    )
    sleep(2)
    content = response.content

    soup = BeautifulSoup(content, "html.parser")
    tactics_div = soup.find("div", attrs={"id": "card-tactics"})
    if not tactics_div:
        print(entry, "ERROR")
        continue
    tactics_a = tactics_div.find_all("a")
    tactics = [t.text for t in tactics_a]

    technique_h1 = soup.find("h1")
    techniques = technique_h1.text.strip().split(":")
    if len(techniques) > 1:
        subtechnique = techniques[1].strip()
        technique = techniques[0].strip()
    else:
        subtechnique = None
        technique = techniques[0].strip()
    data[entry] = {
        "technique": technique,
        "subtechnique": subtechnique,
        "tactics": tactics,
    }

print(data)

with open("x.csv", "w") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["t_id", "tactics", "technique", "subtechnique"])
    for t_id in data:
        csv_writer.writerow(
            [
                t_id,
                data[t_id]["tactics"],
                data[t_id]["technique"],
                data[t_id]["subtechnique"],
            ]
        )
