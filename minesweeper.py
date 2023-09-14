import random
import enum
import pygame

pygame.init()

# Set game constants
FRAMES_PER_SECOND = 10
NUM_MINES = 8

# Set game window dimensions
grid_size_horizontal = 10
grid_size_vertical = 10
game_size = 50
top_border = 90
other_border = 30
display_horizontal = (game_size * grid_size_horizontal) + (other_border * 2)
display_vertical = (game_size * grid_size_vertical) + other_border + top_border

# Create Pygame display and timer
pygame_display = pygame.display.set_mode((display_horizontal, display_vertical))
pygame_timer = pygame.time.Clock()
pygame.display.set_caption("Minesweeper")

# Define colors
white_color = (255, 255, 255)
light_gray_color = (192, 192, 192)
dark_gray_color = (128, 128, 128)
black_color = (0, 0, 0)

# Load sprites
sprite_flag = pygame.image.load("sprites/large_icons/flag.png")
sprite_grid_default = pygame.image.load("sprites/large_icons/grid_default.png").convert()
sprite_grid_empty = pygame.image.load("sprites/large_icons/grid_empty.png")
sprite_grid1 = pygame.image.load("sprites/large_icons/grid1.png")
sprite_grid2 = pygame.image.load("sprites/large_icons/grid2.png")
sprite_grid3 = pygame.image.load("sprites/large_icons/grid3.png")
sprite_grid4 = pygame.image.load("sprites/large_icons/grid4.png")
sprite_grid5 = pygame.image.load("sprites/large_icons/grid5.png")
sprite_grid6 = pygame.image.load("sprites/large_icons/grid6.png")
sprite_grid7 = pygame.image.load("sprites/large_icons/grid7.png")
sprite_grid8 = pygame.image.load("sprites/large_icons/grid8.png")
sprite_mine_clicked = pygame.image.load("sprites/large_icons/mine_clicked.png")
sprite_mine_default = pygame.image.load("sprites/large_icons/mine_default.png")
sprite_mine_false = pygame.image.load("sprites/large_icons/mine_false.png")

# Define global grid squares and mine location arrays
game_grid = []
mine_locations = []
num_mines_remaining = NUM_MINES

# Define enum to track game state
class GameState(enum.Enum):
    WIN = 0
    LOSS = 1
    PLAY = 2
    STOP = 4

# Define class to represent each grid square
class GridIcon:
    def __init__(self, x_pos, y_pos, type):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.type = type
        self.clicked = False
        self.mine_clicked = False
        self.mine_false = False
        self.flag = False
        left = other_border + (x_pos * game_size)
        top = top_border + (y_pos * game_size)
        self.rect = pygame.Rect(left, top, game_size, game_size)

    # Update the sprite based on the state of the grid icon
    def update_icon(self):
        if self.clicked:
            if self.type == 0:
                pygame_display.blit(sprite_grid_empty, self.rect)
            elif self.type == 1:
                pygame_display.blit(sprite_grid1, self.rect)
            elif self.type == 2:
                pygame_display.blit(sprite_grid2, self.rect)
            elif self.type == 3:
                pygame_display.blit(sprite_grid3, self.rect)
            elif self.type == 4:
                pygame_display.blit(sprite_grid4, self.rect)
            elif self.type == 5:
                pygame_display.blit(sprite_grid5, self.rect)
            elif self.type == 6:
                pygame_display.blit(sprite_grid6, self.rect)
            elif self.type == 7:
                pygame_display.blit(sprite_grid7, self.rect)
            elif self.type == 8:
                pygame_display.blit(sprite_grid8, self.rect)
            if self.type == -1:
                if self.mine_clicked:
                    pygame_display.blit(sprite_mine_clicked, self.rect)
                else:
                    pygame_display.blit(sprite_mine_default, self.rect)
        elif self.mine_false:
            pygame_display.blit(sprite_mine_false, self.rect)
        elif self.flag:
            pygame_display.blit(sprite_flag, self.rect)
        else:
            pygame_display.blit(sprite_grid_default, self.rect)

    # Check whether a given X offset is in range for the grid icon's position
    def x_offset_is_in_range(self, x_offset):
        current_x_pos = self.x_pos + x_offset
        return (current_x_pos >= 0 and current_x_pos < grid_size_horizontal)

    # Check whether a given Y offset is in range for the grid icon's position
    def y_offset_is_in_range(self, y_offset):
        current_y_pos = self.y_pos + y_offset
        return (current_y_pos >= 0 and current_y_pos < grid_size_vertical)

    # Reveal the type of a grid icon after being clicked
    def reveal(self):
        self.clicked = True
        if self.flag:
            global num_mines_remaining
            num_mines_remaining += 1
        # If grid icon has no neighboring mines, reveal all neighboring icons
        if self.type == 0:
            for x in neighbor_range():
                if self.x_offset_is_in_range(x):
                    for y in neighbor_range():
                        if self.y_offset_is_in_range(y):
                            current_grid_icon = game_grid[self.y_pos + y][self.x_pos + x]
                            if not current_grid_icon.clicked:
                                current_grid_icon.reveal()
        # If a grind icon is a mine, reveal all other mines (game is lost)
        elif self.type == -1:
            for mine_location in mine_locations:
                if not game_grid[mine_location[1]][mine_location[0]].clicked:
                    game_grid[mine_location[1]][mine_location[0]].reveal()

    # Check all neighboring icons and update the type of the current grid icon
    def update_type(self):
        if self.type != -1:
            for x in neighbor_range():
                if self.x_offset_is_in_range(x):
                    for y in neighbor_range():
                        if self.y_offset_is_in_range(y):
                            if game_grid[self.y_pos + y][self.x_pos + x].type == -1:
                                self.type += 1

