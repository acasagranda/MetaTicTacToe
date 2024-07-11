from project import calculate_moves, check_for_full, check_for_win, get_computer_move


class Grid:
    def __init__(self):
        self.status = 'free'
        self.cells = [' ']*10


def test_calculate_moves():
    grids = []
    for _ in range(10):
        grids.append(Grid())
    moves = []
    for i in range(1, 10):
        moves.append((2, i))
    moves2 = []
    for i in range(1, 10):
        for j in range(1, 10):
            moves2.append((i, j))

    # initially moves should be all 81 cells
    assert calculate_moves(grids, 0) == moves2

    # if last person chooses small grid cell 2, new moves come from big grid cell 2
    assert calculate_moves(grids, 2) == moves

    for j in range(1, 10):
        moves2.remove((3, j))
    grids[3].status = 'X'

    # if a small grid is already won it should not be used for possible moves
    assert calculate_moves(grids, 3) == moves2

    # if a small grid is full it should not be used for possible moves
    grids[3].status = 'full'
    assert calculate_moves(grids, 3) == moves2


def test_check_for_full():
    grids = []
    for _ in range(10):
        grids.append(Grid())

    assert check_for_full(grids, 4) == False

    grids[5].cells[1] = 'X'
    grids[5].cells[2] = 'O'
    grids[5].cells[3] = 'X'
    grids[5].cells[4] = 'O'
    grids[5].cells[5] = 'X'
    grids[5].cells[6] = 'O'
    grids[5].cells[7] = 'O'
    grids[5].cells[8] = 'X'
    grids[5].cells[9] = 'O'

    # small grid is full of tokens
    assert check_for_full(grids, 5) == True

    grids[0].cells[1] = 'full'
    grids[0].cells[2] = 'X'
    grids[0].cells[3] = 'O'
    grids[0].cells[4] = 'X'
    grids[0].cells[5] = 'full'
    grids[0].cells[6] = 'O'
    grids[0].cells[7] = 'full'
    grids[0].cells[8] = 'X'
    grids[0].cells[9] = 'X'

    # large grid is full of ties or tokens
    assert check_for_full(grids, 0) == True


def test_check_for_win():
    grids = []
    for _ in range(10):
        grids.append(Grid())

    assert check_for_win(grids, 4, 'X') == False

    # check for win by row

    grids[5].cells[1] = 'X'
    grids[5].cells[2] = 'O'
    grids[5].cells[3] = 'X'
    grids[5].cells[4] = 'X'
    grids[5].cells[5] = 'X'
    grids[5].cells[6] = 'X'
    grids[5].cells[7] = 'O'
    grids[5].cells[8] = 'X'
    grids[5].cells[9] = 'O'

    assert check_for_win(grids, 5, 'O') == False
    assert check_for_win(grids, 5, 'X') == True

    # check for win by column

    grids[5].cells[5] = '*'
    grids[5].cells[7] = 'X'

    assert check_for_win(grids, 5, 'X') == True

    # check for win by diagonal

    grids[5].cells[4] = '*'
    grids[5].cells[5] = 'X'

    assert check_for_win(grids, 5, 'X') == True


def test_get_computer_move():
    grids = []
    for _ in range(10):
        grids.append(Grid())

    grids[1].status = 'X'
    grids[2].staus = 'full'
    grids[3].status = 'O'
    moves = [(1, 4), (2, 7), (3, 3), (4, 2)]

    # computer doesn't choose a move that will give user free choice if possible
    assert get_computer_move(grids, moves) == (4, 2)
