import os
import csv
import json
from shutil import copyfile

src_dir = "original-csvs"

for f in os.listdir(src_dir):
	filepath = os.path.join(src_dir, f)
	if not f.endswith(".csv"):
		continue
	copyfile(os.path.join(src_dir, f), os.path.join("csv", f))
	varname = os.path.splitext(os.path.basename(f))[0]

	json_year = {}
	json_state = {}
	with open(filepath, "r") as opencsv:
		reader = csv.DictReader(opencsv)

		for row in reader:
			for k, v in row.items():
				if k == "state":
					continue
				if k in json_year:
					json_year[k][row["state"]] = v
				else:
					json_year[k] = {row["state"]: v}

			json_state[row["state"]] = {k:v for k,v in row.items() if not k == "state"}

	with open(os.path.join("json", varname + ".json"), "w") as outcsv:
		json.dump(json_year, outcsv, indent=1)

	for state, data in json_state.items():
		state_dir = os.path.join("json", state).replace(" ", "-").lower()
		if not os.path.isdir(state_dir):
			os.mkdir(state_dir)
		with open(os.path.join(state_dir, varname + ".json"), "w") as ex:
			json.dump(data, ex, indent=1)
