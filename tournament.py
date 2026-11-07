import csv
import json
import os
import random


class Team:
    

    def __init__(self, sponsor, budget):
        self.sponsor = sponsor      
        self.budget = budget        
        self.inventory = []        

    @property
    def score(self):
        
        # TODO: add up car["MPG-H"] for every car in self.inventory
        pass

    def buy_cars(self, available_cars):
        
        # TODO:
        # 1. sort available_cars by value per cost (MPG-H / Price), best first
        # 2. go down the list; if the car fits in self.budget and hasn't been
        #    bought in THIS purchase, add it to self.inventory and subtract its price
        # 3. decide what counts as a "duplicate" (same row? same Make + Model?)
        pass

    def __str__(self):
        # Must match the example output, e.g.
        # "Team sponsored by Nissan with $32000 available and 32 cars and a score of 1032"
        # TODO: build this string from the team's attributes
        pass


class Tournament:
    

    def __init__(self, config_path="./data/configTEST.json"):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, "r") as config_file:
            config = json.load(config_file)

        self.name = config["name"]
        self.car_data_path = config["path"]
        self.nteams = config["nteams"]
        self.default_low = config["default_low"]
        self.default_high = config["default_high"]
        self.default_incr = config["default_incr"]
        self.prize = config["prize"]

        self._validate_config()

        self.cars = self._load_cars()
        self.teams = []         
        self.rounds = []         
        self.champion = None     

    def _validate_config(self):
        if self.nteams < 2 or self.nteams & (self.nteams - 1) != 0:
            raise ValueError("The amount of teams must be a mutiple of two)")

        # TODO: more checks, e.g.
        # - car data file exists
        # - default_low, default_high, default_incr, prize are positive numbers
        # - default_low <= default_high
        # - enough distinct budget values in the range for every team
        #   (hint: len(range(default_low, default_high + 1, default_incr)))
        pass

    def _load_cars(self):
        """Read the car CSV into a list of dicts"""
        # TODO:
        # - open self.car_data_path with csv.DictReader
        
        with open(self.car_data_path, newline="") as car_file:
            cars = list(csv.DictReader(car_file))

        for row_number, car in enumerate(cars, start=2):  
            try:
                car["MPG-H"] = int(car["MPG-H"])
                car["Price"] = int(car["Price"])
            except (KeyError, ValueError):
                raise ValueError(f"Bad MPG-H or Price on row {row_number} of {self.car_data_path}")

        # - convert "MPG-H" and "Price" to int
        # - return the list of rows
        # (after loading: check there are at least nteams different Makes)
        pass

    def generate_sponsors_and_teams_with_inventory(self):
        """Create nteams teams, each with a unique random sponsor and budget,
        and buy each team's starting inventory."""
        # TODO:
        # 1. get the list of distinct Makes; random.sample nteams of them
        # 2. random.sample nteams distinct budgets from the range
        # 3. create a Team for each pair, call team.buy_cars(<that sponsor's cars>)
        # 4. store them in self.teams
        pass

    def _play_match(self, team_a, team_b):
        """Return the winner of one match (higher score wins)."""
        # TODO: compare scores; decide and document a tie-break rule
        pass

    def hold_event(self):
        """Play every round until one team is left, then set self.champion."""
        # TODO:
        # while more than one team remains:
        #   - pair up the remaining teams (1 v 2, 3 v 4, ...)
        #   - play each match with _play_match
        #   - winner: budget += self.prize, then buy_cars again
        #   - record the round in self.rounds (for show_win_record)
        # the last team left is self.champion
        pass

    def show_win_record(self):
        """Print the tournament bracket (see the example in the notebook)."""
       
        pass