# Return a range for checking neighboring icons (-1, 0, 1)
def neighbor_range():
    return range(-1, 2)

# Display a given text string, in a given size, at a given position
def display_text(text, text_size, center_x, center_y):
    text_font = pygame.font.SysFont("inkfree", text_size, True)
    text_to_display = text_font.render(text, True, white_color, black_color)
    rect = text_to_display.get_rect()
    rect.center = (center_x, center_y)
    pygame_display.blit(text_to_display, rect)

# Start Minesweeper gameplay
def play_minesweeper():
    print("Starting Minesweeper...")
    game_state = GameState.PLAY
    global num_mines_remaining
    num_mines_remaining = NUM_MINES
    global game_grid
    game_grid = []
    global mine_locations
    mine_locations = []
    current_time = 0
    current_time_text = "0"

    # Generate random positions for all mines
    while len(mine_locations) < NUM_MINES:
        picked_pos = [random.randrange(0, grid_size_horizontal), random.randrange(0, grid_size_vertical)]
        if picked_pos not in mine_locations:
            mine_locations.append(picked_pos)

    # Create a new grid icon instance for every position
    for row_index in range(grid_size_horizontal):
        row = []
        for col_index in range(grid_size_vertical):
            type = 0
            if [col_index, row_index] in mine_locations:
                type = -1
            row.append(GridIcon(col_index, row_index, type))
        game_grid.append(row)

    # Update the types of each grid icon based on the mine locations
    for grid_row in game_grid:
        for grid_icon in grid_row:
            grid_icon.update_type()

    # Run gameplay loop while the game state is anything other than STOP
    while game_state != GameState.STOP:
        pygame_display.fill(light_gray_color)

        for event in pygame.event.get():
            # Quit if a QUIT event is received
            if event.type == pygame.QUIT:
                print("Game state set to STOP because you quit")
                game_state = GameState.STOP
            # Restart gameplay loop if player won or lost and pressed any key
            elif game_state == GameState.WIN or game_state == GameState.LOSS:
                if event.type == pygame.KEYDOWN:
                    print("Game state set to STOP because you pressed a key")
                    game_state = GameState.STOP
                    play_minesweeper()
            # Adjust grid icon state if a grid icon is clicked
            elif event.type == pygame.MOUSEBUTTONUP:
                for grid_row in game_grid:
                    for grid_icon in grid_row:
                        # Check if the click location collides with a grid icon
                        if grid_icon.rect.collidepoint(event.pos):
                            # Reveal the icon if there is a left click
                            if event.button == 1:
                                grid_icon.reveal()
                                if grid_icon.type == -1:
                                    print("Game state set to LOSS because you lost")
                                    game_state = GameState.LOSS
                                    grid_icon.mine_clicked = True
                            # Toggle flag if there is a right click
                            elif event.button == 3:
                                if not grid_icon.clicked:
                                    if grid_icon.flag:
                                        grid_icon.flag = False
                                        num_mines_remaining += 1
                                    else:
                                        grid_icon.flag = True
                                        num_mines_remaining -= 1

        # Check whether the game was won
        won_game = True
        for grid_row in game_grid:
            for grid_icon in grid_row:
                grid_icon.update_icon()
                # The game is not yet won if there still exists non-mines unclicked
                if grid_icon.type != -1 and not grid_icon.clicked:
                    won_game = False

        # Set game state to WIN if the game was won
        if won_game and game_state != GameState.STOP:
            print("Game state set to WIN because you won")
            game_state = GameState.WIN

        # Increment time if the game is still being played
        if game_state == GameState.PLAY:
            current_time += 1
            current_time_text = str(current_time // FRAMES_PER_SECOND)
        # Display game loss text if the game has been lost
        elif game_state == GameState.LOSS:
            display_text("You Lost!", 60, (grid_size_horizontal * game_size / 2 + other_border), (grid_size_vertical * game_size / 2 + top_border))
            display_text("Press any key to restart.", 30, (grid_size_horizontal * game_size / 2 + other_border), (grid_size_vertical * game_size / 2 + top_border + 30))

            for grid_row in game_grid:
                for grid_icon in grid_row:
                    if grid_icon.flag and grid_icon.type != -1:
                        grid_icon.mine_false = True
        # Display game win text if the game has been won
        elif game_state == GameState.WIN:
            display_text("You Won " + "In " + current_time_text + " Secs!", 60, (grid_size_horizontal * game_size / 2 + other_border), (grid_size_vertical * game_size / 2 + top_border))
            display_text("Press any key to restart.", 30, (grid_size_horizontal * game_size / 2 + other_border), (grid_size_vertical * game_size / 2 + top_border + 30))

        # Display current time in seconds
        display_text(current_time_text + " secs.", 40, other_border + 40, other_border)

        # Display number of mines remaining
        num_mines_text = str(num_mines_remaining) + " mines"
        if num_mines_remaining < 0:
            num_mines_text = "Flag check"
        display_text(num_mines_text, 40, display_horizontal - other_border - 60, other_border)

        pygame.display.update()

        pygame_timer.tick(FRAMES_PER_SECOND)

play_minesweeper()

print("Quitting Minesweeper...")
pygame.quit()
quit()
