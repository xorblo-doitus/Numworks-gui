import sys, requests
from typing import Literal


def get(URL: str) -> None:
	response = requests.get(URL)
	
	if response.status_code < 200 or 300 <= response.status_code :
		print("Error " + str(response) + ": " + URL + ": ")
		return
	
	splits: list[str] = URL.split("?")[0].split("/")
	target_path: str = splits[-2] + "/" + splits[-1]
	
	with open(target_path, "w", encoding="utf-8") as file:
		file.write(response.text)


with open("dependencies.txt", "r", encoding="utf-8") as file:
	for line in file:
		get(line)
		if "minified" in line:
			get(line.replace("minified", "src"))
		else:
			get(line.replace("src", "minified"))