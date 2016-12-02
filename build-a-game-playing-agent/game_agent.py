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
        self.TIMER_THRESHOLD = 10  # time (in ms) to leave on the clock when terminating search

    def get_move(self, game, legal_moves, time_left):

        self.time_left = time_left

        if (-1, -1) in legal_moves:
            return -1, -1

        self.is_player1 = game.get_active_player() is game.__player_1__

        if self.is_player1:
            reflect_move = self.reflective_move(game.get_last_move_for_player(game.__player_2__), legal_moves)
            if reflect_move != -1:
                return reflect_move
        else:
            reflect_move = self.reflective_move(game.get_last_move_for_player(game.__player_1__), legal_moves)
            if reflect_move != -1:
                return reflect_move
            avoid_reflection_move = self.non_reflective_move(legal_moves)
            if avoid_reflection_move != -1:
                return avoid_reflection_move

        try:
            best_move, utility = self.alphabeta(game, time_left, self.search_depth)
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
            score = self.maxvalue(gamestate, depth, self.time_left(), maximizing_player)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move

    def maxvalue(self, gamestate, depth, timeleft, maximizing_player):
        if depth == 0 or timeleft() < 500 or gamestate.is_winner(self) or gamestate.is_opponent_winner(self):
            return gamestate.utility(gamestate, maximizing_player)

        moves = gamestate.get_legal_moves()
        best_score = float('-inf')
        for move in moves:
            gamestate = gamestate.forecast_move(move)
            score = self.minvalue(gamestate, depth - 1, timeleft, False)
            if score > best_score:
                best_score = score
        return best_score

    def minvalue(self, gamestate, depth, timeleft, maximizing_player):
        if depth == 0 or timeleft() < 500 or gamestate.is_winner(self) or gamestate.is_opponent_winner(self):
            return gamestate.utility(gamestate, maximizing_player)

        moves = gamestate.get_legal_moves()
        best_score = float('inf')
        for move in moves:
            gamestate = gamestate.forecast_move(move)
            score = self.maxvalue(gamestate, depth - 1, timeleft, True)
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
            score = self.alphabeta_maxvalue(game, depth, self.time_left(), alpha, beta, maximizing_player)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move

    def alphabeta_maxvalue(self, gamestate, depth, time_left, alpha, beta, maximizing_player):
        if depth == 0 or time_left() < 500 or gamestate.is_winner(self) or gamestate.is_opponent_winner(self):
            return gamestate.utility(gamestate, maximizing_player)

        moves = gamestate.get_legal_moves()
        for move in moves:
            gamestate = gamestate.forecast_move(move)
            score = self.alphabeta_minvalue(gamestate, depth - 1, time_left, alpha, beta, False)
            if score >= beta:
                return score
            alpha = max(alpha, score)

        return score

    def alphabeta_minvalue(self, gamestate, depth, time_left, alpha, beta, maximizing_player):
        if depth == 0 or time_left() < 500 or gamestate.is_winner(self) or gamestate.is_opponent_winner(self):
            return gamestate.utility(gamestate, maximizing_player)

        moves = gamestate.get_legal_moves()
        for move in moves:
            gamestate = gamestate.forecast_move(move)
            score = self.alphabeta_minvalue(gamestate, depth - 1, time_left, alpha, beta, True)
            if score <= alpha:
                return score
            beta = min(beta, score)

        return score

    @staticmethod
    def non_reflective_move(legal_moves):
        if (0, 1) in legal_moves:
            return 0, 1
        elif (1, 0) in legal_moves:
            return 1, 0
        elif (0, 3) in legal_moves:
            return 0, 3
        elif (3, 0) in legal_moves:
            return 3, 0
        elif (1, 4) in legal_moves:
            return 1, 4
        elif (4, 1) in legal_moves:
            return 4, 1
        elif (3, 4) in legal_moves:
            return 3, 4
        elif (4, 3) in legal_moves:
            return 4, 3
        else:
            return -1

    @staticmethod
    def reflective_move(lastmove, legal_moves):
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

    def utility(self, game, maximizing_player):

        if game.is_winner(self):
            return float("inf")

        if game.is_opponent_winner(self):
            return float("-inf")

        return self.eval_fn.score(game, maximizing_player)