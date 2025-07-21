from sudoku_game import SudokuGame

def demo_game():
    print("=== SUDOKU GAME DEMO ===")
    
    # Test all difficulty levels
    for difficulty in ["easy", "medium", "hard", "expert"]:
        print(f"\n{'='*50}")
        print(f"DEMO: {difficulty.upper()} DIFFICULTY")
        print(f"{'='*50}")
        
        game = SudokuGame()
        game.create_puzzle(difficulty)
        
        print(f"\nGenerated {difficulty} puzzle:")
        game.print_grid()
        
        print(f"\nSolution:")
        game.print_grid(game.solution)
        
        # Demo some moves
        print(f"\nDemo moves:")
        moves_made = 0
        for i in range(9):
            for j in range(9):
                if game.grid[i][j] == 0 and moves_made < 3:
                    correct_num = game.solution[i][j]
                    print(f"Making move: row {i+1}, col {j+1} = {correct_num}")
                    success = game.make_move(i, j, correct_num)
                    if success:
                        moves_made += 1
                    break
            if moves_made >= 3:
                break
        
        print(f"\nPuzzle after demo moves:")
        game.print_grid()
        
        print(f"\nPuzzle statistics:")
        empty_cells = sum(1 for i in range(9) for j in range(9) if game.grid[i][j] == 0)
        print(f"- Empty cells: {empty_cells}")
        print(f"- Filled cells: {81 - empty_cells}")
        print(f"- Completion: {((81 - empty_cells) / 81) * 100:.1f}%")
        
    print(f"\n{'='*50}")
    print("DEMO COMPLETE")
    print("To play interactively, run: python3 sudoku_game.py")
    print(f"{'='*50}")

if __name__ == "__main__":
    demo_game()