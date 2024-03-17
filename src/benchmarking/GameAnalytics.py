import json
import matplotlib.pyplot as plt


class GameAnalytics:
    def __init__(self, filename='game_data.json'):
        self.data = {'games': []}
        self.filename = filename
        self.load_existing_data()

    def load_existing_data(self):
        try:
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def add_game_data(self, game_duration, total_turns, players):
        players_data = []
        for i, player in enumerate(players):
            player_dict = player.to_dict()
            player_dict['player_id'] = i + 1
            players_data.append(player_dict)

        existing_game_index = None
        for index, existing_game in enumerate(self.data['games']):
            existing_players = existing_game['players']
            if all(player['player_type'] == new_player['player_type'] and
                   player['max_depth'] == new_player['max_depth']
                   for player, new_player in zip(existing_players, players_data)):
                existing_game_index = index
                break

        game_data = {
            'game_duration': game_duration,
            'total_turns': total_turns,
            'players': players_data
        }

        if existing_game_index is not None:
            self.data['games'][existing_game_index] = game_data
        else:
            self.data['games'].append(game_data)

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

    def plot_average_time_per_action(self):
        for game in self.data['games']:
            player_ids = [player['player_id'] for player in game['players']]
            average_times = [player['average_time_per_action'] for player in game['players']]

            plt.figure(figsize=(10, 6))
            plt.bar(player_ids, average_times, color='skyblue')
            plt.xlabel('Player ID')
            plt.ylabel('Average Time per Action (s)')
            plt.title('Average Time per Action for Each Player')
            plt.xticks(player_ids)
            plt.show()
