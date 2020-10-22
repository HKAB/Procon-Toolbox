import requests
import sys
import json
from subprocess import PIPE
import subprocess
import time

# http://sv-procon.uet.vnu.edu.vn:3000/matches/268
# curl -H 'Authorization: TOKEN' -H 'Content-Type: application/json' -X GET http://sv-procon.uet.vnu.edu.vn:8888/matches


SERVER = "http://sv-procon.uet.vnu.edu.vn:8888"
MATCH_ID = 9
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoicGxhbnkiLCJpYXQiOjE2MDMzMzIyMTEsImV4cCI6MTYwMzQxODYxMX0.hnAT5-pkxxmQOtJFHv9HMEXwX5HGL4T9IcxRrpvCD1o"
TEAMID = 28
MAX_TURN = 100

last_turn = -1000
current_turn = 0;

while (last_turn < MAX_TURN):
	r = requests.get(SERVER + "/matches/" + str(MATCH_ID), headers={"Authorization": TOKEN})
	# print(r.json())
	if (r.status_code == requests.codes.ok):
		data = r.json()
		if (data["startedAtUnixTime"] > 0):
			current_turn = data["turn"]
		# with open("test.json", "r") as f:
			# data = (json.load(f))
			if (last_turn < current_turn):
				print("---Turn " + str(current_turn) +"---\nConstruct board.txt....\n")
				s = str(data["width"]) + " " + str(data["height"]) + " " + str(TEAMID) + "\n"
				for x in range(0, len(data["points"])):
					for y in range(0, len(data["points"][0])):
						s = s + str(data["points"][x][y]) + " "
					s = s + "\n"
				for x in range(0, len(data["tiled"])):
					for y in range(0, len(data["tiled"][0])):
						s = s + str(data["tiled"][x][y]) + " "
					s = s + "\n"
				s = s + str(len(data["teams"][0]["agents"])) + "\n"
				if data["teams"][0]['teamID'] == TEAMID:
					for x in range(0, len(data["teams"][0]['agents'])):
						s = s + str(data["teams"][0]['agents'][x]['agentID']) + " " + str(data["teams"][0]['agents'][x]['x']) + " " + str(data["teams"][0]['agents'][x]['y']) + "\n"
					for x in range(0, len(data["teams"][1]['agents'])):
						s = s + str(data["teams"][1]['agents'][x]['x']) + " " + str(data["teams"][1]['agents'][x]['y']) + "\n"
				else:
					for x in range(0, len(data["teams"][1]['agents'])):
						s = s + str(data["teams"][1]['agents'][x]['agentID']) + " " + str(data["teams"][1]['agents'][x]['x']) + " " + str(data["teams"][1]['agents'][x]['y']) + "\n"
					for x in range(0, len(data["teams"][0]['agents'])):
						s = s + str(data["teams"][0]['agents'][x]['x']) + " " + str(data["teams"][0]['agents'][x]['y']) + "\n"

				s = s + str(len(data["obstacles"])) + "\n"
				for obstacle in data["obstacles"]:
					s = s + str(obstacle['x']) + " " + str(obstacle['y']) + "\n"

				s = s + str(len(data["treasure"])) + "\n"						
				for treasure in data["treasure"]:
					s = s + str(treasure['x']) + " " + str(treasure['y']) + " " + str(treasure['point']) + " " + str(treasure['status']) + "\n"

				with open("board.txt", "w") as f:
					f.write(s)

				print("Running algorithm....\n")
				json_string = json.loads(subprocess.run("./main", stdout=PIPE, stderr=PIPE).stdout);
				print(json_string)
				print("Sent JSON above....")
				headers = {'Content-type': 'application/json', "Authorization": TOKEN}
				r = requests.post(SERVER + "/matches/" + str(MATCH_ID) + "/action", headers=headers, json=json_string)
				if (r.status_code == requests.codes.ok):
					print("Done! Waiting for next turn...\n")
					last_turn = current_turn
				else:
					print(r.status_code)
			else:
				print("Time passing by....\n")
				time.sleep(2)
		else:
			print("Match does not start..\n");
			time.sleep(1);
	else:
		time.sleep(1)
	# print(json_string)


# print(data["points"][1][1])
# print(data)

