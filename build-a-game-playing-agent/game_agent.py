"""
This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using run_tournament.py and include the results in your
report.
"""


class Timeout(Exception):
    """ Subclass base exception for code clarity. """
    pass


class CustomEval():
    """
    Custom evaluation function that acts however you think it should.
    """
    @staticmethod
    def score(game, maximizing_player):

        if maximizing_player:
            eval_fn = game.get_legal_moves().__len__()
        else:
            eval_fn = game.get_opponent_moves().__len__()
        return eval_fn


class CustomPlayer():

    def __init__(self, search_depth=3, eval_fn=CustomEval(), iterative=False, method='minimax'):
        """
        You MAY modify this function, but the interface must remain compatible
        with the version provided.
        """
        self.eval_fn = eval_fn
        self.search_depth = search_depth
        self.iterative = iterative
        self.method = method
        self.time_left = None
        self.is_player1 = False
        self.MINIMAX = 'minimax'
        self.ALPHABETA = 'alphabeta'
        self.TIMER_THRESHOLD = 10  # time (in ms) to leave on the clock when terminating search

    def get_move(self, game, legal_moves, time_left):

        self.is_player1 = game.get_active_player() is game.__player_1__

        if self.is_player1:
            reflect_move = self.reflecting_move(game.get_last_move_for_player(game.__player_2__), legal_moves)
            if reflect_move != -1:
                return reflect_move
        else:
            reflect_move = self.reflecting_move(game.get_last_move_for_player(game.__player_1__), legal_moves)
            if reflect_move != -1:
                return reflect_move
            avoid_reflection_move = self.non_reflective_move(legal_moves)
            if avoid_reflection_move != -1:
                return avoid_reflection_move

        try:
            if self.method is self.ALPHABETA:
                best_move, utility = self.alphabeta(game, time_left, self.search_depth)
            else:
                best_move, utility = self.minimax(game, time_left, True)
            return best_move, utility
            pass

        except Timeout:
            pass

    def minimax(self, game, depth, maximizing_player=True):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        moves = game.get_legal_moves()
        best_move = moves[0]
        best_score = float('-inf')
        for move in moves:
            gamestate = game.forecast_move(move)
            score = self.max(gamestate, depth, self.time_left(), maximizing_player)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move

    def max(self, gamestate, depth, timeleft, maximizing_player):
        if gamestate.is_winner(self) or gamestate.is_opponent_winner(self):
            return gamestate.utility(gamestate, maximizing_player)

        moves = gamestate.get_legal_moves()
        best_score = float('-inf')
        for move in moves:
            gamestate = gamestate.forecast_move(move)
            score = self.min(gamestate, depth - 1, timeleft, False)
            if score > best_score:
                best_score = score
        return best_score

    def min(self, gamestate, depth, timeleft, maximizing_player):
        if gamestate.is_winner(self) or gamestate.is_opponent_winner(self):
            return gamestate.utility(gamestate, maximizing_player)

        moves = gamestate.get_legal_moves()
        best_score = float('inf')
        for move in moves:
            gamestate = gamestate.forecast_move(move)
            score = self.max(gamestate, depth - 1, timeleft, True)
            if score < best_score:
                best_score = score
        return best_score

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        moves = game.get_legal_moves()
        best_move = moves[0]
        best_score = float('-inf')
        for move in moves:
            game = game.forecast_move(move)
            score = self.alphabeta_max(game, depth, self.time_left(), alpha, beta, maximizing_player)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move

    def alphabeta_max(self, gamestate, depth, time_left, alpha, beta, maximizing_player):
        if gamestate.is_winner(self) or gamestate.is_opponent_winner(self):
            return gamestate.utility(gamestate, maximizing_player)

        moves = gamestate.get_legal_moves()
        for move in moves:
            gamestate = gamestate.forecast_move(move)
            score = self.alphabeta_mini(gamestate, depth - 1, time_left, alpha, beta, False)
            if score >= beta:
                return score
            alpha = max(alpha, score)

            return alpha

    def alphabeta_mini(self, gamestate, depth, time_left, alpha, beta, maximizing_player):
        if gamestate.is_winner(self) or gamestate.is_opponent_winner(self):
            return gamestate.utility(gamestate, maximizing_player)

        moves = gamestate.get_legal_moves()
        for move in moves:
            gamestate = gamestate.forecast_move(move)
            score = self.alphabeta_mini(gamestate, depth - 1, time_left, alpha, beta, True)
            if score <= alpha:
                return score
            beta = min(beta, score)

            return beta

    @staticmethod
    def non_reflective_move(legal_moves):
        if legal_moves[0] < 0 and legal_moves[1] < 0:
            return legal_moves
        else:
            return -1

    @staticmethod
    def reflecting_move(lastmove, legal_moves):
        if lastmove[0] is 0:
            x = 4
        elif lastmove[0] is 1:
            x = 3
        elif lastmove[0] is 4:
            x = 0
        elif lastmove[0] is 3:
            x = 1
        else:
            x = 2

        if lastmove[1] is 0:
            y = 4
        elif lastmove[1] is 1:
            y = 3
        elif lastmove[1] is 4:
            y = 0
        elif lastmove[1] is 3:
            y = 1
        else:
            y = 2

        reflectmove = x, y

        if reflectmove in legal_moves:
            return reflectmove
        else:
            return -1