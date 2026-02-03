import csv
import requests
from Manjot_CollectFiles import github_auth
import os
from datetime import datetime
import json

SOURCE_FILE_EXTENSIONS = (
    ".java",
    ".kt",
    ".c",
    ".cpp",
    ".h",
)

TOKEN = [os.getenv("REPO_GITHUB_TOKEN", "0000000000000000000000000000000000000000")]
REPO = "scottyab/rootbeer"
BASE_URL = f"https://api.github.com/repos/{REPO}/commits"

data = {}
file_name_to_number = {}

file_num = 0
earliest_date = None

with open("data/file_rootbeer.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        filepath = row["Filename"].strip()
        if "/src/" not in filepath or not filepath.endswith(SOURCE_FILE_EXTENSIONS):
            continue

        page = 1
        ct = 0

        while True:
            spage = str(page)
            url = f"{BASE_URL}?path={filepath}&page={spage}&per_page=100"
            commits, ct = github_auth(url, TOKEN, ct)

            if not commits:
                break

            for commit in commits:
                author = commit["commit"]["author"]["name"]
                date = commit["commit"]["author"]["date"]

                if author not in data:
                    data[author] = []

                if filepath not in file_name_to_number:
                    file_name_to_number[filepath] = file_num
                    file_num += 1

                dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")

                if earliest_date is None or earliest_date > dt:
                    earliest_date = dt

                data[author].append([dt, file_name_to_number[filepath]])

                print(f'author: {author}, date: {date}')

            page += 1

for author in data:
    for i in range(len(data[author])):
        dt = data[author][i][0]
        data[author][i][0] = (dt - earliest_date).days // 7

with open("data/author_touches.json", "w") as f:
    json.dump(data, f)

print(data)