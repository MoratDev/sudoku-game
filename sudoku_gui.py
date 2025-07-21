import tkinter as tk
from tkinter import ttk, messagebox, font
from sudoku_game import SudokuGame
import copy

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.root.geometry("800x900")
        self.root.resizable(False, False)
        
        # Initialize game
        self.game = SudokuGame()
        self.selected_cell = None
        self.original_grid = None
        
        # Colors
        self.colors = {
            'bg': '#f0f0f0',
            'grid_bg': 'white',
            'selected': '#e6f3ff',
            'fixed': '#f5f5f5',
            'error': '#ffebee',
            'valid': '#e8f5e8',
            'border_thick': '#000000',
            'border_thin': '#cccccc',
            'text_fixed': '#000000',
            'text_user': '#2196F3'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Title
        title_font = font.Font(family="Arial", size=24, weight="bold")
        title_label = tk.Label(main_frame, text="SUDOKU", font=title_font, 
                              bg=self.colors['bg'], fg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        # Control panel
        control_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        control_frame.pack(pady=(0, 20))
        
        # Difficulty selection
        diff_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        diff_frame.pack(side='left', padx=(0, 30))
        
        tk.Label(diff_frame, text="Difficulty:", font=('Arial', 12, 'bold'), 
                bg=self.colors['bg']).pack()
        
        self.difficulty_var = tk.StringVar(value="medium")
        difficulties = [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard"), ("Expert", "expert")]
        
        for text, value in difficulties:
            tk.Radiobutton(diff_frame, text=text, variable=self.difficulty_var, 
                          value=value, bg=self.colors['bg'], font=('Arial', 10)).pack(anchor='w')
        
        # Buttons frame
        button_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        button_frame.pack(side='left')
        
        button_style = {'font': ('Arial', 11, 'bold'), 'padx': 15, 'pady': 8}
        
        tk.Button(button_frame, text="New Game", command=self.new_game, 
                 bg='#4CAF50', fg='white', **button_style).pack(side='left', padx=5)
        tk.Button(button_frame, text="Clear Cell", command=self.clear_cell, 
                 bg='#ff9800', fg='white', **button_style).pack(side='left', padx=5)
        tk.Button(button_frame, text="Hint", command=self.get_hint, 
                 bg='#2196F3', fg='white', **button_style).pack(side='left', padx=5)
        tk.Button(button_frame, text="Solution", command=self.show_solution, 
                 bg='#9C27B0', fg='white', **button_style).pack(side='left', padx=5)
        
        # Grid frame
        self.grid_frame = tk.Frame(main_frame, bg=self.colors['border_thick'], relief='solid', bd=3)
        self.grid_frame.pack(pady=20)
        
        # Create grid
        self.cells = []
        self.create_grid()
        
        # Number input panel
        number_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        number_frame.pack(pady=20)
        
        tk.Label(number_frame, text="Click a cell, then click a number:", 
                font=('Arial', 12), bg=self.colors['bg']).pack()
        
        number_button_frame = tk.Frame(number_frame, bg=self.colors['bg'])
        number_button_frame.pack(pady=10)
        
        self.number_buttons = []
        for i in range(1, 10):
            btn = tk.Button(number_button_frame, text=str(i), command=lambda n=i: self.input_number(n),
                           font=('Arial', 14, 'bold'), width=3, height=2, 
                           bg='#ffffff', fg='#2c3e50', relief='raised', bd=2)
            btn.pack(side='left', padx=3)
            self.number_buttons.append(btn)
        
        # Status label
        self.status_label = tk.Label(main_frame, text="Welcome! Click 'New Game' to start.", 
                                    font=('Arial', 12), bg=self.colors['bg'], fg='#2c3e50')
        self.status_label.pack(pady=10)
        
    def create_grid(self):
        for i in range(9):
            row = []
            for j in range(9):
                # Determine border thickness based on position
                border_top = 3 if i % 3 == 0 else 1
                border_left = 3 if j % 3 == 0 else 1
                border_right = 3 if j == 8 or (j + 1) % 3 == 0 else 1
                border_bottom = 3 if i == 8 or (i + 1) % 3 == 0 else 1
                
                cell_frame = tk.Frame(self.grid_frame, bg=self.colors['border_thick'])
                cell_frame.grid(row=i, column=j, 
                               padx=(border_left, 0), pady=(border_top, 0))
                
                cell = tk.Label(cell_frame, text="", font=('Arial', 16, 'bold'),
                               width=3, height=2, bg=self.colors['grid_bg'],
                               relief='solid', bd=1, cursor='hand2')
                cell.pack()
                
                # Bind click event
                cell.bind("<Button-1>", lambda e, r=i, c=j: self.select_cell(r, c))
                
                row.append(cell)
            self.cells.append(row)
    
    def select_cell(self, row, col):
        # Clear previous selection
        if self.selected_cell:
            old_r, old_c = self.selected_cell
            self.update_cell_color(old_r, old_c)
        
        # Select new cell
        self.selected_cell = (row, col)
        self.cells[row][col].configure(bg=self.colors['selected'])
        
        self.status_label.configure(text=f"Selected cell: Row {row+1}, Column {col+1}")
    
    def update_cell_color(self, row, col):
        if self.original_grid and self.original_grid[row][col] != 0:
            # Fixed cell (from original puzzle)
            self.cells[row][col].configure(bg=self.colors['fixed'])
        else:
            # Empty or user-filled cell
            self.cells[row][col].configure(bg=self.colors['grid_bg'])
    
    def input_number(self, num):
        if not self.selected_cell:
            self.status_label.configure(text="Please select a cell first!")
            return
        
        row, col = self.selected_cell
        
        # Check if cell is fixed (from original puzzle)
        if self.original_grid and self.original_grid[row][col] != 0:
            self.status_label.configure(text="Cannot modify fixed cells!")
            return
        
        # Make the move
        if self.game.make_move(row, col, num):
            self.cells[row][col].configure(text=str(num), fg=self.colors['text_user'])
            self.update_cell_color(row, col)
            self.status_label.configure(text=f"Placed {num} in cell ({row+1}, {col+1})")
            
            # Check for win
            if self.game.is_complete():
                if self.game.is_valid_solution():
                    messagebox.showinfo("Congratulations!", 
                                      "🎉 You solved the puzzle! Well done!")
                    self.status_label.configure(text="Puzzle completed!")
        else:
            self.status_label.configure(text=f"Invalid move! {num} conflicts with Sudoku rules.")
    
    def new_game(self):
        difficulty = self.difficulty_var.get()
        self.game.create_puzzle(difficulty)
        self.original_grid = copy.deepcopy(self.game.grid)
        self.selected_cell = None
        
        # Update display
        for i in range(9):
            for j in range(9):
                if self.game.grid[i][j] != 0:
                    self.cells[i][j].configure(text=str(self.game.grid[i][j]), 
                                              fg=self.colors['text_fixed'])
                    self.update_cell_color(i, j)
                else:
                    self.cells[i][j].configure(text="", bg=self.colors['grid_bg'])
        
        empty_cells = sum(1 for i in range(9) for j in range(9) if self.game.grid[i][j] == 0)
        self.status_label.configure(text=f"New {difficulty} puzzle generated! {empty_cells} empty cells.")
    
    def clear_cell(self):
        if not self.selected_cell:
            self.status_label.configure(text="Please select a cell first!")
            return
        
        row, col = self.selected_cell
        
        # Check if cell is fixed
        if self.original_grid and self.original_grid[row][col] != 0:
            self.status_label.configure(text="Cannot clear fixed cells!")
            return
        
        # Clear the cell
        self.game.grid[row][col] = 0
        self.cells[row][col].configure(text="")
        self.update_cell_color(row, col)
        self.status_label.configure(text=f"Cleared cell ({row+1}, {col+1})")
    
    def get_hint(self):
        if not self.selected_cell:
            self.status_label.configure(text="Please select a cell for hint!")
            return
        
        row, col = self.selected_cell
        
        if self.game.grid[row][col] != 0:
            self.status_label.configure(text="Cell is already filled!")
            return
        
        hint_number = self.game.solution[row][col]
        self.status_label.configure(text=f"Hint: The number for this cell is {hint_number}")
    
    def show_solution(self):
        result = messagebox.askyesno("Show Solution", 
                                   "Are you sure you want to see the complete solution?")
        if result:
            for i in range(9):
                for j in range(9):
                    self.cells[i][j].configure(text=str(self.game.solution[i][j]))
                    if self.original_grid[i][j] != 0:
                        self.cells[i][j].configure(fg=self.colors['text_fixed'])
                    else:
                        self.cells[i][j].configure(fg=self.colors['text_user'])
            
            self.status_label.configure(text="Complete solution displayed")

def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()