from trueskill import setup, Rating, rate_1vs1
from sets import Set
from collections import deque
import argparse

class Team(object):
    def __init__(self, name):
        self.name    = name
        self.rating  = Rating()
        self.events  = Set()

def find_team(name, teams):
    for team in teams:
        if team.name == name:
            return team
    else:
        return None

def process(filename, format):
    setup(draw_probability=0.0)

    teams = []
    recent = deque()

    delim = ""
    if format:
        delim = "|"

    file = open(filename, "r")
    for line in file:
        line = line.strip().split(',')

        date      = line[0]
        win_color = line[3]
        gold_name = line[4]
        blue_name = line[5]

        if date not in recent:
            recent.append(date)
            if len(recent) > 6:
                recent.popleft()

        gold_team = find_team(gold_name, teams)
        if gold_team == None:
            gold_team = Team(gold_name)
            teams.append(gold_team)

        blue_team = find_team(blue_name, teams)
        if blue_team == None:
            blue_team = Team(blue_name)
            teams.append(blue_team)

        gold_team.events.add(date)
        blue_team.events.add(date)

        if win_color == "GOLD":
            gold_team.rating, blue_team.rating = rate_1vs1(gold_team.rating, blue_team.rating)
        elif win_color == "BLUE":
            blue_team.rating, gold_team.rating = rate_1vs1(blue_team.rating, gold_team.rating)

    teams.sort(key=lambda x: x.rating.mu, reverse=True)

    if format:
        print "**Recent**\n"
        print "|Rating|Team|"
        print "|------|----|"

    for team in teams:
        if len(team.events.intersection(recent)) >= 2:
            print("{0:s}{1:.5f} {2:s}{3:s} {4:s}".format(delim, team.rating.mu, delim, team.name, delim))

    print
    if format:
        print "**All Time**\n"
        print "|Rating|Team|"
        print "|------|----|"

    for team in teams:
        if len(team.events) >= 5:
            print("{0:s}{1:.5f} {2:s}{3:s} {4:s}".format(delim, team.rating.mu, delim, team.name, delim))


def main():
    parser = argparse.ArgumentParser(description="Determine teams' skill based on match results")
    parser.add_argument('--format', action='store_true', help="Format output for markdown")
    parser.add_argument('filename', help="File containing match results")

    args = parser.parse_args()
    process(args.filename, args.format)

if __name__ == '__main__':
    main()
