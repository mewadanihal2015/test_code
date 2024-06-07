let randomNumber;
let attempts;
let score;

function startGame() {
    randomNumber = Math.floor(Math.random() * 100) + 1;
    attempts = 0;
    score = 100;
    setMessage('');
    updateScore();
}

function checkGuess() {
    const userGuess = parseInt(document.getElementById('userGuess').value);
    attempts++;

    if (isNaN(userGuess) || userGuess < 1 || userGuess > 100) {
        setMessage('Please enter a valid number between 1 and 100.');
        return;
    }

    if (userGuess === randomNumber) {
        setMessage(`Congratulations! You've guessed the correct number ${randomNumber} in ${attempts} attempts. Your score is ${score}.`);
    } else if (userGuess < randomNumber) {
        setMessage('Too low! Try a higher number.');
        score -= 10;
    } else {
        setMessage('Too high! Try a lower number.');
        score -= 10;
    }

    if (score <= 0) {
        setMessage(`Game Over! The correct number was ${randomNumber}. Your score is 0. Would you like to play again?`);
        disableInput();
    }

    updateScore();
}

function setMessage(message) {
    document.getElementById('message').textContent = message;
}

function updateScore() {
    document.getElementById('score').textContent = `Score: ${score}`;
}

function disableInput() {
    document.getElementById('userGuess').disabled = true;
    document.getElementById('userGuess').value = '';
    document.getElementById('userGuess').placeholder = 'Game Over';
    document.getElementById('userGuess').setAttribute('title', 'Game Over');
}

startGame();
