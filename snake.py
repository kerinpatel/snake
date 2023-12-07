import turtle
import random
import time

WIDTH = 500
HEIGHT = 500
FOOD_SIZE = 10
DELAY = 100
GAME_DURATION = 60

offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}

score = 0
start_time = time.time()
food_pos = (0, 0)
snake_direction = "up"
snake_speed = 20  # Initial snake speed

# Snake initialization
snake = [[0, 0], [0, 20], [0, 40], [0, 50], [0, 60]]

def get_random_food_pos():
    x = random.randint(-WIDTH / 2 + FOOD_SIZE, WIDTH / 2 - FOOD_SIZE)
    y = random.randint(-HEIGHT / 2 + FOOD_SIZE, HEIGHT / 2 - FOOD_SIZE)
    return (x, y)

def update_score():
    pen_score.clear()
    pen_score.penup()
    pen_score.goto(WIDTH // 2 - 100, HEIGHT // 2 - 40)
    pen_score.color("lightblue")
    pen_score.write(f"Score: {score}", align="center", font=("Courier", 14, "normal"))

def update_timer():
    elapsed_time = max(0, GAME_DURATION - (time.time() - start_time))
    pen_timer.clear()
    pen_timer.penup()
    pen_timer.goto(0, HEIGHT // 2 - 40)  # Centered Y position
    pen_timer.color("lightblue")
    pen_timer.write(f"Time: {int(elapsed_time)}s", align="center", font=("Courier", 14, "normal"))

def update_game_over():
    pen_game_over.clear()
    pen_game_over.penup()
    pen_game_over.goto(0, 0)
    pen_game_over.color("red")
    pen_game_over.write(f"Game Over\nFinal Score: {score}", align="center", font=("Courier", 24, "normal"))

    # Add a reset button
    pen_reset = turtle.Turtle()
    pen_reset.penup()
    pen_reset.goto(0, -50)
    pen_reset.color("lightblue")
    pen_reset.write("Press 'R' to Restart", align="center", font=("Courier", 14, "normal"))

    screen.onkey(reset, "r")  # Bind the reset function to the 'R' key

def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
    return distance

def food_collision():
    global food_pos, snake
    return get_distance(snake[-1], food_pos) < 20

def go_up():
    global snake_direction
    if snake_direction != "down":
        snake_direction = "up"

def go_right():
    global snake_direction
    if snake_direction != "left":
        snake_direction = "right"

def go_down():
    global snake_direction
    if snake_direction != "up":
        snake_direction = "down"

def go_left():
    global snake_direction
    if snake_direction != "right":
        snake_direction = "left"


pen_reset = None  # Declare pen_reset as a global variable

def reset():
    global snake, snake_direction, food_pos, pen_score, pen_timer, pen_game_over, pen_reset, pen_made_by, score, food, start_time, snake_speed
    snake = [[0, 0], [0, 20], [0, 40], [0, 50], [0, 60]]
    snake_direction = "up"
    food_pos = get_random_food_pos()
    food.goto(food_pos)
    score = 0
    start_time = time.time()
    snake_speed = 1  # Increase snake speed after restart
    update_score()
    update_timer()
    pen_game_over.clear()
    
    # Check if pen_reset is not None before clearing
    if pen_reset is not None:
        pen_reset.clear()
    
    move_snake()

def move_snake():
    global snake, snake_direction, score, start_time, food, food_pos, snake_speed
    elapsed_time = time.time() - start_time

    if elapsed_time >= GAME_DURATION:
        update_game_over()
        print("Game over! Time limit reached.")
        return

    new_head = snake[-1].copy()
    new_head[0] = snake[-1][0] + offsets[snake_direction][0]
    new_head[1] = snake[-1][1] + offsets[snake_direction][1]

    if new_head in snake[:-1]:
        update_game_over()
        return
    else:
        snake.append(new_head)

        if not food_collision():
            snake.pop(0)
        else:
            score += 10
            update_score()

            food_pos = get_random_food_pos()
            food.goto(food_pos)

        if snake[-1][0] > WIDTH / 2:
            snake[-1][0] -= WIDTH
        elif snake[-1][0] < -WIDTH / 2:
            snake[-1][0] += WIDTH
        elif snake[-1][1] > HEIGHT / 2:
            snake[-1][1] -= HEIGHT
        elif snake[-1][1] < -HEIGHT / 2:
            snake[-1][1] += HEIGHT

        pen.clearstamps()

        for segment in snake:
            pen.goto(segment[0], segment[1])
            pen.stamp()

        screen.update()
        update_timer()

        turtle.ontimer(move_snake, DELAY // snake_speed)  # Adjust speed

screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("Snake Game")
screen.bgcolor("black")
screen.tracer(0)

border = turtle.Turtle()
border.speed(0)
border.color("pink")
border.penup()
border.goto(-WIDTH / 2, -HEIGHT / 2)
border.pendown()
for _ in range(4):
    border.forward(WIDTH)
    border.left(90)
border.hideturtle()

pen = turtle.Turtle("square")
pen.penup()
pen.pencolor("yellow")
pen.goto(0, HEIGHT // 2 - 20)

food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.shapesize(FOOD_SIZE / 20)
food.penup()

pen_score = turtle.Turtle()
pen_score.hideturtle()

pen_timer = turtle.Turtle()
pen_timer.hideturtle()

pen_game_over = turtle.Turtle()
pen_game_over.hideturtle()

pen_made_by = turtle.Turtle()
pen_made_by.penup()
pen_made_by.goto(WIDTH // 2 - 130, -HEIGHT // 2 + 10)
pen_made_by.color("white")
pen_made_by.write("Made by IT Club Students", align="right", font=("Courier", 10, "normal"))

# Now, initialize pen_reset
pen_reset = turtle.Turtle()
pen_reset.penup()
pen_reset.hideturtle()

screen.listen()
screen.onkey(lambda: snake_direction != "down" and go_up(), "Up")
screen.onkey(lambda: snake_direction != "left" and go_right(), "Right")
screen.onkey(lambda: snake_direction != "up" and go_down(), "Down")
screen.onkey(lambda: snake_direction != "right" and go_left(), "Left")

def update_game_over():
    global pen_game_over, pen_reset
    pen_game_over.clear()
    pen_game_over.penup()
    pen_game_over.goto(0, 0)
    pen_game_over.color("red")
    pen_game_over.write(f"Game Over\nFinal Score: {score}\nPress 'R' to Restart", align="center", font=("Courier", 24, "normal"))

    # Add a reset button
    pen_reset = turtle.Turtle()
    pen_reset.penup()
    pen_reset.goto(0, -50)
    pen_reset.color("lightblue")
    pen_reset.write("Press 'R' to Restart", align="center", font=("Courier", 14, "normal"))

    screen.onkey(reset, "r")  # Bind the reset function to the 'R' key


reset()
turtle.done()
