import chess
import chess.svg
import chess.polyglot
import time
import traceback
import chess.pgn
import chess.engine
from flask import Flask, Response, request
import webbrowser
import pyttsx3


# Evaluating the board
pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]


def evaluate_board():
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0

    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)

    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum([-pawntable[chess.square_mirror(i)]
                           for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq = sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum([-bishopstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)]
                           for i in board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)]
                             for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)]
                           for i in board.pieces(chess.KING, chess.BLACK)])

    eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
    if board.turn:
        return eval
    else:
        return -eval


# Searching the best move using minimax and alphabeta algorithm with negamax implementation
def alphabeta(alpha, beta, depthleft):
    bestscore = -9999
    if (depthleft == 0):
        return quiesce(alpha, beta)
    for move in board.legal_moves:
        board.push(move)
        score = -alphabeta(-beta, -alpha, depthleft - 1)
        board.pop()
        if (score >= beta):
            return score
        if (score > bestscore):
            bestscore = score
        if (score > alpha):
            alpha = score
    return bestscore


def quiesce(alpha, beta):
    stand_pat = evaluate_board()
    if (stand_pat >= beta):
        return beta
    if (alpha < stand_pat):
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiesce(-beta, -alpha)
            board.pop()

            if (score >= beta):
                return beta
            if (score > alpha):
                alpha = score
    return alpha


def selectmove(depth):
    try:
        move = chess.polyglot.MemoryMappedReader("C:/Users/your_path/books/human.bin").weighted_choice(board).move
        return move
    except:
        bestMove = chess.Move.null()
        bestValue = -99999
        alpha = -100000
        beta = 100000
        for move in board.legal_moves:
            board.push(move)
            boardValue = -alphabeta(-beta, -alpha, depth - 1)
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            if (boardValue > alpha):
                alpha = boardValue
            board.pop()
        return bestMove


# Speak Function for the Assistant to speak
def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  
    engine.say(text)
    engine.runAndWait()


# Searching Dev-Zero's Move
def devmove():
    move = selectmove(3)
    speak(move)
    board.push(move)





# Searching Stockfish's Move
def stockfish():
    try:
        engine = chess.engine.SimpleEngine.popen_uci("C:/Users/WELCOME/Desktop/Chess-World-master/engines/stockfish.exe")
        move = engine.play(board, chess.engine.Limit(time=0.1))
        speak(move.move)
        board.push(move.move)
    finally:
        engine.quit()



app = Flask(__name__)


# Introduction lines
def lines():
    speak(
        "Welcome to the Chess World. Enjoy your game. Hope you have fun.")


