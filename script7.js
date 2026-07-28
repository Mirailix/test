const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
canvas.width = 400;
canvas.height = 400;

const tileSize = 40;
const levels = [
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 'E', 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    [
        [1, 1, 1, 1, 1, 'E', 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 'E', 1, 'E', 'E', 'E', 'E', 'E', 'E'],
        [1, 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
        [1, 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
        [1, 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
        [1, 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
    ],
    [
        [1,'E','E','E','E','E','E','E','E'],
        [1,'E','E','E','E','E','E','E','E'],
        [1,'E','E','E','E','E','E','E','E'],
        [1,'E','E','E','E','E','E','E','E'],
        [1,'E','E','E','E','E','E','E','E'],
        [1,'E','E','E','E','E','E','E','E'],
        [1,'E','E','E','E','E','E','E','' ],
    ]
];


const playerImg = new Image();
playerImg.src = 'player.png';

const exitImg = new Image();
exitImg.src = 'exit.png';


let playerLoaded = false;
let exitLoaded = false;

playerImg.onload = () => { playerLoaded = true; drawLevel(); };
exitImg.onload = () => { exitLoaded = true; drawLevel(); };

let player = {
    x: 1,
    y: 1,
};

let levelIndex = 0;

function drawLevel() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const level = levels[levelIndex];

    for (let y = 0; y < level.length; y++) {
        for (let x = 0; x < level[y].length; x++) {
            if (level[y][x] === 1) {
                ctx.fillStyle = '#000'; // Черный цвет для стен
                ctx.fillRect(x * tileSize, y * tileSize, tileSize, tileSize);
            }
            if (level[y][x] === 'E') {
                if (exitLoaded) {
                    ctx.drawImage(exitImg, x * tileSize, y * tileSize, tileSize, tileSize);
                } else {
                    // Запасной вариант, если картинка ещё не загрузилась
                    ctx.fillStyle = '#00F';
                    ctx.fillRect(x * tileSize + tileSize / 4,
                                 y * tileSize + tileSize / 4,
                                 tileSize / 2,
                                 tileSize / 2);
                }
            }
        }
    }

    // Рисуем игрока
    if (playerLoaded) {
        ctx.drawImage(playerImg, player.x * tileSize, player.y * tileSize, tileSize, tileSize);
    } else {
        // Запасной вариант
        ctx.fillStyle = '#FF0000';
        ctx.fillRect(player.x * tileSize, player.y * tileSize, tileSize, tileSize);
    }
}

function resetPlayerPosition() {
    player.x = 1;
    player.y = 1;
    drawLevel();
}

function checkGameOver() {
    if (levelIndex >= 2) {
        alert("Поздравляем! Вы прошли все уровни!");
        levelIndex = 0;
        resetPlayerPosition();
        drawLevel();
    }
}

function movePlayer(dx, dy) {
    const newX = player.x + dx;
    const newY = player.y + dy;
    const level = levels[levelIndex];

    if (newX < 0 || newX >= level[0].length || newY < 0 || newY >= level.length) {
        return;
    }

    if (level[newY][newX] === 1) {
        return;
    }

    player.x = newX;
    player.y = newY;

    if (level[newY][newX] === 'E') {
        levelIndex++;
        resetPlayerPosition();
    }

    checkGameOver();
    drawLevel();
}

document.addEventListener('keydown', (event) => {
    switch(event.key) {
        case 'ArrowUp':
            movePlayer(0, -1);
            break;
        case 'ArrowDown':
            movePlayer(0, 1);
            break;
        case 'ArrowLeft':
            movePlayer(-1, 0);
            break;
        case 'ArrowRight':
            movePlayer(1, 0);
            break;
    }
});

drawLevel();