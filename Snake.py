# Imports
import queue
import random
import sys
import threading
import time
import keyboard

# Configuration Variables
grid_size = (20, 5)
time_limit = 24000
frame_time = 0.3
snake_extra_length = 2

# Logic Variables
head = (random.randint(0, grid_size[0] - 1), random.randint(0, grid_size[1] - 1))
snake = [(head[0], head[1])]
input_queue = queue.Queue()
direction = (1, 0)
last_key = None

# Input Threading Logic
def player_input():
    global last_key
    while True:
        key = None
        if keyboard.is_pressed('w'):
            key = (0, -1)
        elif keyboard.is_pressed('a'):
            key = (-1, 0)
        elif keyboard.is_pressed('s'):
            key = (0, 1)
        elif keyboard.is_pressed('d'):
            key = (1, 0)
        if key is not None:
            if key != last_key:
                input_queue.put(key)
                last_key = key
        else:
            last_key = None
        time.sleep(0.05)

# Game Start Logic
if snake_extra_length > 0:
    for i in range(snake_extra_length):
        if head[0] - (i + 1) >= 0:
            snake.append((head[0] - (i + 1), head[1]))
        else:
            snake.append((grid_size[0] - (i + 1), head[1]))
free_list = [(x, y) for y in range(grid_size[1]) for x in range(grid_size[0]) if (x, y) not in snake]
food = free_list[random.randrange(len(free_list))]
t = threading.Thread(target=player_input, daemon=True)
t.start()

# Main Logic Updating Loop
for step in range(time_limit):
    # Input Logic
    while not input_queue.empty():
        new_direction = input_queue.get()
        if new_direction[0] + direction[0] != 0 or new_direction[1] + direction[1] != 0:
            direction = new_direction

    # Dynamic Positioning Logic
    new_head = (head[0] + direction[0], head[1] + direction[1])
    if direction[0] != 0:
        if 0 > new_head[0]:
            new_head = (grid_size[0] - 1, head[1])
        elif new_head[0] >= grid_size[0]:
            new_head = (0, head[1])
    else:
        if 0 > new_head[1]:
            new_head = (head[0], grid_size[1] - 1)
        elif new_head[1] >= grid_size[1]:
            new_head = (head[0], 0)
    head = new_head
    snake.insert(0, head)
    if head != food:
        snake.pop()
    if head in snake[1:]:
        print("Game ended by player action")
        sys.exit(0)
    if head == food:
        free_list = [(x, y) for y in range(grid_size[1]) for x in range(grid_size[0]) if (x, y) not in snake]
        food = free_list[random.randrange(len(free_list))]

    # Rendering
    grid = [['.'] * grid_size[0] for _ in range(grid_size[1])]
    grid[food[1]][food[0]] = 'o'
    for i in range(len(snake)):
        grid[snake[i][1]][snake[i][0]] = '#'
    row_strings = [''.join(row) for row in grid]
    print(f"{'\n' * 2}Snake head pos: {head}\nFood pos: {food}\nScore: {len(snake)}\nStep {step + 1} out of {time_limit}:\n{'\n'.join(row_strings)}")

    # Frame Update
    time.sleep(frame_time)