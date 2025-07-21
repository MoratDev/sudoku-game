import random
import copy

class SudokuGame:
    def __init__(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        
    def is_valid_move(self, grid, row, col, num):
        for x in range(9):
            if grid[row][x] == num or grid[x][col] == num:
                return False
        
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if grid[i + start_row][j + start_col] == num:
                    return False
        return True
    
    def solve_sudoku(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid_move(grid, i, j, num):
                            grid[i][j] = num
                            if self.solve_sudoku(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True
    
    def generate_complete_grid(self):
        grid = [[0 for _ in range(9)] for _ in range(9)]
        
        def fill_grid(grid):
            for i in range(9):
                for j in range(9):
                    if grid[i][j] == 0:
                        numbers = list(range(1, 10))
                        random.shuffle(numbers)
                        for num in numbers:
                            if self.is_valid_move(grid, i, j, num):
                                grid[i][j] = num
                                if fill_grid(grid):
                                    return True
                                grid[i][j] = 0
                        return False
            return True
        
        fill_grid(grid)
        return grid
    
    def create_puzzle(self, difficulty="medium"):
        complete_grid = self.generate_complete_grid()
        self.solution = copy.deepcopy(complete_grid)
        puzzle = copy.deepcopy(complete_grid)
        
        difficulty_levels = {
            "easy": 35,
            "medium": 45,
            "hard": 55,
            "expert": 65
        }
        
        cells_to_remove = difficulty_levels.get(difficulty, 45)
        
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        for i, j in cells[:cells_to_remove]:
            puzzle[i][j] = 0
        
        self.grid = puzzle
        return puzzle
    
    def print_grid(self, grid=None):
        if grid is None:
            grid = self.grid
            
        print("\n  " + "   ".join([str(i) for i in range(1, 10)]))
        print("  " + "-" * 37)
        
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("  " + "-" * 37)
            
            row_str = f"{i+1}|"
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    row_str += " |"
                
                if grid[i][j] == 0:
                    row_str += "   "
                else:
                    row_str += f" {grid[i][j]} "
            row_str += " |"
            print(row_str)
        print("  " + "-" * 37)
    
    def make_move(self, row, col, num):
        if self.grid[row][col] != 0:
            print("This cell is already filled!")
            return False
        
        if not self.is_valid_move(self.grid, row, col, num):
            print("Invalid move! This number conflicts with Sudoku rules.")
            return False
        
        self.grid[row][col] = num
        return True
    
    def is_complete(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return False
        return True
    
    def is_valid_solution(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return False
                
                temp = self.grid[i][j]
                self.grid[i][j] = 0
                if not self.is_valid_move(self.grid, i, j, temp):
                    self.grid[i][j] = temp
                    return False
                self.grid[i][j] = temp
        return True

def main():
    game = SudokuGame()
    
    print("=== SUDOKU GAME ===")
    print("Choose difficulty level:")
    print("1. Easy")
    print("2. Medium") 
    print("3. Hard")
    print("4. Expert")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            difficulty_map = {"1": "easy", "2": "medium", "3": "hard", "4": "expert"}
            
            if choice in difficulty_map:
                difficulty = difficulty_map[choice]
                break
            else:
                print("Please enter a valid choice (1-4)")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            return
    
    print(f"\nGenerating {difficulty} Sudoku puzzle...")
    game.create_puzzle(difficulty)
    
    print("\nInstructions:")
    print("- Enter moves as: row col number (e.g., '1 1 5' to place 5 in row 1, column 1)")
    print("- Type 'hint' to see the solution for a cell")
    print("- Type 'solution' to see the complete solution")
    print("- Type 'quit' to exit")
    
    while True:
        game.print_grid()
        
        if game.is_complete():
            if game.is_valid_solution():
                print("\n🎉 Congratulations! You solved the puzzle!")
                break
            else:
                print("\nSomething's wrong with the solution. Please check your moves.")
        
        try:
            user_input = input("\nEnter your move: ").strip().lower()
            
            if user_input == 'quit':
                print("Thanks for playing!")
                break
            elif user_input == 'solution':
                print("\nComplete solution:")
                game.print_grid(game.solution)
                continue
            elif user_input == 'hint':
                print("Enter the row and column for the hint:")
                hint_input = input("Row Col: ").strip()
                try:
                    parts = hint_input.split()
                    if len(parts) == 2:
                        hint_row, hint_col = int(parts[0]) - 1, int(parts[1]) - 1
                        if 0 <= hint_row < 9 and 0 <= hint_col < 9:
                            print(f"Hint: The answer for row {hint_row + 1}, column {hint_col + 1} is {game.solution[hint_row][hint_col]}")
                        else:
                            print("Invalid row or column!")
                    else:
                        print("Please enter row and column numbers.")
                except ValueError:
                    print("Please enter valid numbers.")
                continue
            
            parts = user_input.split()
            if len(parts) == 3:
                row, col, num = int(parts[0]) - 1, int(parts[1]) - 1, int(parts[2])
                
                if not (0 <= row < 9 and 0 <= col < 9 and 1 <= num <= 9):
                    print("Please enter valid numbers (row/col: 1-9, number: 1-9)")
                    continue
                
                game.make_move(row, col, num)
            else:
                print("Invalid input format. Use: row col number")
                
        except ValueError:
            print("Please enter valid numbers.")
        except KeyboardInterrupt:
            print("\nThanks for playing!")
            break

if __name__ == "__main__":
    main()