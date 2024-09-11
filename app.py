from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

boggle_game = Boggle()

@app.route('/')
def boogle_home():
    """Show board and initialize session variables."""
    board = boggle_game.make_board()
    
    # Initialize session variables if they don't exist
    session.setdefault('highscore', 0)
    session.setdefault('games_played', 0)
    session['word_set'] = []  # Reset word_set to an empty list for a new game
    
    # Update session with new board
    session['board'] = board
    
    # Retrieve current score
    score = session.get("score", 0)
    
    # Prepare data for rendering
    highscore = session['highscore']
    games_played = session['games_played']

    return render_template("boggle.html", board=board, score=score, highscore=highscore, games_played=games_played)

@app.route('/check-guess', methods=["POST"])
def check_word():
    """Check if the guessed word is valid."""
    guess = request.json.get("guess")
    board = session.get("board")
    word_set = set(session.get("word_set", []))

    response = boggle_game.check_valid_word(board, guess)

    """If the word is valid, add it to the word_set."""
    if response == 'ok':
        if guess in word_set:
            response = "duplicate"
        else:
            word_set.add(guess)
            session['word_set'] = list(word_set)

    return jsonify({"result": response})

@app.route('/post-score', methods=["POST"])
def post_score():
    """Receive the current score and return it in the response."""
    score = request.json.get("score")
    session["score"] = score

    return jsonify({"score": score})

@app.route('/post-high-score', methods=["POST"])
def post_high_score():
    """Receive a score, update high score and games played, then return the updated values."""
    score = request.json.get("score")
    highscore = session.get("highscore", 0)

    """Update games played."""
    games_played = session.get("games_played", 0) + 1
    session["games_played"] = games_played

    """Update highscore if the new score is higher."""
    if highscore < score:
        session["highscore"] = score
        return jsonify({
            "highscore": score, 
            "games_played": games_played})
    else:
        return jsonify({
            "highscore": highscore,
            "games_played": games_played})

