# Imports
import random
import sys
import time

# Configuration Variables
grid_size = (60, 15)
snake = [(58,10), (57, 10), (56, 10)]
food = random
time_limit = 15
frame_time = 0.3

# Logic Variables
direction = (1, 0)
head = snake[0]

# Main Logic Updating Loop
for step in range(time_limit):
    # Dynamic Positioning Logic
    new_head = (head[0] + direction[0], head[1] + direction[1])
    if new_head != food:
        snake.pop()
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
    if new_head in snake:
        print("Game Over")
        sys.exit(0)
    head = new_head
    snake.insert(0, new_head)

    # Rendering
    grid = [['.'] * grid_size[0] for _ in range(grid_size[1])]
    grid[food[1]][food[0]] = 'o'
    for i in range(len(snake)):
        grid[snake[i][1]][snake[i][0]] = '#'
    row_strings = [''.join(row) for row in grid]
    print(f"{'\n' * 2}Step {step + 1} out of {time_limit}:\n{'\n'.join(row_strings)}")

    # Frame Update
    time.sleep(frame_time)