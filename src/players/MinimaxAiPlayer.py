import GameProblem

from State import State
from Action import Action
from players.Player import Player


class MinimaxAIPlayer(Player):
    def get_action(self, problem: GameProblem, state: State) -> Action:
        return self.minimax_decision(state)

    @staticmethod
    def minimax(prob: GameProblem, state: State, depth: int, alpha: float, beta: float, max_player: int):
        """
        Minimax algorithm with alpha-beta pruning
        :param prob: formal definition of a Game Problem
        :param state:
        :param depth:
        :param alpha:
        :param beta:
        :param max_player:
        :return:
        """
        if depth == 0 or prob.terminal_test(state):
            return state, prob.utility(state, max_player)

        if max_player:
            max_eval = float('-inf')
            best_action = None
            for action in prob.actions(state):
                child = prob.result(state, action)
                evl, _ = MinimaxAIPlayer.minimax(prob, child, depth - 1, alpha, beta, False)
                if evl > max_eval:
                    max_eval = evl
                    best_action = action
                alpha = max(alpha, evl)
                if beta <= alpha:
                    break
            return max_eval, best_action

        else:
            min_eval = float('inf')
            best_action = None
            for action in prob.actions(state):
                child = prob.result(state, action)
                evl, _ = MinimaxAIPlayer.minimax(prob, child, depth - 1, alpha, beta, True)
                if evl < min_eval:
                    min_eval = evl
                    best_action = action
                beta = min(beta, evl)
                if beta <= alpha:
                    break
            return min_eval, best_action
