import json
import matplotlib.pyplot as plt
import os


class GameAnalytics:
    def __init__(self, filename='game_data.json'):
        self.filename = filename
        if os.path.exists(self.filename):
            self.data = self.load_from_file(self.filename)
        else:
            self.data = {'games': []}

    def load_existing_data(self):
        try:
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {'games': []}

    def add_game_data(self, game_duration, total_turns, players, winner):
        players_data = []
        for i, player in enumerate(players):
            player_dict = player.to_dict()
            player_dict['player_id'] = i + 1  # Assign player ID based on enumeration
            players_data.append(player_dict)

        game_data = {
            'game_duration': game_duration,
            'total_turns': total_turns,
            'players': players_data,
            'winner': winner
        }
        self.data['games'].append(game_data)
        self.save_to_file()

    def print_game_data(self):
        if not self.data['games']:
            print("No games have been recorded.")
            return

        # Access the most recent game's data
        game = self.data['games'][-1]

        print('Most Recent Game:')
        print(f"Game elapsed time: {game['game_duration']:0.8f} | Turns = {game['total_turns']}")
        for i, player_data in enumerate(game['players']):
            print('-----')
            print(f"Player {player_data['player_id']} average time: {player_data['average_time_per_action']:0.8f}")
            print(f"Player {player_data['player_id']} move count: {player_data['move_count']}")
            print(f"Player {player_data['player_id']} move count: {player_data['move_count']}")
            if 'expanded_states' in player_data:
                print(f"Player {player_data['player_id']} expanded states: {player_data['expanded_states']}")
        print('\n')

    def save_to_file(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'r') as file:
            return json.load(file)

    def plot(self):
        # TODO: Plot valuable data
        return
