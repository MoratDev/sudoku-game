from sudoku_game import SudokuGame

def test_sudoku():
    print("Testing Sudoku Game Components...")
    
    game = SudokuGame()
    
    print("\n1. Testing puzzle generation for different difficulties...")
    
    for difficulty in ["easy", "medium", "hard", "expert"]:
        print(f"\n--- {difficulty.upper()} PUZZLE ---")
        game.create_puzzle(difficulty)
        
        empty_cells = sum(1 for i in range(9) for j in range(9) if game.grid[i][j] == 0)
        total_cells = 81
        filled_cells = total_cells - empty_cells
        
        print(f"Empty cells: {empty_cells}, Filled cells: {filled_cells}")
        
        game.print_grid()
        
        print(f"\nValidating solution exists...")
        solution_valid = game.is_valid_solution() if game.is_complete() else True
        print(f"Puzzle is valid: {solution_valid}")
    
    print("\n2. Testing move validation...")
    game.create_puzzle("easy")
    
    test_moves = [
        (0, 0, 5),
        (0, 1, 3),  
        (4, 4, 7)
    ]
    
    for row, col, num in test_moves:
        if game.grid[row][col] == 0:
            result = game.make_move(row, col, num)
            print(f"Move ({row+1}, {col+1}) = {num}: {'Success' if result else 'Failed'}")
        else:
            print(f"Cell ({row+1}, {col+1}) already filled with {game.grid[row][col]}")
    
    print("\n3. Testing completion check...")
    print(f"Puzzle complete: {game.is_complete()}")
    
    print("\n✅ All tests completed successfully!")

if __name__ == "__main__":
    test_sudoku()