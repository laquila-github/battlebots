# Author: Jason Taylor 2019
# Copyright (c) Jason Taylor.

import sys
import subprocess
from collections import namedtuple

Match = namedtuple('Match', ['player1', 'player2'])

if len(sys.argv) != 4:
    print("Invalid arguments!")
    print("Usage: bestofnmatches.py <player1bot> <player2bot> number_of_matches")
    exit(0)

player1 = sys.argv[1]
player2 = sys.argv[2]
number_of_matches = int(sys.argv[3])

matches = []
for i in range(1, number_of_matches+1):
    if i % 2 == 0:
        matches.append(Match(player1, player2))
    else:
        matches.append(Match(player2, player1))

player_1_wins = 0
player_2_wins = 0
draws = 0
for match in matches:
    ecode = subprocess.call(["python", "battlebots.py", match.player1, match.player2], stdout=subprocess.DEVNULL)
    if ecode == 1:  # Player 1 wins
        print(match.player1 + " wins")
        if match.player1 == player1:
            player_1_wins += 1
        else:
            player_2_wins += 1
    elif ecode == 2:  # Player 2 wins
        print(match.player2 + " wins")
        if match.player2 == player2:
            player_2_wins += 1
        else:
            player_1_wins += 1
    elif ecode == 3:  # Draw
        print("draw")
        draws += 1

print("Results - %s wins: %d, %s wins: %d, Draws: %d" % (player1, player_1_wins, player2, player_2_wins, draws))
