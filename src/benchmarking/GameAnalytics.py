import json
from collections import defaultdict

import matplotlib.pyplot as plt
import os

import numpy as np


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
        expanded_states_per_depth = defaultdict(list)
        average_time_per_depth = defaultdict(list)

        for game in self.data['games']:
            for player in game['players']:
                depth = player['max_depth']
                expanded_states_per_depth[depth].append(player['expanded_states'])
                average_time_per_depth[depth].append(player['average_time_per_action'])

        # Calculate average expanded states and time per depth
        avg_expanded_states = {depth: np.mean(states) for depth, states in expanded_states_per_depth.items()}
        avg_time_per_action = {depth: np.mean(times) for depth, times in average_time_per_depth.items()}

        # Sort depths for consistent plotting
        sorted_depths = sorted(avg_expanded_states.keys())
        avg_states = [avg_expanded_states[depth] for depth in sorted_depths]
        avg_times = [avg_time_per_action[depth] for depth in sorted_depths]

        # Plotting
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Expanded states
        color = 'tab:blue'
        ax1.set_xlabel('Max Depth')
        ax1.set_ylabel('Average Expanded States', color=color)
        bars = ax1.bar(sorted_depths, avg_states, color='skyblue', label='Expanded States')
        ax1.tick_params(axis='y', labelcolor=color)

        # Highlight the bar for depth 6
        for bar, depth in zip(bars, sorted_depths):
            if depth == 6:
                bar.set_color('lightgreen')  # Highlight depth 6
                ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), 'Winner', ha='center', va='bottom')

        # Average time per action
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Average Time per Action (s)', color=color)
        ax2.plot(sorted_depths, avg_times, color=color, marker='o', label='Time per Action')
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()
        plt.title('Game Depth Analysis: Expanded States and Time per Action')
        plt.savefig('game_depth_analysis.jpg', format='jpg', dpi=300)
        plt.show()