import sys
import random
from typing import Dict, List, Tuple, Set, Optional

import pygame
from pygame.locals import QUIT, KEYDOWN
from sudoku import Sudoku


class SudokuGame:
    """A Sudoku game implementation using Pygame."""
    
    # Constants
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    CELL_SIZE = 70
    GRID_OFFSET_X = 70
    GRID_OFFSET_Y = 20
    CELL_SPACING = 5
    FPS = 60
    
    # Colors
    WHITE = (255, 255, 255)
    GREEN = (0, 153, 0)
    LIGHT_GRAY = (192, 192, 192)
    DEEP_GRAY = (105, 105, 105)
    RED = (204, 0, 0)
    LIGHT_GREEN = (144, 238, 144)
    YELLOW = (255, 255, 0)
    
    # Game configuration
    VALID_NUMBERS = '123456789'
    GRID_SIZE = 9
    TOTAL_CELLS = GRID_SIZE * GRID_SIZE
    
    # Number popup configuration
    POPUP_RADIUS = 20
    POPUP_SPACING = 45
    POPUP_ALPHA = 180
    
    def __init__(self) -> None:
        """Initialize the Sudoku game."""
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Pygame Sudoku")
        
        # Fonts
        self.font = pygame.font.Font(None, 50)
        self.mini_font = pygame.font.SysFont("Arial", 20)
        
        # Game state
        self.clock = pygame.time.Clock()
        self.running = True
        self.is_complete = False
        self.time_elapsed = 0
        self.difficulty = 0.50
        
        # Number popup state
        self.show_popup = False
        self.popup_cell_index = -1
        self.popup_rects = []
        
        # Cell focus state
        self.focused_cell_index = -1
        
        # Double-click detection
        self.last_click_time = 0
        self.last_click_cell = -1
        self.DOUBLE_CLICK_DELAY = 300  # milliseconds
        
        # Initialize game components
        self._initialize_grid()
        self._initialize_game_state()
        self._initialize_ui_elements()
        self._initialize_validation_groups()
        
    def _initialize_grid(self) -> None:
        """Initialize the visual grid of input boxes."""
        self.input_boxes = []
        rect = pygame.Rect(self.GRID_OFFSET_X, self.GRID_OFFSET_Y, 
                          self.CELL_SIZE, self.CELL_SIZE)
        
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                copy = rect.copy()
                copy.top += ((self.CELL_SIZE * row) + (row // 3) * self.CELL_SPACING)
                copy.left += ((self.CELL_SIZE * col) + (col // 3) * self.CELL_SPACING)
                self.input_boxes.append(copy)
    
    def _initialize_game_state(self) -> None:
        """Initialize the game state dictionaries."""
        self.box_values = {i: '' for i in range(self.TOTAL_CELLS)}
        self.box_is_initial = {i: False for i in range(self.TOTAL_CELLS)}
        self.box_has_conflict = {i: False for i in range(self.TOTAL_CELLS)}
        self.box_multiple_values = {i: '' for i in range(self.TOTAL_CELLS)}
        self.box_is_uncertain = {i: False for i in range(self.TOTAL_CELLS)}
    
    def _initialize_ui_elements(self) -> None:
        """Initialize the UI elements (timer, difficulty, start button, reset button)."""
        self.timer_box = pygame.Rect(200, 700, 80, 35)
        self.difficulty_box = pygame.Rect(300, 700, 80, 35)
        self.start_button = pygame.Rect(400, 700, 80, 35)
        self.reset_button = pygame.Rect(500, 700, 80, 35)
    
    def _initialize_validation_groups(self) -> None:
        """Initialize the validation groups for Sudoku rules."""
        self.horizontal_groups = []
        self.vertical_groups = []
        self.nine_box_groups = []
        
        # Horizontal groups (rows)
        for i in range(self.GRID_SIZE):
            group = [x for x in range(self.GRID_SIZE * i, self.GRID_SIZE * (i + 1))]
            self.horizontal_groups.append(group)
        
        # Vertical groups (columns)
        for i in range(self.GRID_SIZE):
            group = [x for x in range(i, self.TOTAL_CELLS, self.GRID_SIZE)]
            self.vertical_groups.append(group)
        
        # 3x3 box groups
        for box_index in range(self.GRID_SIZE):
            group = []
            for cell_index in range(self.GRID_SIZE):
                row = box_index // 3 * 3 + cell_index // 3
                col = box_index % 3 * 3 + cell_index % 3
                index = row * self.GRID_SIZE + col
                group.append(index)
            self.nine_box_groups.append(group)
    
    def _validate_input(self, cell_index: int, group: List[int]) -> None:
        """Validate input against a group and mark conflicts."""
        for other_index in group:
            if cell_index == other_index:
                continue
            if (not self.box_is_initial[other_index] and 
                self.box_values[cell_index] == self.box_values[other_index] and 
                self.box_values[cell_index]):
                self.box_has_conflict[cell_index] = True
                self.box_has_conflict[other_index] = True
    
    def _validate_all_cells(self) -> None:
        """Validate all cells against Sudoku rules."""
        # Reset conflict flags
        self.box_has_conflict = {i: False for i in range(self.TOTAL_CELLS)}
        
        # Check each filled cell
        for cell_index, value in self.box_values.items():
            if value:
                # Check horizontal group
                self._validate_input(cell_index, self.horizontal_groups[cell_index // self.GRID_SIZE])
                # Check vertical group
                self._validate_input(cell_index, self.vertical_groups[cell_index % self.GRID_SIZE])
                # Check 3x3 box group
                for box_group in self.nine_box_groups:
                    if cell_index in box_group:
                        self._validate_input(cell_index, box_group)
                        break
    
    def _get_valid_numbers(self, cell_index: int) -> Set[str]:
        """Get set of valid numbers for a specific cell."""
        if self.box_is_initial[cell_index]:
            return set()
        
        valid_numbers = set(self.VALID_NUMBERS)
        
        # Check horizontal group
        for other_index in self.horizontal_groups[cell_index // self.GRID_SIZE]:
            if other_index != cell_index and self.box_values[other_index]:
                valid_numbers.discard(self.box_values[other_index])
        
        # Check vertical group
        for other_index in self.vertical_groups[cell_index % self.GRID_SIZE]:
            if other_index != cell_index and self.box_values[other_index]:
                valid_numbers.discard(self.box_values[other_index])
        
        # Check 3x3 box group
        for box_group in self.nine_box_groups:
            if cell_index in box_group:
                for other_index in box_group:
                    if other_index != cell_index and self.box_values[other_index]:
                        valid_numbers.discard(self.box_values[other_index])
                break
        
        return valid_numbers
    
    def _reset_user_input(self) -> None:
        """Reset all user-input numbers, keeping initial puzzle."""
        for i in range(self.TOTAL_CELLS):
            if not self.box_is_initial[i]:
                self.box_values[i] = ''
                self.box_multiple_values[i] = ''
                self.box_is_uncertain[i] = False
        
        # Reset conflicts and completion
        self.box_has_conflict = {i: False for i in range(self.TOTAL_CELLS)}
        self.is_complete = False
        self._validate_all_cells()
    
    def _generate_new_puzzle(self) -> None:
        """Generate a new Sudoku puzzle with current difficulty."""
        puzzle = Sudoku(3, 3, seed=random.randint(0, sys.maxsize - 1)).difficulty(self.difficulty)
        
        # Reset game state
        self.box_values = {i: '' for i in range(self.TOTAL_CELLS)}
        self.box_is_initial = {i: False for i in range(self.TOTAL_CELLS)}
        self.box_has_conflict = {i: False for i in range(self.TOTAL_CELLS)}
        self.box_multiple_values = {i: '' for i in range(self.TOTAL_CELLS)}
        self.box_is_uncertain = {i: False for i in range(self.TOTAL_CELLS)}
        
        # Fill initial values from puzzle
        index = 0
        for row in puzzle.board:
            for cell_value in row:
                if cell_value:
                    self.box_values[index] = str(cell_value)
                    self.box_is_initial[index] = True
                index += 1
        
        # Reset game state
        self.is_complete = False
        self.time_elapsed = 0
    
    def _handle_number_input(self, key: str) -> None:
        """Handle number key input for the focused cell."""
        if self.focused_cell_index != -1 and not self.box_is_initial[self.focused_cell_index]:
            # If cell is uncertain, clear uncertainty and set single value
            if self.box_is_uncertain[self.focused_cell_index]:
                self.box_is_uncertain[self.focused_cell_index] = False
                self.box_multiple_values[self.focused_cell_index] = ''
            
            self.box_values[self.focused_cell_index] = key
            self._validate_all_cells()
    
    def _handle_space_input(self) -> None:
        """Handle space key input for filling multiple valid numbers."""
        if self.focused_cell_index != -1 and not self.box_is_initial[self.focused_cell_index]:
            valid_numbers = self._get_valid_numbers(self.focused_cell_index)
            
            if len(valid_numbers) > 1:
                # Clear single value and set multiple values
                self.box_values[self.focused_cell_index] = ''
                self.box_multiple_values[self.focused_cell_index] = ''.join(sorted(valid_numbers))
                self.box_is_uncertain[self.focused_cell_index] = True
                self._validate_all_cells()
    
    def _handle_mouse_wheel(self, direction: int) -> None:
        """Handle mouse wheel input for difficulty adjustment."""
        if direction == 1:  # wheel up
            self.difficulty += 0.01
        elif direction == -1:  # wheel down
            self.difficulty -= 0.01
        
        # Clamp difficulty values
        self.difficulty = max(0.01, min(0.99, self.difficulty))
    
    def _check_completion(self) -> None:
        """Check if the puzzle is completed."""
        if self.is_complete:
            return
        
        # Check if there are any uncertain cells
        if any(self.box_is_uncertain.values()):
            return
        
        total = 0
        for value in self.box_values.values():
            total += int(value) if value else 0
        
        # Check if all cells are filled and no conflicts
        self.is_complete = (total == 45 * self.GRID_SIZE and 
                          not any(self.box_has_conflict.values()))
    
    def _draw_grid(self, mouse_pos: Tuple[int, int]) -> None:
        """Draw the Sudoku grid."""
        for i, box in enumerate(self.input_boxes):
            # Determine box color
            if self.box_is_initial[i]:
                bg_color = self.LIGHT_GRAY
            else:
                bg_color = self.WHITE
            
            # Draw box background
            pygame.draw.rect(self.screen, bg_color, box)
            
            # Determine border color and width
            if self.show_popup and i == self.popup_cell_index:
                # Keep the popup cell highlighted
                border_color = self.GREEN
                border_width = 2
            elif i == self.focused_cell_index:
                # Focused cell
                if self.box_is_uncertain[i]:
                    # Uncertain cell has yellow border
                    border_color = self.YELLOW
                    border_width = 2
                else:
                    # Normal focused cell has green border
                    border_color = self.GREEN
                    border_width = 2
            elif self.box_is_uncertain[i]:
                # Uncertain but not focused has yellow border
                border_color = self.YELLOW
                border_width = 1
            elif box.collidepoint(mouse_pos) and not self.box_is_initial[i] and not self.show_popup:
                # Hover effect: just thicker border
                border_color = self.DEEP_GRAY
                border_width = 2
            else:
                border_color = self.DEEP_GRAY
                border_width = 1
            
            # Draw box border
            pygame.draw.rect(self.screen, border_color, box, border_width, 3)
            
            # Draw number(s)
            if self.box_values[i]:
                # Single number
                text_color = self.RED if self.box_has_conflict[i] else self.DEEP_GRAY
                text_surface = self.font.render(self.box_values[i], True, text_color)
                text_rect = text_surface.get_rect(center=box.center)
                self.screen.blit(text_surface, text_rect)
            elif self.box_multiple_values[i] and self.box_is_uncertain[i]:
                # Multiple numbers in uncertain state
                self._draw_multiple_numbers(box, self.box_multiple_values[i])
    
    def _draw_multiple_numbers(self, box: pygame.Rect, numbers: str) -> None:
        """Draw multiple numbers in a cell with automatic spacing."""
        if not numbers:
            return
        
        # Use smaller font for multiple numbers
        small_font = pygame.font.Font(None, 20)
        
        # Calculate layout based on number of digits
        num_count = len(numbers)
        
        if num_count <= 3:
            # Horizontal layout for 1-3 numbers
            total_width = box.width - 10
            spacing = total_width // (num_count + 1)
            for i, num in enumerate(numbers):
                x = box.left + spacing * (i + 1)
                y = box.centery
                text_surface = small_font.render(num, True, self.DEEP_GRAY)
                text_rect = text_surface.get_rect(center=(x, y))
                self.screen.blit(text_surface, text_rect)
        
        elif num_count <= 6:
            # Two rows for 4-6 numbers
            numbers_per_row = (num_count + 1) // 2
            total_width = box.width - 10
            spacing = total_width // (numbers_per_row + 1)
            
            for i, num in enumerate(numbers):
                row = i // numbers_per_row
                col = i % numbers_per_row
                x = box.left + spacing * (col + 1)
                y = box.centery + (row - 0.5) * 25
                text_surface = small_font.render(num, True, self.DEEP_GRAY)
                text_rect = text_surface.get_rect(center=(x, y))
                self.screen.blit(text_surface, text_rect)
        
        else:
            # 3x3 grid for 7-9 numbers
            positions = [
                (box.left + box.width * 0.25, box.top + box.height * 0.25),
                (box.centerx, box.top + box.height * 0.25),
                (box.left + box.width * 0.75, box.top + box.height * 0.25),
                (box.left + box.width * 0.25, box.centery),
                (box.centerx, box.centery),
                (box.left + box.width * 0.75, box.centery),
                (box.left + box.width * 0.25, box.top + box.height * 0.75),
                (box.centerx, box.top + box.height * 0.75),
                (box.left + box.width * 0.75, box.top + box.height * 0.75),
            ]
            
            for i, num in enumerate(numbers):
                if i < len(positions):
                    x, y = positions[i]
                    text_surface = small_font.render(num, True, self.DEEP_GRAY)
                    text_rect = text_surface.get_rect(center=(x, y))
                    self.screen.blit(text_surface, text_rect)
    
    def _show_number_popup(self, cell_index: int) -> None:
        """Show number popup for a specific cell."""
        if self.box_is_initial[cell_index]:
            return
        
        self.show_popup = True
        self.popup_cell_index = cell_index
        self.popup_rects = []
        
        # Calculate popup position
        cell_rect = self.input_boxes[cell_index]
        center_x = cell_rect.centerx
        center_y = cell_rect.centery
        
        # Create popup circles in 3x3 grid
        for i in range(9):
            row = i // 3
            col = i % 3
            
            # Calculate position relative to cell
            offset_x = (col - 1) * self.POPUP_SPACING
            offset_y = (row - 1) * self.POPUP_SPACING
            
            popup_x = center_x + offset_x
            popup_y = center_y + offset_y
            
            # Create popup rect
            popup_rect = pygame.Rect(popup_x - self.POPUP_RADIUS, 
                                   popup_y - self.POPUP_RADIUS,
                                   self.POPUP_RADIUS * 2, 
                                   self.POPUP_RADIUS * 2)
            self.popup_rects.append(popup_rect)
    
    def _hide_number_popup(self) -> None:
        """Hide number popup."""
        self.show_popup = False
        self.popup_cell_index = -1
        self.popup_rects = []
    
    def _draw_number_popup(self) -> None:
        """Draw number popup if active."""
        if not self.show_popup or self.popup_cell_index == -1:
            return
        
        # Get valid numbers for this cell
        valid_numbers = self._get_valid_numbers(self.popup_cell_index)
        
        # Draw semi-transparent background
        popup_surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        popup_surface.fill((255, 255, 255, self.POPUP_ALPHA))
        self.screen.blit(popup_surface, (0, 0))
        
        # Draw number circles
        for i, rect in enumerate(self.popup_rects):
            number = str(i + 1)
            
            # Determine color based on validity
            if number in valid_numbers:
                color = self.LIGHT_GREEN
                text_color = self.DEEP_GRAY
            else:
                color = self.RED
                text_color = self.WHITE
            
            # Draw circle
            pygame.draw.circle(self.screen, color, rect.center, self.POPUP_RADIUS)
            pygame.draw.circle(self.screen, self.DEEP_GRAY, rect.center, self.POPUP_RADIUS, 2)
            
            # Draw number
            text_surface = self.font.render(number, True, text_color)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)
    
    def _handle_popup_click(self, mouse_pos: Tuple[int, int]) -> bool:
        """Handle click on number popup. Returns True if a number was selected."""
        if not self.show_popup:
            return False
        
        for i, rect in enumerate(self.popup_rects):
            if rect.collidepoint(mouse_pos):
                number = str(i + 1)
                self.box_values[self.popup_cell_index] = number
                self.box_multiple_values[self.popup_cell_index] = ''
                self.box_is_uncertain[self.popup_cell_index] = False
                self._validate_all_cells()
                self._hide_number_popup()
                return True
        
        # Click outside popup closes it
        self._hide_number_popup()
        return False
    
    def _draw_ui_elements(self, mouse_pos: Tuple[int, int]) -> None:
        """Draw UI elements (timer, difficulty, start button)."""
        # Draw timer
        timer_color = self.GREEN if self.is_complete else self.DEEP_GRAY
        pygame.draw.rect(self.screen, timer_color, self.timer_box, 1, 3)
        
        elapsed_seconds = self.time_elapsed // 1000
        minutes = str(elapsed_seconds // 60).zfill(2)
        seconds = str(elapsed_seconds % 60).zfill(2)
        
        timer_text = self.mini_font.render(f'{minutes}:{seconds}', True, timer_color)
        timer_rect = timer_text.get_rect(center=self.timer_box.center)
        self.screen.blit(timer_text, timer_rect)
        
        # Draw difficulty box
        diff_bg_color = self.LIGHT_GRAY if self.difficulty_box.collidepoint(mouse_pos) else self.WHITE
        pygame.draw.rect(self.screen, diff_bg_color, self.difficulty_box)
        pygame.draw.rect(self.screen, self.DEEP_GRAY, self.difficulty_box, 1, 3)
        
        diff_text = self.mini_font.render(f'{self.difficulty:.2f}', True, self.DEEP_GRAY)
        diff_rect = diff_text.get_rect(center=self.difficulty_box.center)
        self.screen.blit(diff_text, diff_rect)
        
        # Draw start button
        start_bg_color = self.LIGHT_GRAY if self.start_button.collidepoint(mouse_pos) else self.WHITE
        pygame.draw.rect(self.screen, start_bg_color, self.start_button)
        pygame.draw.rect(self.screen, self.DEEP_GRAY, self.start_button, 1, 3)
        
        start_text = self.mini_font.render('start', True, self.DEEP_GRAY)
        start_rect = start_text.get_rect(center=self.start_button.center)
        self.screen.blit(start_text, start_rect)
        
        # Draw reset button
        reset_bg_color = self.LIGHT_GRAY if self.reset_button.collidepoint(mouse_pos) else self.WHITE
        pygame.draw.rect(self.screen, reset_bg_color, self.reset_button)
        pygame.draw.rect(self.screen, self.DEEP_GRAY, self.reset_button, 1, 3)
        
        reset_text = self.mini_font.render('reset', True, self.DEEP_GRAY)
        reset_rect = reset_text.get_rect(center=self.reset_button.center)
        self.screen.blit(reset_text, reset_rect)
    
    def run(self) -> None:
        """Main game loop."""
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                
                elif event.type == KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.show_popup:
                            # Close popup and fill multiple numbers
                            self._hide_number_popup()
                            self._handle_space_input()
                        else:
                            self._handle_space_input()
                    elif event.unicode in self.VALID_NUMBERS:
                        self._handle_number_input(event.unicode)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        if self.show_popup:
                            self._handle_popup_click(mouse_pos)
                        elif self.start_button.collidepoint(mouse_pos):
                            self._generate_new_puzzle()
                        elif self.reset_button.collidepoint(mouse_pos):
                            self._reset_user_input()
                        else:
                            # Check if click is on a cell for focusing
                            current_time = pygame.time.get_ticks()
                            for i, box in enumerate(self.input_boxes):
                                if box.collidepoint(mouse_pos) and not self.box_is_initial[i]:
                                    # Check for double-click
                                    if (i == self.last_click_cell and 
                                        current_time - self.last_click_time < self.DOUBLE_CLICK_DELAY):
                                        # Double-click: clear the cell
                                        self.box_values[i] = ''
                                        self.box_multiple_values[i] = ''
                                        self.box_is_uncertain[i] = False
                                        self._validate_all_cells()
                                        self.focused_cell_index = i
                                    else:
                                        # Single-click: focus the cell
                                        self.focused_cell_index = i
                                    
                                    self.last_click_cell = i
                                    self.last_click_time = current_time
                                    break
                            else:
                                # Click outside any cell, remove focus
                                self.focused_cell_index = -1
                                self.last_click_cell = -1
                    
                    elif event.button == 3:  # Right click
                        if not self.show_popup:
                            # Check if click is on a cell
                            for i, box in enumerate(self.input_boxes):
                                if box.collidepoint(mouse_pos) and not self.box_is_initial[i]:
                                    self._show_number_popup(i)
                                    self.focused_cell_index = i
                                    break
                    
                    elif event.button == 4:  # Mouse wheel up
                        if self.difficulty_box.collidepoint(mouse_pos):
                            self._handle_mouse_wheel(1)
                    
                    elif event.button == 5:  # Mouse wheel down
                        if self.difficulty_box.collidepoint(mouse_pos):
                            self._handle_mouse_wheel(-1)
            
            # Update game state
            if not self.is_complete:
                self._check_completion()
                self.time_elapsed += self.clock.tick(self.FPS)
            else:
                self.clock.tick(self.FPS)
            
            # Draw everything
            self.screen.fill(self.WHITE)
            self._draw_grid(mouse_pos)
            self._draw_ui_elements(mouse_pos)
            self._draw_number_popup()
            pygame.display.flip()
        
        pygame.quit()


def main() -> None:
    """Entry point for the Sudoku game."""
    game = SudokuGame()
    game.run()


if __name__ == "__main__":
    main()
