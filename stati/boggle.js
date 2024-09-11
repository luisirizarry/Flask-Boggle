class BoogleGame {
    constructor(boardId, secs = 60) {
        // initialize the game
        this.board = $('#' + boardId)
        this.score = 0
        this.words = new Set()
        this.secs = secs
        this.timer = null
        this.message = $("#message-text")
        this.guessInput = $("#guess-input")
    }

    bindEvents() {
        // bind events
        $('#start-button').on('click', () => this.start());
        $('#guess-form').on('submit', (evt) => this.checkUserGuess(evt));
    }

    start(){
        // start the game
        this.showTimer();
        this.startTimer();
    }

    startTimer() {
        // start the timer
        if(this.timer) return;
        this.showTimer();

        // set interval to count down
        this.timer = setInterval(() => {
            this.secs -= 1;
            this.showTimer();
            
            // if time runs out, end the game
            if (this.secs <= 0) {
                this.endGame();
            }
        }, 1000);
    }

    // show the timer
    showTimer(){
        $('#time').text(this.secs)
    }

    // check the user's guess from the info sent from the server, and update the score
    checkDataResult(result, length){
        if (result === 'ok') {
            this.sendMessage("Good job! That's a word on the board.");
            this.score += length;
        } 
        else if (result === 'not-on-board') {
            this.sendMessage("Sorry, that word is not on the board.");
        } 
        else if (result === 'not-word') {
            this.sendMessage("Sorry, that's not a valid word.");
        } 
        else if (result === 'duplicate') {
            this.sendMessage("You already used that word.");
        } 
        else {
            this.sendMessage("Error: " + result);
        }
    }

    // check the user's guess
    async checkUserGuess(evt) {
        evt.preventDefault();

        const guess = this.guessInput.val();

        try {
            // send the guess to the server
            const resp = await axios.post('/check-guess', { "guess": guess });

            // check the result of the guess and send it to the checkDataResult function
            this.checkDataResult(resp.data.result, guess.length)

            // Clear the message box 
            setTimeout(() => {
                this.sendMessage('');
            }, 1500);

            // Clear the input box
            this.guessInput.val('');
        } catch (e) {
            console.error("Error: ", e);
        }

        // send score to the server
        await this.sendScore(this.score);
    }

    // send a message to the user
    sendMessage(message){
        $("#message-text").text(message)
    }

    // send the score to the server
    async sendScore(score) {
        try {
            // send the score to the server
            const resp = await axios.post('/post-score', { "score": score });
            // update the score on the page
            $('#score-value').text(resp.data.score);
        } catch (e) {
            console.error("Error sending score: ", e);
        }
    }

    // send the high score to the server
    async sendHighScore(score) {
        try {
            // send the high score to the server
            const resp = await axios.post('/post-high-score', { "score": score });
            // update the high score and times played on the page
            if (resp.data.highscore) {
                $('#highscore-value').text(resp.data.highscore);
            }
            $('#times-played-value').text(resp.data.games_played);
        } catch (e){
            console.error("Error sending high score and times played: ", e);
        }
    }

    // end the game
    endGame(){
        // clear the timer
        clearInterval(this.timer);
        this.timer = null
        // tell the user the game ended and thier score
        this.sendMessage(`Game Over, your score was ${this.score}`);
        // disable the buttons and input
        $('#submit-btn').prop('disabled', true);
        $('#start-button').prop('disabled', true);
        $('#guess-input').prop('disabled', true);
        // send the high score to the server
        this.sendHighScore(this.score);
    }


}

// when document is ready, create a new game and allow the user to play the game
$(document).ready(function() {
    const game = new BoogleGame('game-board', 60);
    game.bindEvents();
});