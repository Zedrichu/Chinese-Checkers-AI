from src.State import State
from src.Action import Action
from src.PlayerInterface import PlayerInterface
from src.ChineseCheckers import ChineseCheckers


class MinimaxAI(PlayerInterface):
    def __init__(self, player_id: int):
        super().__init__(player_id)

    def get_action(self, state: State) -> Action:
        return self.minimax_decision(state)

    @staticmethod
    def minimax(state, depth, alpha, beta, max_player):
        """
        Minimax algorithm with alpha-beta pruning
        :param state:
        :param depth:
        :param alpha:
        :param beta:
        :param max_player:
        :return:
        """
        if depth == 0 or ChineseCheckers.terminal_test(state):
            return state, ChineseCheckers.utility(state, max_player)

        if max_player:
            max_eval = float('-inf')
            for action in ChineseCheckers.actions(state):
                child = ChineseCheckers.result(state, action)
                evl = MinimaxAI.minimax(child, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, evl)
                alpha = max(alpha, evl)
                if beta <= alpha:
                    break
            return max_eval

        else:
            min_eval = float('inf')
            for action in ChineseCheckers.actions(state):
                child = ChineseCheckers.result(state, action)
                evl = MinimaxAI.minimax(child, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, evl)
                beta = min(beta, evl)
                if beta <= alpha:
                    break
            return min_eval
