# Author: Jason Taylor 2019
# Copyright (c) Jason Taylor.

import os
import sys
import time
import subprocess
from collections import namedtuple

Match = namedtuple('Match', ['player1', 'player2'])


class Data:
    def __init__(self, wins, draws, losses):
        self.wins = wins
        self.draws = draws
        self.losses = losses

    def calculate_points(self):
        return self.wins * 2 + self.draws;


def write_data_file(data_to_write):
    data_file = open("data.txt", "w")
    for key, val in data_to_write.items():
        data_file.write(key + " " + str(val.wins) + " " + str(val.draws) + " " + str(val.losses) + "\n")
    data_file.close()


def read_data_file():
    data_from_file = dict()
    data_file = open("data.txt", "r")
    lines = data_file.readlines()
    data_file.close()
    for line in lines:
        splits = line.split(' ')
        data_from_file[splits[0]] = Data(int(splits[1]), int(splits[2]), int(splits[3]))
    return data_from_file


def generate_results_html(results):
    above_html = """
 <!DOCTYPE html>
<html>
  <header>
      <meta http-equiv="refresh" content="5">
  </header>
  <head>
    <meta charset="utf-8">
    <link href="minimal-table.css" rel="stylesheet" type="text/css">
  </head>
  <body>
    <center>
    <h1>Battle Bots Results</h1>
    <table>
        <caption>Points: (2 points for a win, 1 point for draw, 0 for loss)</caption>
        <tr>
          <th scope="col">NAME</th>
          <th scope="col">POINTS</th>
          <th scope="col">WINS</th>
          <th scope="col">DRAWS</th>
          <th scope="col">LOSSES</th>
        </tr>
      <tbody>
    """
    below_html = """
      </tbody>
    </table>
    </center>
  </body>
</html>
    """
    results_file = open("results.html", "w")
    results_file.write(above_html + "\n")
    for key, val in results.items():
        str = "<tr><th score=\"row\">%s</th><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr>" % \
              (key, val.calculate_points(), val.wins, val.draws, val.losses)
        results_file.write(str + "\n")

    results_file.write(below_html + "\n")
    results_file.close()


bots = []
for f in os.listdir("./bots"):
    if os.path.isdir(f) is not True and not f.startswith(".") and not f.endswith(".png"):
        name, ext = os.path.splitext(f)
        bots.append(name)
bots.sort()

matches = []
match_number = 1
for i in range(0, len(bots)):
    first_bot = bots[i]
    for j in range(i+1, len(bots)):
        second_bot = bots[j]
        matches.append(Match(first_bot, second_bot))
        match_number += 1
        matches.append(Match(second_bot, first_bot))
        match_number += 1

data = dict()
for bot in bots:
    data[bot] = Data(0, 0, 0)

skip = 0
if len(sys.argv) == 2:
    data = read_data_file()
    skip = int(sys.argv[1])

matches_completed = 0
for match in matches:
    if skip > 0:
        skip -= 1
        matches_completed += 1
        continue

    print("Match " + str(matches_completed + 1) + ": " + match.player1 + " vs " + match.player2)
    ecode = subprocess.call(["python", "battlebots.py", "bots." + match.player1, "bots." + match.player2],
                            stdout=subprocess.DEVNULL)
    if ecode == 1:  # Player 1 wins
        print(match.player1 + " wins")
        data[match.player1].wins += 1
        data[match.player2].losses += 1
    elif ecode == 2:  # Player 2 wins
        print(match.player2 + " wins")
        data[match.player2].wins += 1
        data[match.player1].losses += 1
    elif ecode == 3:  # Draw
        print("draw")
        data[match.player1].draws += 1
        data[match.player2].draws += 1

    write_data_file(data)
    generate_results_html(data)
    time.sleep(3)
    matches_completed += 1

print("Done, completed " + str(matches_completed) + " matches.")
