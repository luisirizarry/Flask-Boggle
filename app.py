from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
app.run(debug=True)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

boggle_game = Boggle()

@app.route('/')
def boogle_home():
    """Show board."""
    board = boggle_game.make_board()
    session['board'] = board
    score = session.get("score", 0)

    return render_template("boggle.html", board=board, score=score)