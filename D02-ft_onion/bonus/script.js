const playerX = 'X';
const playerO = 'O';
let currentPlayer = playerX;
let board = ['', '', '', '', '', '', '', '', ''];
const winConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
];

function placeMark(index) {
    if (board[index] === '' && !checkWin()) {
        board[index] = currentPlayer;
        document.getElementById('board').children[index].innerText = currentPlayer;
        if (checkWin()) {
            document.getElementById('status').innerText = `Le joueur ${currentPlayer} a gagné !`;
        } else if (board.every(cell => cell !== '')) {
            document.getElementById('status').innerText = 'Match nul !';
        } else {
            currentPlayer = currentPlayer === playerX ? playerO : playerX;
            document.getElementById('status').innerText = `Tour du joueur ${currentPlayer}`;
        }
    }
}

function checkWin() {
    for (const condition of winConditions) {
        const [a, b, c] = condition;
        if (board[a] !== '' && board[a] === board[b] && board[a] === board[c]) {
            return true;
        }
    }
    return false;
}

function restartGame() {
    board = ['', '', '', '', '', '', '', '', ''];
    currentPlayer = playerX;
    document.getElementById('status').innerText = `Tour du joueur ${currentPlayer}`;
    Array.from(document.getElementById('board').children).forEach(cell => cell.innerText = '');
}

document.getElementById('status').innerText = `Tour du joueur ${currentPlayer}`;
