const GAME_ID = 'default';
const DOT_RADIUS = 8;
const EDGE_WIDTH = 6;
const CELL_SIZE = 80;
const PADDING = 40;

const PLAYER1_COLOR = '#3498db';
const PLAYER2_COLOR = '#e74c3c';
const EMPTY_EDGE_COLOR = 'rgba(255,255,255,0.2)';
const DOT_COLOR = '#fff';

let canvas, ctx;
let gameState = null;
let hoveredEdge = null;

function init() {
    canvas = document.getElementById('gameCanvas');
    ctx = canvas.getContext('2d');
    
    document.getElementById('resetBtn').addEventListener('click', resetGame);
    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('click', handleClick);
    canvas.addEventListener('mouseleave', () => {
        hoveredEdge = null;
        render();
    });
    
    loadGame();
}

async function loadGame() {
    const response = await fetch(`/api/game/${GAME_ID}`);
    gameState = await response.json();
    resizeCanvas();
    render();
    updateUI();
}

async function resetGame() {
    await fetch(`/api/game/${GAME_ID}/reset`, { method: 'POST' });
    document.getElementById('gameOver').classList.remove('show');
    await loadGame();
}

function resizeCanvas() {
    const rows = gameState.rows;
    const cols = gameState.cols;
    canvas.width = cols * CELL_SIZE + PADDING * 2;
    canvas.height = rows * CELL_SIZE + PADDING * 2;
}

function render() {
    if (!gameState) return;
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    drawBoxes();
    drawEdges();
    drawDots();
}

function drawBoxes() {
    const rows = gameState.rows;
    const cols = gameState.cols;
    
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            const key = `${r},${c}`;
            if (gameState.box_owners[key]) {
                const owner = gameState.box_owners[key];
                const x = PADDING + c * CELL_SIZE;
                const y = PADDING + r * CELL_SIZE;
                
                ctx.fillStyle = owner === 1 
                    ? 'rgba(52, 152, 219, 0.3)' 
                    : 'rgba(231, 76, 60, 0.3)';
                ctx.fillRect(x, y, CELL_SIZE, CELL_SIZE);
                
                ctx.fillStyle = owner === 1 ? PLAYER1_COLOR : PLAYER2_COLOR;
                ctx.font = 'bold 24px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(owner === 1 ? '1' : '2', x + CELL_SIZE/2, y + CELL_SIZE/2);
            }
        }
    }
}

function drawEdges() {
    const rows = gameState.rows;
    const cols = gameState.cols;
    
    for (let r = 0; r <= rows; r++) {
        for (let c = 0; c < cols; c++) {
            const idx = r * cols + c;
            const filled = gameState.horizontal_edges[idx];
            const isHovered = hoveredEdge && 
                hoveredEdge.orientation === 'H' && 
                hoveredEdge.r === r && 
                hoveredEdge.c === c;
            
            drawHorizontalEdge(r, c, filled, isHovered);
        }
    }
    
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c <= cols; c++) {
            const idx = r * (cols + 1) + c;
            const filled = gameState.vertical_edges[idx];
            const isHovered = hoveredEdge && 
                hoveredEdge.orientation === 'V' && 
                hoveredEdge.r === r && 
                hoveredEdge.c === c;
            
            drawVerticalEdge(r, c, filled, isHovered);
        }
    }
}

function drawHorizontalEdge(r, c, filled, isHovered) {
    const x1 = PADDING + c * CELL_SIZE;
    const y1 = PADDING + r * CELL_SIZE;
    const x2 = x1 + CELL_SIZE;
    
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y1);
    ctx.lineWidth = EDGE_WIDTH;
    
    if (filled) {
        ctx.strokeStyle = PLAYER1_COLOR;
    } else if (isHovered) {
        ctx.strokeStyle = gameState.current_player === 1 
            ? 'rgba(52, 152, 219, 0.6)' 
            : 'rgba(231, 76, 60, 0.6)';
    } else {
        ctx.strokeStyle = EMPTY_EDGE_COLOR;
    }
    
    ctx.stroke();
}

