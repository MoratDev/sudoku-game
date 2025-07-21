import http.server
import socketserver
import json
import urllib.parse
from sudoku_game import SudokuGame
import threading
import webbrowser
import time

class SudokuWebServer(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.game = SudokuGame()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.serve_index()
        elif self.path.startswith('/api/'):
            self.handle_api_get()
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path.startswith('/api/'):
            self.handle_api_post()
        else:
            self.send_error(404)
    
    def serve_index(self):
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sudoku Game</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #333;
        }

        .container {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            max-width: 600px;
            width: 95%;
        }

        h1 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 30px;
            font-size: 2.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }

        .controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            flex-wrap: wrap;
            gap: 15px;
        }

        .difficulty-section {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .difficulty-section label {
            font-weight: bold;
            color: #2c3e50;
        }

        select {
            padding: 8px 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 14px;
            background: white;
        }

        .buttons {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }

        button {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 14px;
        }

        .btn-primary { background: #4CAF50; color: white; }
        .btn-warning { background: #ff9800; color: white; }
        .btn-info { background: #2196F3; color: white; }
        .btn-purple { background: #9C27B0; color: white; }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        .sudoku-grid {
            display: grid;
            grid-template-columns: repeat(9, 1fr);
            gap: 1px;
            background: #333;
            border: 3px solid #333;
            margin: 20px auto;
            width: fit-content;
            border-radius: 8px;
            overflow: hidden;
        }

        .cell {
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            background: white;
            transition: all 0.2s ease;
        }

        .cell:nth-child(3n):not(:nth-child(9n)) {
            border-right: 2px solid #333;
        }

        .cell:nth-child(n+19):nth-child(-n+27),
        .cell:nth-child(n+46):nth-child(-n+54) {
            border-bottom: 2px solid #333;
        }

        .cell.selected {
            background: #e3f2fd !important;
            border: 2px solid #2196F3;
        }

        .cell.fixed {
            background: #f5f5f5;
            color: #333;
        }

        .cell.user-input {
            color: #2196F3;
        }

        .cell:hover:not(.selected) {
            background: #f0f0f0;
        }

        .number-input {
            display: flex;
            justify-content: center;
            gap: 8px;
            margin: 20px 0;
            flex-wrap: wrap;
        }

        .number-btn {
            width: 40px;
            height: 40px;
            border: 2px solid #ddd;
            background: white;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .number-btn:hover {
            background: #2196F3;
            color: white;
            border-color: #2196F3;
        }

        .status {
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            font-weight: bold;
            color: #2c3e50;
        }

        .instruction {
            text-align: center;
            margin: 15px 0;
            color: #666;
            font-size: 14px;
        }

        @media (max-width: 600px) {
            .container {
                padding: 20px;
            }
            
            .controls {
                flex-direction: column;
                align-items: stretch;
            }
            
            .buttons {
                justify-content: center;
            }
            
            .cell {
                width: 35px;
                height: 35px;
                font-size: 14px;
            }
            
            .number-btn {
                width: 35px;
                height: 35px;
                font-size: 14px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧩 SUDOKU</h1>
        
        <div class="controls">
            <div class="difficulty-section">
                <label for="difficulty">Difficulty:</label>
                <select id="difficulty">
                    <option value="easy">Easy</option>
                    <option value="medium" selected>Medium</option>
                    <option value="hard">Hard</option>
                    <option value="expert">Expert</option>
                </select>
            </div>
            
            <div class="buttons">
                <button class="btn-primary" onclick="newGame()">New Game</button>
                <button class="btn-warning" onclick="clearCell()">Clear Cell</button>
                <button class="btn-info" onclick="getHint()">Hint</button>
                <button class="btn-purple" onclick="showSolution()">Solution</button>
            </div>
        </div>
        
        <div class="sudoku-grid" id="sudokuGrid"></div>
        
        <div class="instruction">Click a cell, then click a number below:</div>
        
        <div class="number-input">
            <button class="number-btn" onclick="inputNumber(1)">1</button>
            <button class="number-btn" onclick="inputNumber(2)">2</button>
            <button class="number-btn" onclick="inputNumber(3)">3</button>
            <button class="number-btn" onclick="inputNumber(4)">4</button>
            <button class="number-btn" onclick="inputNumber(5)">5</button>
            <button class="number-btn" onclick="inputNumber(6)">6</button>
            <button class="number-btn" onclick="inputNumber(7)">7</button>
            <button class="number-btn" onclick="inputNumber(8)">8</button>
            <button class="number-btn" onclick="inputNumber(9)">9</button>
        </div>
        
        <div class="status" id="status">Welcome! Click 'New Game' to start playing.</div>
    </div>

    <script>
        let selectedCell = null;
        let gameData = { grid: [], solution: [], originalGrid: [] };

        function createGrid() {
            const grid = document.getElementById('sudokuGrid');
            grid.innerHTML = '';
            
            for (let i = 0; i < 81; i++) {
                const cell = document.createElement('div');
                cell.className = 'cell';
                cell.onclick = () => selectCell(Math.floor(i / 9), i % 9);
                cell.id = `cell-${Math.floor(i / 9)}-${i % 9}`;
                grid.appendChild(cell);
            }
        }

        function selectCell(row, col) {
            // Clear previous selection
            if (selectedCell) {
                const oldCell = document.getElementById(`cell-${selectedCell[0]}-${selectedCell[1]}`);
                oldCell.classList.remove('selected');
            }
            
            // Select new cell
            selectedCell = [row, col];
            const cell = document.getElementById(`cell-${row}-${col}`);
            cell.classList.add('selected');
            
            updateStatus(`Selected cell: Row ${row + 1}, Column ${col + 1}`);
        }

        function updateStatus(message) {
            document.getElementById('status').textContent = message;
        }

        async function newGame() {
            const difficulty = document.getElementById('difficulty').value;
            
            try {
                const response = await fetch('/api/new_game', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ difficulty: difficulty })
                });
                
                gameData = await response.json();
                updateDisplay();
                
                const emptyCount = gameData.grid.flat().filter(x => x === 0).length;
                updateStatus(`New ${difficulty} puzzle generated! ${emptyCount} empty cells.`);
            } catch (error) {
                updateStatus('Error generating new game!');
            }
        }

        function updateDisplay() {
            for (let i = 0; i < 9; i++) {
                for (let j = 0; j < 9; j++) {
                    const cell = document.getElementById(`cell-${i}-${j}`);
                    const value = gameData.grid[i][j];
                    
                    cell.textContent = value === 0 ? '' : value;
                    cell.classList.remove('fixed', 'user-input');
                    
                    if (gameData.originalGrid[i][j] !== 0) {
                        cell.classList.add('fixed');
                    } else if (value !== 0) {
                        cell.classList.add('user-input');
                    }
                }
            }
        }

        async function inputNumber(num) {
            if (!selectedCell) {
                updateStatus('Please select a cell first!');
                return;
            }
            
            const [row, col] = selectedCell;
            
            if (gameData.originalGrid[row][col] !== 0) {
                updateStatus('Cannot modify fixed cells!');
                return;
            }
            
            try {
                const response = await fetch('/api/make_move', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ row: row, col: col, num: num })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    gameData.grid[row][col] = num;
                    updateDisplay();
                    updateStatus(`Placed ${num} in cell (${row + 1}, ${col + 1})`);
                    
                    if (result.completed) {
                        setTimeout(() => {
                            alert('🎉 Congratulations! You solved the puzzle!');
                            updateStatus('Puzzle completed! Well done!');
                        }, 100);
                    }
                } else {
                    updateStatus(`Invalid move! ${num} conflicts with Sudoku rules.`);
                }
            } catch (error) {
                updateStatus('Error making move!');
            }
        }

        async function clearCell() {
            if (!selectedCell) {
                updateStatus('Please select a cell first!');
                return;
            }
            
            const [row, col] = selectedCell;
            
            if (gameData.originalGrid[row][col] !== 0) {
                updateStatus('Cannot clear fixed cells!');
                return;
            }
            
            gameData.grid[row][col] = 0;
            updateDisplay();
            updateStatus(`Cleared cell (${row + 1}, ${col + 1})`);
        }

        async function getHint() {
            if (!selectedCell) {
                updateStatus('Please select a cell for hint!');
                return;
            }
            
            const [row, col] = selectedCell;
            
            if (gameData.grid[row][col] !== 0) {
                updateStatus('Cell is already filled!');
                return;
            }
            
            const hintNumber = gameData.solution[row][col];
            updateStatus(`Hint: The number for this cell is ${hintNumber}`);
        }

        function showSolution() {
            if (confirm('Are you sure you want to see the complete solution?')) {
                gameData.grid = gameData.solution.map(row => [...row]);
                updateDisplay();
                updateStatus('Complete solution displayed');
            }
        }

        // Initialize the grid when page loads
        createGrid();
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def handle_api_post(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())
        
        if self.path == '/api/new_game':
            difficulty = data.get('difficulty', 'medium')
            self.game.create_puzzle(difficulty)
            
            response_data = {
                'grid': self.game.grid,
                'solution': self.game.solution,
                'originalGrid': [row[:] for row in self.game.grid]
            }
        
        elif self.path == '/api/make_move':
            row = data['row']
            col = data['col']
            num = data['num']
            
            success = self.game.make_move(row, col, num)
            completed = self.game.is_complete() and self.game.is_valid_solution()
            
            response_data = {
                'success': success,
                'completed': completed
            }
        
        else:
            self.send_error(404)
            return
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())

def start_server():
    PORT = 8000
    with socketserver.TCPServer(("", PORT), SudokuWebServer) as httpd:
        print(f"🎮 Sudoku Web App running at http://localhost:{PORT}")
        print("Press Ctrl+C to stop the server")
        
        # Open browser automatically
        def open_browser():
            time.sleep(1)
            webbrowser.open(f'http://localhost:{PORT}')
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")

if __name__ == "__main__":
    start_server()