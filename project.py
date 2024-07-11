import random

from time import sleep


TOKEN = {1: 'X', 0: 'O'}


class Grid:
    def __init__(self):
        self.status = 'free'
        self.cells = [' ']*10


def main():
    print(instructions())
    play_again = play('no')
    while play_again == 'yes':
        again = 'yes'
        grids = initialize_grids()
        turn = 0
        last_move = 0

        # grids[0] hold the big grid's data, grids 1-9 hold the small grids' data
        # status tells whether a grid has been won by 'X' or 'O' or is 'full' or is still 'free' to play in
        # cells store whether the cell has been chosen by 'X' or 'O' or is free (' ') or is a possible next choice ('*')
        while grids[0].status == 'free':
            turn += 1

            # calculate the possible moves based on the last move
            moves = calculate_moves(grids, last_move)
            print_board(grids)

            # user takes odd turns, computer takes even
            if turn % 2 == 1:
                move = get_user_move(grids, moves)
            else:
                move = get_computer_move(grids, moves)
                # change grid, cell data to row, column data
                row = ((move[0] - 1) // 3) * 3 + (move[1] - 1) // 3 + 1
                col = ((move[0] - 1) % 3) * 3 + (move[1] - 1) % 3 + 1
                sleep(1)
                print(f"I choose row {row} and column {col}")
                sleep(2)

            # the cell last played in tells which big cell is playable for next player
            last_move = move[1]

            # record last move
            grids[move[0]].cells[move[1]] = TOKEN[turn % 2]

            if check_for_win(grids, move[0], TOKEN[turn % 2]):

                # there has been a win in a small grid. Change status of that grid and mark grid[0]'s cell
                grids[move[0]].status = TOKEN[turn % 2]
                grids[0].cells[move[0]] = TOKEN[turn % 2]

                if check_for_win(grids, 0, TOKEN[turn % 2]):
                    # there is an overall win.  Change status of grid[0]
                    grids[0].status = TOKEN[turn % 2]

                elif check_for_full(grids, 0):

                    # all small grids are full.  Change status of grid[0]
                    grids[0].status = 'full'

            elif check_for_full(grids, move[0]):

                # this grid is full. Change status of that grid and mark grid[0]'s cell
                grids[move[0]].status = 'full'
                grids[0].cells[move[0]] = 'full'

                if check_for_full(grids, 0):

                    # all small grids are full.  Change status of grid[0]
                    grids[0].status = 'full'
            print()

        print_board(grids)
        if grids[0].status == 'full':
            print("The game is a tie!!")
        else:
            print(f"{TOKEN[turn % 2]} wins!!")
        print()
        play_again = play(again)


def calculate_moves(grids, last_move):
    # change all * from last move to ' '
    if last_move != 0:
        for big in range(1, 10):
            for small in range(1, 10):
                if grids[big].cells[small] == '*':
                    grids[big].cells[small] = ' '
    moves = []
    # if the indicated cell is already won by X or O or it is full set ALL '' cells to '*' otherwise only those in indicated cell
    if last_move == 0 or grids[last_move].status in ['X', 'O', 'full']:
        for big in range(1, 10):
            if grids[big].status == 'free':
                for small in range(1, 10):
                    if grids[big].cells[small] == ' ':
                        grids[big].cells[small] = '*'
                        moves.append((big, small))
    else:
        for small in range(1, 10):
            if grids[last_move].cells[small] == ' ':
                grids[last_move].cells[small] = '*'
                moves.append((last_move, small))
    return moves


def check_for_full(grids, grid_num):
    cells = grids[grid_num].cells
    for cell in range(1, 10):
        if cells[cell] == ' ' or cells[cell] == '*' or cells[cell] == 'free':
            return False
    return True


def check_for_win(grids, grid_num, target):
    cells = grids[grid_num].cells

    # check rows for 3 in a row
    for cell in range(1, 10, 3):
        if cells[cell] == target and cells[cell + 1] == target and cells[cell + 2] == target:
            return True

    # check cols for 3 in a row
    for cell in range(1, 4):
        if cells[cell] == target and cells[cell + 3] == target and cells[cell + 6] == target:
            return True

    # check diagonals for 3 in a row
    if cells[1] == target and cells[5] == target and cells[9] == target:
        return True

    if cells[3] == target and cells[5] == target and cells[7] == target:
        return True

    return False


def get_computer_move(grids, moves):
    # make this better
    best_moves = [move for move in moves if grids[move[1]].status == 'free']
    if best_moves:
        move = random.choice(best_moves)
    else:
        move = random.choice(moves)

    return move


def get_user_move(grids, moves):
    while True:
        print("Legal moves are marked with *")
        try:
            row = int(input("What row do you want to place your X in? ").strip())
        except ValueError:
            print("Enter a number.")
            continue
        try:
            col = int(input("What column do you want to place your X in? ").strip())
        except ValueError:
            print("Enter a number.")
            continue

        # convert from row, col to grid, cell
        big = ((row - 1) // 3) * 3 + (col - 1) // 3 + 1
        cell = ((row - 1) % 3) * 3 + (col - 1) % 3 + 1
        if (big, cell) in moves:
            break
        print("This is not a legal move.")
    return (big, cell)


def initialize_grids():
    grids = []
    for _ in range(10):
        grids.append(Grid())
    return grids


def instructions():
    return """\nMeta Tic-Tac-Toe is also known as Ultimate Tic-Tac-Toe and Super Tic-Tac-Toe.
            \nIt is a board game set up like regular tic-tac-toe but in each cell of the big grid there is a smaller tic-tac-toe grid.
            \nX goes first. (In this game, that's you.  The computer is O.)
            \nThe first X can go in any of the 81 cells.  Where you place it determines the computer's options for the next move.
            \nWhichever cell you place it in relation to the small grid is the position of the large grid the computer must choose a cell from.
            \nWhichever cell the computer chooses will similarly determine your options for your next move.
            \nOnce a small grid has been won, or is completely filled in a tie, no more moves can be played in that small grid.
            \nIf that's the area your options are in, you may play instead in any unoccupied cell.
            \nWhoever wins three large cells in a row wins the game!\n"""


def play(again):
    if again == 'no':
        play_again = input("Would you like to play Meta Tic-Tac-Toe? ").strip()
    else:
        play_again = input("Would you like to play again? ").strip()
    if play_again.lower() in ['y', 'yes']:
        return 'yes'
    return 'no'


def print_board(grids):
    print()
    print("columns:    1   2   3       4   5   6       7   8   9")
    print()
    line_str = f"rows: "
    for line in range(9):

        # print row numbers
        line_str += str(line + 1) + "  "

        # print three small grids per each row of big grid
        for grid in range((line // 3) * 3 + 1, (line // 3) * 3 + 4):

            # check if small grid has been won by 'X' or 'O'
            if grids[grid].status in ['X', 'O'] and line % 3 != 1:
                line_str += f"               "

            # if won put token in middle
            elif grids[grid].status in ['X', 'O']:
                line_str += f"       {grids[grid].status}       "
            else:
                line_str += f"   {grids[grid].cells[1 + (line % 3)*3]} | {grids[grid].cells[2 + (line % 3)*3]} | {grids[grid].cells[3 + (line % 3)*3]}   "
            if grid != (line // 3) * 3 + 3:
                line_str += "|"
        print(line_str)

        line_str = "         "
        if (line + 1) % 3 != 0:
            for i in range((line // 3) * 3 + 1, (line // 3) * 3 + 4):
                if grids[i].status in ['X', 'O']:
                    line_str += "               "
                else:
                    line_str += "  ---+---+---  "
                if i % 3 != 0:
                    line_str += "|"
            print(line_str)

        elif line != 8:
            print("                        |               |")
            print("          --------------+---------------+-------------")
            print("                        |               |")
        line_str = "      "
    print()


if __name__ == "__main__":
    main()