# Front Page of the Flask Web Page
@app.route("/")
def main():
    global count, board

    # Initialize the game with lines if it's the first invocation
    if count == 1:
        lines()
        count += 1

    # Start building the HTML response
    html = '<!DOCTYPE html>'
    html += '<html lang="en"><head>'
    html += '''
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chess Game</title>
        <style>
            body {
                font-family: 'Roboto', sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, #2d3436, #636e72);
                color: white;
                min-height: 100vh;
                overflow-x: hidden;
            }
            h1 {
                margin-top: 20px;
                font-size: 2.5em;
                color: #00cec9;
            }
            .container {
                text-align: center;
                padding: 20px;
                background-color: #2d3436;
                border-radius: 12px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
                width: 90%;
                max-width: 800px;
                margin: 20px;
            }
            img {
                margin: 20px auto;
                max-width: 100%;
                height: auto;
                display: block;
                border: 3px solid #00cec9;
                border-radius: 8px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
            }
            input, button {
                font-size: 18px;
                padding: 10px 20px;
                margin: 10px;
                border-radius: 8px;
                border: none;
                cursor: pointer;
                background-color: #00cec9;
                color: #2d3436;
                transition: all 0.3s ease;
            }
            input:hover, button:hover {
                background-color: #81ecec;
            }
            input[type="text"] {
                width: 250px;
            }
            form {
                margin: 15px 0;
            }
            .footer {
                margin-top: 20px;
                font-size: 0.9em;
                color: #dfe6e9;
            }
            .footer a {
                color: #00cec9;
                text-decoration: none;
            }
            .footer a:hover {
                text-decoration: underline;
            }
        </style>
    '''
    html += '</head><body>'

    # Add the header and chessboard
    html += '''
        <h1>Welcome to the Chess Game</h1>
        <div class="container">
            <img src="/board.svg?%f" alt="Chess Board"><br>
    ''' % time.time()

    # Add buttons and forms for various game actions
    actions = [
        {"action": "/game/", "label": "New Game"},
        {"action": "/undo/", "label": "Undo Last Move"},
        {"action": "/move/", "label": "Make Human Move:", "input": True},
        {"action": "/dev/", "label": "Make Dev-Zero Move"},
        {"action": "/engine/", "label": "Make Stockfish Move"},
        {"action": "/inst/", "label": "Instructions"}
    ]

    for act in actions:
        if act.get("input"):
            html += f'''
                <form action="{act["action"]}">
                    <input type="text" name="move" placeholder="Enter move (e.g., e2e4)">
                    <button type="submit">{act["label"]}</button>
                </form>
            '''
        else:
            html += f'''
                <form action="{act["action"]}" method="post">
                    <button type="submit">{act["label"]}</button>
                </form>
            '''

    # Add game status checks
    if board.is_stalemate():
        speak("It's a draw by stalemate")
    elif board.is_checkmate():
        speak("Checkmate")
    elif board.is_insufficient_material():
        speak("It's a draw by insufficient material")
    elif board.is_check():
        speak("Check")

    # Close the container and add a footer
    html += '''
        </div>
        <div class="footer">
            <p>Our Team :-
            </br>Harsh Shah
            </br>Anshit Srivastava
            </br>Priyank Paladiya
            </br>Shikhar Sharma
            </br>Maharshi Bhesania
            </p>
        </div>
    '''

    # Close the HTML tags
    html += '</body></html>'

    return html




# Display Board
@app.route("/board.svg/")
def board():
    return Response(chess.svg.board(board=board, size=700), mimetype='image/svg+xml')


# Human Move
@app.route("/move/")
def move():
    try:
        move = request.args.get('move', default="")
        speak(move)
        board.push_san(move)
    except Exception:
        traceback.print_exc()
    return main()




# Make Dev-Zero Move
@app.route("/dev/", methods=['POST'])
def dev():
    try:
        devmove()
    except Exception:
        traceback.print_exc()
        speak("illegal move, try again")
    return main()


# Make UCI Compatible engine's move
@app.route("/engine/", methods=['POST'])
def engine():
    try:
        stockfish()
    except Exception:
        traceback.print_exc()
        speak("illegal move, try again")
    return main()


# New Game
@app.route("/game/", methods=['POST'])
def game():
    speak("Board Reset, Best of Luck for the next game.")
    board.reset()
    return main()


# Undo
@app.route("/undo/", methods=['POST'])
def undo():
    try:
        board.pop()
    except Exception:
        traceback.print_exc()
        speak("Nothing to undo")
    return main()





# Instructions
@app.route("/inst/", methods=['POST'])
def inst():
    speak(
        "This is a simple chess game developed by our team. The game works with chess SAN (Standard Algebraic Notation), which you can learn by browsing online. For starters, you can make a human move like e4 or Nf3. This game is equipped with two chess engines, namely Dev-Zero and Stockfish 9, to enhance the learning experience. The Dev-Zero engine was developed by our team as part of this project. The Stockfish 9 engine, created by Tord Romstad and his team, is one of the most powerful open-source chess engines available today.The engines search for the best possible move and provide it to the user. Occasionally, the engine might not return a move due to unforeseen issues, in which case you can try again. The interface includes several user-friendly buttons that make navigation intuitive, so no detailed explanation is required.This server allows smooth one-on-one gameplay. However, communication between players is necessary to decide who will play white and black. In a two-human game, a user can make a move using the Make Human Move button or use providing AI engine. For starters, try making a move like e4 to begin playing.")
    return main()


# Main Function
if __name__ == '__main__':
    count = 1
    board = chess.Board()
    webbrowser.open("http://127.0.0.1:5000/")
    app.run()
