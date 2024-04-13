import tkinter
import random
import pprint

class Game:
    
    def __init__(self, fullscreen = True):
        self.window = tkinter.Tk()
        self.window.attributes("-fullscreen", fullscreen)
        self.canvas = tkinter.Canvas(self.window)
        self.width = self.window.winfo_width()
        self.height = self.window.winfo_height()
        self.color = "white"
        self.left_x_speed = random.randint(3,5)
        self.left_y_speed = random.choice(list(range(-5, -3)) + list(range(3, 5)))
        self.right_x_speed = random.randint(-5,-3)
        self.right_y_speed = random.choice(list(range(-5, -3)) + list(range(3, 5)))
        self.left_ball = None
        self.right_ball = None
        self.blue_edge = {}
        self.red_edge = {}

    def start(self):
        self.createSides()
        self.createBouncingBall("LEFT")
        self.moveBall("LEFT")
        self.createBouncingBall("RIGHT")
        self.moveBall("RIGHT")
        self.canvas.pack(fill=tkinter.BOTH, expand=True)
        self.window.mainloop()
        
    def createBouncingBall(self, side):
        x, y = self.__getWindowCenter()
        r = self.__ballSize()
        if side == "LEFT":
            x = 2 * r
        else:
            x = self.width - (2 * r)
        x0 = x - r
        x1 = x + r
        y0 = y - r 
        y1 = y + r
        if side == "LEFT":
            self.left_ball = self.canvas.create_oval(x0, y0, x1, y1, fill=self.color)
        else:
            self.right_ball = self.canvas.create_oval(x0, y0, x1, y1, fill=self.color)

    def createSides(self):
        divisble_by = 10
        box_width = self.width // divisble_by
        box_height = self.height // divisble_by
        threshold = box_width // 2
        for i in range(0, self.width, box_width):
            for j in range(0, self.height, box_height):
                x0 = i
                x1 = i + box_width
                y0 = j
                y1 = j + box_height
                if x1 >= self.width/2:
                    rectangle = self.canvas.create_rectangle(x0, y0, x1, y1, fill="blue")
                    if not self.blue_edge.get(j):
                        self.blue_edge[j] = [rectangle]
                    else:
                        self.blue_edge[j].append(rectangle)
                else:
                    rectangle = self.canvas.create_rectangle(x0, y0, x1, y1, fill="red")
                    if self.red_edge.get(j) is None:
                        self.red_edge[j] = [rectangle]
                    else:
                        self.red_edge[j].append(rectangle)
        self.red_edge[self.height] = []
        self.blue_edge[self.height] = []

    def moveBall(self, side):
        if side == "LEFT":
            ball = self.left_ball
            ball_center = self.__ballSize()/2 + self.canvas.coords(ball)[1]
            x_speed = self.left_x_speed
            y_speed = self.left_y_speed
            max_left = 0
            max_right = self.__max_x("LEFT", ball_center)
        else:
            ball = self.right_ball
            ball_center = self.__ballSize()/2 + self.canvas.coords(ball)[1]
            x_speed = self.right_x_speed
            y_speed = self.right_y_speed
            max_left = self.__max_x("RIGHT", ball_center)
            max_right = self.width

        # Remain ball in each side
        if self.canvas.coords(ball)[0] <= max_left and side == "LEFT":
            x_speed *= -1
        elif self.canvas.coords(ball)[0] <= max_left and side == "RIGHT":
            self.___hit(side, ball)
            x_speed *= -1
        elif self.canvas.coords(ball)[2] >= max_right and side == "RIGHT":
            x_speed *= -1
        elif self.canvas.coords(ball)[2] >= max_right and side == "LEFT":
            self.___hit(side, ball)
            x_speed *= -1

        if self.canvas.coords(ball)[1] <= 0 or self.canvas.coords(ball)[3] >= self.window.winfo_height():
            y_speed *= -1

        if side == "LEFT":
            self.left_x_speed = x_speed
            self.left_y_speed = y_speed
        else:
            self.right_x_speed = x_speed
            self.right_y_speed = y_speed

        self.canvas.move(ball, x_speed, y_speed)
        self.window.after(10, self.moveBall, side)
    
    # Check what the max x left/right is for that coordinate
    def __max_x(self, side, center):
        if side == "LEFT":
            hit_edge = self.blue_edge
        else:
            hit_edge = self.red_edge

        keys = list(hit_edge.keys())
        for i in range(len(keys)):
            if i < len(keys) - 1:  # Check if it's not the last key
                box_top = keys[i + 1]
                box_bottom = keys[i]
                if box_top >= center and box_bottom <= center:
                    if len(hit_edge[keys[i]]) != 0:
                        if side == "LEFT":
                            box = hit_edge[keys[i]][0]
                            return self.canvas.coords(box)[0]
                        else:
                            box = hit_edge[keys[i]][-1]
                            return self.canvas.coords(box)[2]
    
    # Switch color on box when hit
    def ___hit(self, side, ball):
        ball_center = int((self.canvas.coords(ball)[1] + self.canvas.coords(ball)[3]) // 2)
        if side == "LEFT":
            hit_edge = self.blue_edge
            new_edge = self.red_edge
            color = "red"
        else:
            hit_edge = self.red_edge
            new_edge = self.blue_edge
            color = "blue"

        keys = list(hit_edge.keys())
        for i in range(len(keys)):
            if i < len(keys) - 1:  # Check if it's not the last key
                box_top = keys[i + 1]
                box_bottom = keys[i]
                if box_top >= ball_center and box_bottom <= ball_center:
                    if len(hit_edge[keys[i]]) != 0:
                        if side == "LEFT":
                            box = hit_edge[keys[i]].pop(0)
                            new_edge[keys[i]].append(box)
                            self.canvas.itemconfigure(new_edge[keys[i]][-1], fill=color)
                            break
                        else:
                            box = hit_edge[keys[i]].pop()
                            new_edge[keys[i]].insert(0, box)
                            self.canvas.itemconfigure(new_edge[keys[i]][0], fill=color)
                            break

    # Get window center
    def __getWindowCenter(self):
        self.window.update_idletasks()
        x = self.width // 2
        y = self.height // 2
        return x, y
    
    # Make the ball size
    def __ballSize(self):
        return self.height // 30
    
                


