import pygame
pygame.init()

#setup
WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Grid settings
ROW = 10
COL = 10
CELL_SIZE = WIDTH // COL

#Tilemap
grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

#Player variables
player = pygame.Rect(50, 50, CELL_SIZE // 2, CELL_SIZE // 2) 
speed = 3
gravity = 0
max_fall = 8  
jump_height = -15  
velocity_y = 0  

#Collision check function
def is_solid(x, y, w, h):
    for dx in (0, w - 1):  # Left and right edges
        for dy in (0, h - 1):  # Top and bottom edges
            col = (x + dx) // CELL_SIZE
            row = (y + dy) // CELL_SIZE
            if 0 <= col < COL and 0 <= row < ROW:
                if grid[row][col] == 1:  # Solid block
                    return True
    return False


#Draws the grid
def draw_grid():
    for row in range(ROW):
        for col in range(COL):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            if grid[row][col] == 0:
                color = WHITE
            else:
                color = BLACK
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))


#Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Fill screen
    screen.fill(WHITE)

    #Player movement
    keys = pygame.key.get_pressed()

    #Horizontal movement
    if keys[pygame.K_LEFT]:
        if not is_solid(player.x - speed, player.y, player.width, player.height):
            player.x -= speed
    if keys[pygame.K_RIGHT]:
        if not is_solid(player.x + speed, player.y, player.width, player.height):
            player.x += speed

    #Jumping
    if keys[pygame.K_UP] and velocity_y == 0 and nospam==1: 
        nospam=0
        velocity_y = jump_height
    elif not keys[pygame.K_UP]:
        nospam=1
    #Gravity mechanics
    velocity_y += 1 
    velocity_y = min(velocity_y, max_fall)  

    #Move vertically
    if not is_solid(player.x, player.y + velocity_y, player.width, player.height):
        player.y += velocity_y 
    else:
        #Stop falling when landing on solid ground
        if velocity_y > 0: 
            while is_solid(player.x, player.y + 1, player.width, player.height):
                player.y -= 1
            velocity_y = 0 
        elif velocity_y < 0:  
            while is_solid(player.x, player.y, player.width, player.height):
                player.y += 1
            velocity_y = 0  


    #Draw everything
    draw_grid()
    pygame.draw.rect(screen, BLACK, player)  
    pygame.display.update()
    clock.tick(60)

pygame.quit()
