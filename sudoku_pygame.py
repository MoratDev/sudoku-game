import pygame
import sys
from sudoku_game import SudokuGame
import copy

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 900
GRID_SIZE = 540
CELL_SIZE = GRID_SIZE // 9
GRID_OFFSET_X = (WINDOW_WIDTH - GRID_SIZE) // 2
GRID_OFFSET_Y = 150

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (220, 220, 220)
BLUE = (33, 150, 243)
LIGHT_BLUE = (227, 242, 253)
GREEN = (76, 175, 80)
ORANGE = (255, 152, 0)
PURPLE = (156, 39, 176)
RED = (244, 67, 54)
DARK_GRAY = (64, 64, 64)

class SudokuPygame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Sudoku Game")
        
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)
        
        self.game = SudokuGame()
        self.selected_cell = None
        self.original_grid = None
        self.difficulty = "medium"
        self.status_message = "Press 'N' for New Game, arrow keys to select, number keys to input"
        
        # Button rectangles
        self.buttons = {
            'new_game': pygame.Rect(50, 50, 120, 40),
            'easy': pygame.Rect(200, 50, 80, 40),
            'medium': pygame.Rect(290, 50, 80, 40),
            'hard': pygame.Rect(380, 50, 80, 40),
            'expert': pygame.Rect(470, 50, 80, 40),
            'hint': pygame.Rect(580, 50, 80, 40),
            'solution': pygame.Rect(670, 50, 80, 40)
        }
        
        self.running = True
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)
    
    def handle_keydown(self, event):
        # Number input (1-9)
        if pygame.K_1 <= event.key <= pygame.K_9:
            number = event.key - pygame.K_0
            self.input_number(number)
        
        # Keypad numbers
        elif pygame.K_KP1 <= event.key <= pygame.K_KP9:
            number = event.key - pygame.K_KP0
            self.input_number(number)
        
        # Arrow key navigation
        elif event.key == pygame.K_UP:
            self.move_selection(0, -1)
        elif event.key == pygame.K_DOWN:
            self.move_selection(0, 1)
        elif event.key == pygame.K_LEFT:
            self.move_selection(-1, 0)
        elif event.key == pygame.K_RIGHT:
            self.move_selection(1, 0)
        
        # Clear cell
        elif event.key in [pygame.K_DELETE, pygame.K_BACKSPACE, pygame.K_0]:
            self.clear_cell()
        
        # New game
        elif event.key == pygame.K_n:
            self.new_game()
        
        # Hint
        elif event.key == pygame.K_h:
            self.get_hint()
        
        # Solution
        elif event.key == pygame.K_s:
            self.show_solution()
        
        # Difficulty selection
        elif event.key == pygame.K_1:
            self.difficulty = "easy"
            self.status_message = "Difficulty set to Easy"
        elif event.key == pygame.K_2:
            self.difficulty = "medium"
            self.status_message = "Difficulty set to Medium"
        elif event.key == pygame.K_3:
            self.difficulty = "hard"
            self.status_message = "Difficulty set to Hard"
        elif event.key == pygame.K_4:
            self.difficulty = "expert"
            self.status_message = "Difficulty set to Expert"
    
    def handle_mouse_click(self, pos):
        # Check button clicks
        for button_name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                self.handle_button_click(button_name)
                return
        
        # Check grid clicks
        grid_x = pos[0] - GRID_OFFSET_X
        grid_y = pos[1] - GRID_OFFSET_Y
        
        if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
            col = grid_x // CELL_SIZE
            row = grid_y // CELL_SIZE
            if 0 <= row < 9 and 0 <= col < 9:
                self.selected_cell = (row, col)
                self.status_message = f"Selected cell: Row {row+1}, Column {col+1}"
    
    def handle_button_click(self, button_name):
        if button_name == 'new_game':
            self.new_game()
        elif button_name in ['easy', 'medium', 'hard', 'expert']:
            self.difficulty = button_name
            self.status_message = f"Difficulty set to {button_name.capitalize()}"
        elif button_name == 'hint':
            self.get_hint()
        elif button_name == 'solution':
            self.show_solution()
    
    def move_selection(self, dx, dy):
        if self.selected_cell is None:
            self.selected_cell = (0, 0)
        else:
            row, col = self.selected_cell
            new_row = max(0, min(8, row + dy))
            new_col = max(0, min(8, col + dx))
            self.selected_cell = (new_row, new_col)
        
        row, col = self.selected_cell
        self.status_message = f"Selected cell: Row {row+1}, Column {col+1}"
    
    def input_number(self, number):
        if not self.selected_cell:
            self.status_message = "Please select a cell first!"
            return
        
        if not self.original_grid:
            self.status_message = "Please start a new game first!"
            return
        
        row, col = self.selected_cell
        
        # Check if cell is fixed
        if self.original_grid[row][col] != 0:
            self.status_message = "Cannot modify fixed cells!"
            return
        
        # Make the move
        if self.game.make_move(row, col, number):
            self.status_message = f"Placed {number} in cell ({row+1}, {col+1})"
            
            # Check for win
            if self.game.is_complete():
                if self.game.is_valid_solution():
                    self.status_message = "🎉 Congratulations! You solved the puzzle!"
        else:
            self.status_message = f"Invalid move! {number} conflicts with Sudoku rules."
    
    def clear_cell(self):
        if not self.selected_cell:
            self.status_message = "Please select a cell first!"
            return
        
        if not self.original_grid:
            self.status_message = "Please start a new game first!"
            return
        
        row, col = self.selected_cell
        
        # Check if cell is fixed
        if self.original_grid[row][col] != 0:
            self.status_message = "Cannot clear fixed cells!"
            return
        
        # Clear the cell
        self.game.grid[row][col] = 0
        self.status_message = f"Cleared cell ({row+1}, {col+1})"
    
    def new_game(self):
        self.game.create_puzzle(self.difficulty)
        self.original_grid = copy.deepcopy(self.game.grid)
        self.selected_cell = (0, 0)
        
        empty_cells = sum(1 for i in range(9) for j in range(9) if self.game.grid[i][j] == 0)
        self.status_message = f"New {self.difficulty} puzzle generated! {empty_cells} empty cells."
    
    def get_hint(self):
        if not self.selected_cell:
            self.status_message = "Please select a cell for hint!"
            return
        
        if not self.original_grid:
            self.status_message = "Please start a new game first!"
            return
        
        row, col = self.selected_cell
        
        if self.game.grid[row][col] != 0:
            self.status_message = "Cell is already filled!"
            return
        
        hint_number = self.game.solution[row][col]
        self.status_message = f"Hint: The number for this cell is {hint_number}"
    
    def show_solution(self):
        if not self.original_grid:
            self.status_message = "Please start a new game first!"
            return
        
        self.game.grid = copy.deepcopy(self.game.solution)
        self.status_message = "Complete solution displayed"
    
    def draw_grid(self):
        # Draw grid background
        grid_rect = pygame.Rect(GRID_OFFSET_X, GRID_OFFSET_Y, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(self.screen, WHITE, grid_rect)
        
        # Draw cells
        for row in range(9):
            for col in range(9):
                x = GRID_OFFSET_X + col * CELL_SIZE
                y = GRID_OFFSET_Y + row * CELL_SIZE
                cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                
                # Cell background color
                if self.selected_cell == (row, col):
                    pygame.draw.rect(self.screen, LIGHT_BLUE, cell_rect)
                elif self.original_grid and self.original_grid[row][col] != 0:
                    pygame.draw.rect(self.screen, LIGHT_GRAY, cell_rect)
                else:
                    pygame.draw.rect(self.screen, WHITE, cell_rect)
                
                # Cell border
                border_width = 1
                if row % 3 == 0:  # Top border of 3x3 boxes
                    pygame.draw.line(self.screen, BLACK, (x, y), (x + CELL_SIZE, y), 3)
                if col % 3 == 0:  # Left border of 3x3 boxes
                    pygame.draw.line(self.screen, BLACK, (x, y), (x, y + CELL_SIZE), 3)
                if row == 8:  # Bottom border
                    pygame.draw.line(self.screen, BLACK, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 3)
                if col == 8:  # Right border
                    pygame.draw.line(self.screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 3)
                
                pygame.draw.rect(self.screen, GRAY, cell_rect, border_width)
                
                # Draw number
                if self.game.grid and self.game.grid[row][col] != 0:
                    number = str(self.game.grid[row][col])
                    
                    # Color based on whether it's original or user input
                    if self.original_grid and self.original_grid[row][col] != 0:
                        color = BLACK  # Fixed numbers
                    else:
                        color = BLUE  # User input
                    
                    text_surface = self.font_large.render(number, True, color)
                    text_rect = text_surface.get_rect(center=cell_rect.center)
                    self.screen.blit(text_surface, text_rect)
    
    def draw_buttons(self):
        # Draw buttons
        for button_name, rect in self.buttons.items():
            # Button color
            if button_name == 'new_game':
                color = GREEN
            elif button_name in ['easy', 'medium', 'hard', 'expert']:
                color = BLUE if button_name == self.difficulty else GRAY
            elif button_name == 'hint':
                color = ORANGE
            elif button_name == 'solution':
                color = PURPLE
            
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)
            
            # Button text
            text = button_name.replace('_', ' ').title()
            text_surface = self.font_small.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)
    
    def draw_instructions(self):
        instructions = [
            "Keyboard Controls:",
            "• Arrow keys: Navigate cells",
            "• 1-9: Input numbers",
            "• Delete/Backspace/0: Clear cell",
            "• N: New game",
            "• H: Get hint",
            "• S: Show solution"
        ]
        
        y_start = GRID_OFFSET_Y + GRID_SIZE + 30
        for i, instruction in enumerate(instructions):
            text_surface = self.font_small.render(instruction, True, DARK_GRAY)
            self.screen.blit(text_surface, (50, y_start + i * 25))
    
    def draw_status(self):
        status_rect = pygame.Rect(50, GRID_OFFSET_Y + GRID_SIZE + 200, WINDOW_WIDTH - 100, 40)
        pygame.draw.rect(self.screen, LIGHT_GRAY, status_rect)
        pygame.draw.rect(self.screen, GRAY, status_rect, 2)
        
        text_surface = self.font_medium.render(self.status_message, True, BLACK)
        text_rect = text_surface.get_rect(center=status_rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def draw_title(self):
        title_text = "🧩 SUDOKU GAME"
        title_surface = pygame.font.Font(None, 48).render(title_text, True, DARK_GRAY)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 25))
        self.screen.blit(title_surface, title_rect)
    
    def draw(self):
        self.screen.fill(WHITE)
        self.draw_title()
        self.draw_buttons()
        self.draw_grid()
        self.draw_instructions()
        self.draw_status()
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

def main():
    game = SudokuPygame()
    game.run()

if __name__ == "__main__":
    main()