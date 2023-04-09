import tkinter as tk
import random
import csv

WIDTH = 30
HEIGHT = 20
SEG_SIZE = 20

def rgb(rgb): return "#%02x%02x%02x" % rgb
'''
def save_score(name, score):
    with open('scores.csv', mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([name, score])
'''
# Класс змейки
class Snake(object):
    def __init__(self):
        self.segments = [(7, 1), (6, 1), (5, 1)]
        self.speed = 10
        self.direction = "Right"
        self.next_direction = "Right"

    def move(self):
        for i in range(len(self.segments) - 1, 0, -1):
            self.segments[i] = self.segments[i - 1]

        if self.direction == "Up":
            self.segments[0] = (self.segments[0][0] + 0, self.segments[0][1] - 1)
        if self.direction == "Down":
            self.segments[0] = (self.segments[0][0] + 0, self.segments[0][1] + 1)
        if self.direction == "Left":
            self.segments[0] = (self.segments[0][0] - 1, self.segments[0][1] + 0)
        if self.direction == "Right":
            self.segments[0] = (self.segments[0][0] + 1, self.segments[0][1] + 0)
      
    def change_direction(self, event):
        if event.keysym in ["Up", "Down", "Right", "Left"]:
            opposite_dir = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
            if event.keysym != opposite_dir[self.direction]:
                self.next_direction = event.keysym

    def check_collision(self, blocks):
        if self.segments[0][0] < 0 or self.segments[0][0] >= WIDTH: return True
        if self.segments[0][1] < 0 or self.segments[0][1] >= HEIGHT: return True
        for segment in self.segments[1:]:
            if self.segments[0] == segment:
                return True
        for block in blocks:
          if self.segments[0] == block: return True
        return False

    def eat_food(self, food_position):
        if self.segments[0] == food_position:
            self.segments.append(self.segments[-1])
            return True
        return False