function drawVerticalEdge(r, c, filled, isHovered) {
    const x1 = PADDING + c * CELL_SIZE;
    const y1 = PADDING + r * CELL_SIZE;
    const y2 = y1 + CELL_SIZE;
    
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x1, y2);
    ctx.lineWidth = EDGE_WIDTH;
    
    if (filled) {
        ctx.strokeStyle = PLAYER1_COLOR;
    } else if (isHovered) {
        ctx.strokeStyle = gameState.current_player === 1 
            ? 'rgba(52, 152, 219, 0.6)' 
            : 'rgba(231, 76, 60, 0.6)';
    } else {
        ctx.strokeStyle = EMPTY_EDGE_COLOR;
    }
    
    ctx.stroke();
}

function drawDots() {
    const rows = gameState.rows;
    const cols = gameState.cols;
    
    for (let r = 0; r <= rows; r++) {
        for (let c = 0; c <= cols; c++) {
            const x = PADDING + c * CELL_SIZE;
            const y = PADDING + r * CELL_SIZE;
            
            ctx.beginPath();
            ctx.arc(x, y, DOT_RADIUS, 0, Math.PI * 2);
            ctx.fillStyle = DOT_COLOR;
            ctx.fill();
        }
    }
}

function getEdgeAtPosition(mx, my) {
    const rows = gameState.rows;
    const cols = gameState.cols;
    const threshold = 15;
    
    for (let r = 0; r <= rows; r++) {
        for (let c = 0; c < cols; c++) {
            const x1 = PADDING + c * CELL_SIZE;
            const y1 = PADDING + r * CELL_SIZE;
            const x2 = x1 + CELL_SIZE;
            
            const midX = (x1 + x2) / 2;
            const midY = y1;
            
            if (Math.abs(mx - midX) < CELL_SIZE / 2 - DOT_RADIUS && 
                Math.abs(my - midY) < threshold) {
                const idx = r * cols + c;
                if (!gameState.horizontal_edges[idx]) {
                    return { orientation: 'H', r, c };
                }
            }
        }
    }
    
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c <= cols; c++) {
            const x1 = PADDING + c * CELL_SIZE;
            const y1 = PADDING + r * CELL_SIZE;
            const y2 = y1 + CELL_SIZE;
            
            const midX = x1;
            const midY = (y1 + y2) / 2;
            
            if (Math.abs(mx - midX) < threshold && 
                Math.abs(my - midY) < CELL_SIZE / 2 - DOT_RADIUS) {
                const idx = r * (cols + 1) + c;
                if (!gameState.vertical_edges[idx]) {
                    return { orientation: 'V', r, c };
                }
            }
        }
    }
    
    return null;
}

function handleMouseMove(e) {
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    
    const edge = getEdgeAtPosition(mx, my);
    if (JSON.stringify(edge) !== JSON.stringify(hoveredEdge)) {
        hoveredEdge = edge;
        render();
    }
}

async function handleClick(e) {
    if (gameState.game_over) return;
    
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    
    const edge = getEdgeAtPosition(mx, my);
    if (!edge) return;
    
    const response = await fetch(`/api/game/${GAME_ID}/move`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(edge)
    });
    
    if (response.ok) {
        gameState = await response.json();
        hoveredEdge = null;
        render();
        updateUI();
    }
}

function updateUI() {
    document.getElementById('score1').textContent = gameState.scores['1'] || 0;
    document.getElementById('score2').textContent = gameState.scores['2'] || 0;
    
    const turnIndicator = document.getElementById('turnIndicator');
    turnIndicator.textContent = `Player ${gameState.current_player}'s Turn`;
    turnIndicator.className = 'turn-indicator';
    turnIndicator.classList.add(`player${gameState.current_player}-turn`);
    
    if (gameState.game_over) {
        const score1 = gameState.scores['1'] || 0;
        const score2 = gameState.scores['2'] || 0;
        let winnerText;
        
        if (score1 > score2) {
            winnerText = 'Player 1 Wins!';
        } else if (score2 > score1) {
            winnerText = 'Player 2 Wins!';
        } else {
            winnerText = "It's a Tie!";
        }
        
        document.getElementById('winnerText').textContent = winnerText;
        document.getElementById('gameOver').classList.add('show');
    }
}

document.addEventListener('DOMContentLoaded', init);
