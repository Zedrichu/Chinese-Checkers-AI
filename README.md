# Chinese Checkers Game

This project implements a Chinese Checkers game that can be played in various modes, including against different types of AI players and a human player via a graphical user interface (GUI). The game supports command-line arguments to specify the player types and, for AI players using the Minimax algorithm, the depth of the search.

## Installation

Before running the game, ensure you have Python installed on your system. This game has been tested with Python 3.12+.

Clone the repository to your local machine:

git clone https://yourrepositorylink.git

cd chinese-checkers

## Usage

To start the game, navigate to the project directory and run `main.py` with Python, specifying the options for the first and second players.

```bash
python main.py --first-player <player_type> --second-player <player_type> [options]
```

## Player types
- `human`: A human player using the graphical user interface.
- `random`: An AI player that chooses moves randomly.
- `nonrepeatrandom`: An AI player that chooses moves randomly without repeating the last move.
- `minimax`: An AI player that uses the Minimax algorithm with optional depth specification.

## Options
- `--first-minimax-depth <depth>`: Specifies the depth of the Minimax search for the first player. Only required if the first player is minimax. Default is 6.
- `--second-minimax-depth <depth>`: Specifies the depth of the Minimax search for the second player. Only required if the second player is minimax. Default is 6.

## Examples
Start a game with a human player against a Minimax AI player with a depth of 4:
```bash
python main.py --first-player human --second-player minimax --second-minimax-depth 4
```

Start a game between a Minimax AI player with a default depth of 6 and a standard random AI player:

```bash
python main.py --first-player minimax --second-player random
```


