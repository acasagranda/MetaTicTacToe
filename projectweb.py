import os
import random

from flask import Flask
from flask import render_template, redirect, session, url_for


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('skey')
app.config['SECRET_KEY'] = 'somesecretcode'

TOKEN = {1: 'X', 0: 'O'}


def main():
    app.run()


def check_for_all_full():
    for cell in range(1, 10):
        if session['0'][str(cell)] == 'free':
            return
    session['0']['0'] = 'full'
    session.modified = True
    return


def check_for_full(idx):
    for cell in range(1, 10):
        if session[str(idx)][str(cell)] != 'X' and session[str(idx)][str(cell)] != 'O':
            return
    session['0'][str(idx)] = 'full'
    session[str(idx)]['0'] = 'full'
    session.modified = True
    return


def check_for_full_win():

    # check rows for 3 in a row
    for cell in range(1, 10, 3):
        if session['0'][str(cell)] == session['0'][str(cell + 1)] and session['0'][str(cell)] == session['0'][str(cell + 2)]:
            session['0']['0'] = session['0'][str(cell)]
            session.modified = True
            return

    # check cols for 3 in a row
    for cell in range(1, 4):
        if session['0'][str(cell)] == session['0'][str(cell + 3)] and session['0'][str(cell)] == session['0'][str(cell + 6)]:
            session['0']['0'] = session['0'][str(cell)]
            session.modified = True
            return

    # check diagonals for 3 in a row
    if session['0']['1'] == session['0']['5'] and session['0']['1'] == session['0']['9']:
        session['0']['0'] = session['0']['1']
        session.modified = True
        return
    if session['0']['3'] == session['0']['5'] and session['0']['1'] == session['0']['7']:
        session['0']['0'] = session['0']['3']
        session.modified = True
        return


def check_for_win(idx):
    # check rows for 3 in a row
    target = TOKEN[int(session['turn']) % 2]
    for cell in range(1, 10, 3):
        if session[str(idx)][str(cell)] == target and session[str(idx)][str(cell + 1)] == target and session[str(idx)][str(cell + 2)] == target:
            session[str(idx)]['0'] = target
            session['0'][str(idx)] = target
            session.modified = True
            return

    # check cols for 3 in a row
    for cell in range(1, 4):
        if session[str(idx)][str(cell)] == target and session[str(idx)][str(cell + 3)] == target and session[str(idx)][str(cell + 6)] == target:
            session[str(idx)]['0'] = target
            session['0'][str(idx)] = target
            session.modified = True
            return

    # check diagonals for 3 in a row
    if session[str(idx)]['1'] == target and session[str(idx)]['5'] == target and session[str(idx)]['9'] == target:
        session[str(idx)]['0'] = target
        session['0'][str(idx)] = target
        session.modified = True
        return

    if session[str(idx)]['3'] == target and session[str(idx)]['5'] == target and session[str(idx)]['7'] == target:
        session[str(idx)]['0'] = target
        session['0'][str(idx)] = target
        session.modified = True
        return

    return


def choose_best_move():
    moves = []
    for i in range(1, 10):
        for cell in range(1, 10):
            if session[str(i)]['0'] == 'free' and session[str(i)][str(cell)] == 'include':
                moves.append((i, cell))
    best_moves = [move for move in moves if session[str(move[1])]['0'] == 'free']
    if best_moves:
        move = random.choice(best_moves)
    else:
        move = random.choice(moves)

    return str(move[0]) + str(move[1])


def initialize_game():
    for i in range(10):
        session[str(i)] = {'0': 'free'}
        session['0'][str(i)] = 'free'
    for i in range(1, 10):
        for j in range(i, 10):
            session[str(i)][str(j)] = 'include'
            session[str(j)][str(i)] = 'include'


def set_up_next_move(idx):
    # change all includes from last move to ''
    for i in range(1, 10):
        for j in range(i, 10):
            if session[str(i)][str(j)] == 'include':
                session[str(i)][str(j)] = ''
            if session[str(j)][str(i)] == 'include':
                session[str(j)][str(i)] = ''
    # if the indicated cell is already won by X or O or it is full set ALL '' cells to 'include' otherwise only those in indicated cell
    if session[str(idx)]['0'] == 'free':
        for j in range(1, 10):
            if session[str(idx)][str(j)] == '':
                session[str(idx)][str(j)] = 'include'
    else:
        for i in range(1, 10):
            for j in range(1, 10):
                if session[str(i)][str(j)] == '':
                    session[str(i)][str(j)] = 'include'
    session.modified = True
    return


@app.route('/', methods=['GET', 'POST'])
def index():
    session['turn'] = 1
    initialize_game()
    return render_template('userturn.html', message='x')


@app.route('/computer_turn/<x>', methods=['GET', 'POST'])
def computer_turn(x):
    # x is the move the user chose
    session[x[0]][x[1]] = 'X'
    
    check_for_win(int(x[0]))
    if session[x[0]]['0'] == 'X':
        check_for_full_win()
    session.modified = True
    if session['0']['0'] in ['X', 'O']:
        return redirect(url_for('winner'))

    if session[x[0]]['0'] != 'X':
        check_for_full(int(x[0]))
    check_for_all_full()
    session.modified = True
    if session['0']['0'] != 'free':
        return redirect(url_for('winner'))

    set_up_next_move(int(x[1]))

    session["turn"] += 1
    session['best_move'] = choose_best_move()

    return render_template('computerturn.html', best_move=session['best_move'])


@app.route('/directions', methods=['GET', 'POST'])
def directions():

    return render_template('directions.html')


@app.route('/user_turn/<x>', methods=['GET', 'POST'])
def user_turn(x):
    # x is the move the computer chose
    session[x[0]][x[1]] = 'O'

    check_for_win(int(x[0]))
    if session[x[0]]['0'] == 'O':
        check_for_full_win()
    session.modified = True
    if session['0']['0'] in ['X', 'O']:
        return redirect(url_for('winner'))

    if session[x[0]]['0'] != 'O':
        check_for_full(int(x[0]))
    check_for_all_full()
    session.modified = True
    if session['0']['0'] != 'free':
        return redirect(url_for('winner'))

    set_up_next_move(int(x[1]))
    session["turn"] += 1

    return render_template('userturn.html', message='x')


@app.route('/winner', methods=['GET', 'POST'])
def winner():
    # change all includes from last move to ''
    for i in range(1, 10):
        for j in range(i, 10):
            if session[str(i)][str(j)] == 'include':
                session[str(i)][str(j)] = ''
            if session[str(j)][str(i)] == 'include':
                session[str(j)][str(i)] = ''
    session.modified = True
    if session['0']['0'] == 'full':
        message = "The game ends in a tie!!"
    else:
        message = f"{session['0']['0']} has won!"
    return render_template('userturn.html', message=message)


if __name__ == "__main__":
    main()