# Класс игры
class Game(tk.Frame):
    def __init__(self, master):
        global IN_GAME
        super().__init__(master)
        self.master = master
        self.master.title("Snake")
        self.snake = Snake()
        self.hardness = 0
        self.begins = False
        self.in_game = True

        # Создание главного меню
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)
    
        # Добавление меню "Настройки"
        settings_menu = tk.Menu(menu_bar, tearoff=False)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)

        # Подменю "Сложность"
        hard_menu = tk.Menu(settings_menu, tearoff=False)
        settings_menu.add_cascade(label="complexity", menu=hard_menu)
        hard_menu.add_command(label="Can I play, Daddy?", command=lambda: self.regenerate_borders(0))
        hard_menu.add_command(label="Don't hurt me.", command=lambda: self.regenerate_borders(1))
        hard_menu.add_command(label="Do or die!", command=lambda: self.regenerate_borders(2))
        hard_menu.add_command(label="I am death incarnate!", command=lambda: self.regenerate_borders(3))
        hard_menu.add_command(label="Mein leben", command=lambda: self.regenerate_borders(4))

        # Подменю "Скорость"
        speed_menu = tk.Menu(settings_menu, tearoff=False)
        settings_menu.add_cascade(label="speed", menu=speed_menu)
        speed_menu.add_command(label="slow", command=lambda: self.change_speed(7))
        speed_menu.add_command(label="normal", command=lambda: self.change_speed(10))
        speed_menu.add_command(label="fast", command=lambda: self.change_speed(13))

        self.canvas = tk.Canvas(self, width=WIDTH * SEG_SIZE, height=HEIGHT * SEG_SIZE, bg=rgb((12, 12, 12)))
        self.canvas.pack()
        self.borders = []
        self.food = self.spawn_food()
        self.score = 3
        self.direction = "Right"
        self.draw_objects()
        self.bind_keys()
        self.name = ""
        self.master.after(100, self.mainloop)

    def change_speed(self, value):
       if self.begins == False: self.snake.speed = value

    def spawn_food(self):
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        while ((x, y) in self.snake.segments or (x,y) in self.borders):
            x = random.randint(0, WIDTH - 1)
            y = random.randint(0, HEIGHT - 1)
        return (x, y)

    def regenerate_borders(self, hardness):
        if self.begins == False:
            result = []
            if hardness >= 1:
                for i in range(3, 12): result.append((i, 7))
                for i in range(13, 18): result.append((10, i))
                for i in range(4, 9): result.append((22, i))
                for i in range(22, 27): result.append((i, 13))
            if hardness >= 2:
                for i in range(3, 7): result.append((8, i))
                for i in range(17, 22): result.append((i, 13))
                for i in range(5, 10): result.append((i, 13))
                for i in range(15, 27): result.append((i, 4))
            if hardness >= 3:
                for i in range(4, 14): result.append((17, i))
                for i in range(4, 17): result.append((i, 10))
                for i in range(10, 19): result.append((14, i))
                for i in range(18, 31): result.append((i, 17))
            if hardness >= 4:
                for i in range(0, 5): result.append((3, i))
                for i in range(0, 10): result.append((i, 17))
                for i in range(3, 5): result.append((i, 13))
                for i in range(12, 27): result.append((i, 1))
            self.borders = result
            while self.food in result: self.food = self.spawn_food()
            self.draw_objects()

    def draw_objects(self):
        self.canvas.delete("all")
        for block in self.borders:
            self.canvas.create_rectangle(block[0] * SEG_SIZE, block[1] * SEG_SIZE,
                                         (block[0] + 1) * SEG_SIZE, (block[1] + 1) * SEG_SIZE, fill=rgb((100, 100, 100)))
        self.canvas.create_rectangle(self.food[0] * SEG_SIZE + 2,
                                     self.food[1] * SEG_SIZE + 2,
                                     (self.food[0] + 1) * SEG_SIZE - 2,
                                     (self.food[1] + 1) * SEG_SIZE - 2,
                                     fill=rgb((222, 0, 16)))
        for i in range(len(self.snake.segments) - 1):
            if self.snake.segments[i][0] < self.snake.segments[i + 1][0] or self.snake.segments[i][1] < self.snake.segments[i + 1][1]:
                self.canvas.create_rectangle(SEG_SIZE * self.snake.segments[i + 0][0] + 1,
                                             SEG_SIZE * self.snake.segments[i + 0][1] + 1,
                                             SEG_SIZE * (self.snake.segments[i + 1][0] + 1) - 1,
                                             SEG_SIZE * (self.snake.segments[i + 1][1] + 1) - 1,
                                             fill=rgb((45, 159, 22)), outline='')
            if self.snake.segments[i][0] > self.snake.segments[i + 1][0] or self.snake.segments[i][1] > self.snake.segments[i + 1][1]:
                self.canvas.create_rectangle(SEG_SIZE * self.snake.segments[i + 1][0] + 1,
                                             SEG_SIZE * self.snake.segments[i + 1][1] + 1,
                                             SEG_SIZE * (self.snake.segments[i + 0][0] + 1) - 1,
                                             SEG_SIZE * (self.snake.segments[i + 0][1] + 1) - 1,
                                             fill=rgb((45, 159, 22)), outline='')

    def game_start(self, event):
        if event.keysym == "space": self.begins = True

    def bind_keys(self):
        self.master.bind("<KeyPress-Up>", self.snake.change_direction)
        self.master.bind("<KeyPress-Down>", self.snake.change_direction)
        self.master.bind("<KeyPress-Left>", self.snake.change_direction)
        self.master.bind("<KeyPress-Right>", self.snake.change_direction)
        self.master.bind("<KeyPress-space>", self.game_start)

    def print_records(self):
        with open('leaderboard.csv', 'a', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)

    def save_record(self):
      record = [str(input()), self.score]
      with open('leaderboard.csv', 'a', newline='') as file:
          writer = csv.writer(file)
          writer.writerow(record)

    def win(self): self.canvas.create_text((WIDTH * SEG_SIZE / 2, HEIGHT * SEG_SIZE / 2), text="You Win!", font=("Arial", 30), fill=rgb((255, 255, 255)))
    def lose(self):
        self.canvas.create_text((WIDTH * SEG_SIZE / 2, HEIGHT * SEG_SIZE / 2), text="Game Over!", font=("Arial", 20), fill=rgb((222, 0, 16)))
        self.save_record()

    def main_loop(self):
        if self.in_game:
            if self.begins:
                self.snake.direction = self.snake.next_direction
                self.snake.move()
                self.draw_objects()
                if self.snake.check_collision(self.borders):
                    self.in_game = False
                elif self.snake.eat_food(self.food):
                    self.food = self.spawn_food()
                    self.score += 1
                    self.master.title("Snake | Score: {}".format(self.score))
            else:
                self.canvas.create_text((WIDTH * SEG_SIZE / 2, HEIGHT * SEG_SIZE / 2), text="press space to start", font=("Arial", 20), fill=rgb((255, 255, 255)))
                self.canvas.create_text((WIDTH * SEG_SIZE / 2, HEIGHT * SEG_SIZE / 2 + 35), text="enter your name in console", font=("Arial", 20), fill=rgb((255, 255, 255)))
                self.canvas.create_text((WIDTH * SEG_SIZE / 2, HEIGHT * SEG_SIZE / 2 + 60), text="after end of the game", font=("Arial", 20), fill=rgb((255, 255, 255)))
            self.master.after(1000 // self.snake.speed, self.main_loop)
        elif not self.in_game:
            self.lose()
            self.print_records()

# Запуск игры
if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    game.pack()
    game.main_loop()
    root.mainloop()