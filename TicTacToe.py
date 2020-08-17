from random import choice


class TicTacToe:
    def __init__(self):
        self.game_over = False
        self.players = {'X': '', 'O': ''}
        self.players_moves = {'user': self.get_user_move, 'comp': self.get_ai_move}
        self.players_lvl = ['user', 'easy', 'medium', 'hard']
        self.current_move = 'X'
        self.field = [[' '] * 3 for _ in range(3)]

    def start(self):
        while True:
            init, *params = input('Input command: ').split()
            if init == 'exit':
                break
            self.__init__()
            check = self.game_params_handler(*params)
            if check:
                self.game_handler()

    def game_params_handler(self, pl1=None, pl2=None):
        if pl1 in self.players_lvl and pl2 in self.players_lvl:
            self.players['X'], self.players['O'] = pl1, pl2
            return True
        print('Bad parameters!')
        return False

    def game_handler(self):
        self.print_field()
        while not self.game_over:
            self.moves_handler(self.current_move)
            self.print_field()
            self.game_status_handler()
            self.current_move = 'O' if self.current_move == 'X' else 'X'

    def print_field(self):
        print('-' * 9)
        for row in self.field:
            print('|', *row, '|')
        print('-' * 9)

    def check_user_move(self, pos):
        if not all(spot.isdigit() for spot in pos):
            print('You should enter numbers!')
        elif not (0 < int(pos[0]) < 4) or not (0 < int(pos[1]) < 4):
            print('Coordinates should be from 1 to 3!')
        elif self.field[3 - int(pos[1])][int(pos[0]) - 1] != ' ':
            print('This cell is occupied! Choose another one!')
        else:
            return True

    def get_user_move(self):
        pos = input('Enter the coordinates: ').split()
        checked = self.check_user_move(pos)
        while not checked:
            pos = input('Enter the coordinates: ').split()
            checked = self.check_user_move(pos)
        return 3 - int(pos[1]), int(pos[0]) - 1

    def get_ai_move(self, lvl, x=None, y=None):
        print(f'Making move level "{lvl}"')
        if lvl == 'easy':
            free_cells = [(i, j) for i in range(3) for j in range(3) if self.field[i][j] == ' ']
            x, y = choice(free_cells)
        elif lvl == 'medium':
            res, x, y = self.minimax(self.current_move, 2)
        elif lvl == 'hard':
            res, x, y = self.minimax(self.current_move)
        return x, y

    def minimax(self, move, deep=None, cur_deep=0, x=None, y=None, alpha=-2, beta=2):
        free_cells = [(x, y) for x in range(3) for y in range(3) if self.field[x][y] == ' ']
        prev_move = 'O' if self.current_move == 'X' else 'X'
        init_res = 2 if prev_move == move else -2

        if self.is_winner([prev_move] * 3):
            return (1, 0, 0) if prev_move == move else (-1, 0, 0)
        if len(free_cells) == 0 or deep == cur_deep:
            return 0, 0, 0

        cur_deep += 1
        for i, j in free_cells:
            self.field[i][j] = self.current_move
            self.current_move = 'O' if self.current_move == 'X' else 'X'
            res, i_max, j_max = self.minimax(move, deep, cur_deep, alpha=alpha, beta=beta)
            self.current_move = 'O' if self.current_move == 'X' else 'X'
            self.field[i][j] = ' '
            if prev_move == move:
                if res < init_res:
                    init_res, x, y = res, i, j
                if init_res <= alpha:
                    return init_res, x, y
                if init_res < beta:
                    beta = init_res

            elif prev_move != move:
                if res > init_res:
                    init_res, x, y = res, i, j
                if init_res >= beta:
                    return init_res, x, y
                if init_res > alpha:
                    alpha = init_res

        return init_res, x, y

    def moves_handler(self, move):
        x, y = self.get_user_move() if self.players[move] == 'user' else self.get_ai_move(self.players[move])
        self.field[x][y] = self.current_move

    def is_winner(self, win_move):
        if (win_move in self.field or
                win_move in list(map(list, zip(*self.field))) or
                win_move == [self.field[i][i] for i in range(3)] or
                win_move == [self.field[i][2 - i] for i in range(3)]):
            return True
        return False

    def game_status_handler(self):
        if self.is_winner([self.current_move] * 3):
            self.game_over = True
            print(self.current_move, 'wins')
        else:
            free_cells = [(x, y) for x in range(3) for y in range(3) if self.field[x][y] == ' ']
            if len(free_cells) == 0:
                self.game_over = True
                print('Draw')


game = TicTacToe()
game.start()
