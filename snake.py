import pygame
import random


WIDTH, HEIGHT = 600, 400
GRID_SIZE = 50
COLS = HEIGHT // GRID_SIZE
ROWS = WIDTH // GRID_SIZE
FPS = 8
BOARDER = True

BG = (255, 255, 255)
GRID = (0, 0, 0)
APPLE = (255, 0, 0)
SNAKE = (0, 255, 0)


class Apple:
    def __init__(self):
        self.position = [random.randint(0, ROWS), random.randint(0, COLS)]
        print(self.position)
        
    def update(self, empty):
        if empty != []:
            self.position = random.choice(empty)
    
    def draw(self, surface):
        r = pygame.Rect(
            (self.position[0]*GRID_SIZE, self.position[1]*GRID_SIZE),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, APPLE, r)
        pygame.draw.rect(surface, GRID, r, 1)


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self, data):
        init_node = Node(data)
        self.front = init_node
        self.rear = init_node
        
    def enqueue(self, data):
        new_node = Node(data)
        self.rear.next = new_node
        self.rear = new_node
    
    def dequeue(self):
        front_data = self.front.data
        self.front = self.front.next
        return front_data
    
    def search(self, data):
        current = self.front
        while current:
            if current.data == data:
                return True
            current = current.next
        return False


class Snake:
    def __init__(self, apple):
        self.apple = apple
        
        self.length = None
        self.positions = None
        self.direction = []
        self.empty = []
        
        self.reset()
    
    def reset(self):
        self.length = 1
        self.positions = Queue([ROWS // 2, COLS // 2])
        self.direction = random.choice([[0, -1], [0, 1], [-1, 0], [1, 0]])
        
        self.empty = []
        for i in range(ROWS):
            for j in range(COLS):
                self.empty.append([i, j])
        self.empty.remove([ROWS // 2, COLS // 2])
    
    def turn(self, point):
        if [point[0] * -1, point[1] * -1] != self.direction:
            self.direction = point
    
    def move(self):
        current = self.positions.rear
        new = [current.data[0] + self.direction[0],
               current.data[1] + self.direction[1]]

        if BOARDER:
            if new[0] < 0 or new[0] >= ROWS or new[1] < 0 or new[1] >= COLS:
                self.gameover()
                return
        else:
            new[0] %= ROWS
            new[1] %= COLS

        if self.positions.search(new):
            self.gameover()
        else:
            self.positions.enqueue(new)
            self.empty.remove(new)
            
            if new == self.apple.position:
                self.length += 1
                self.apple.update(self.empty)
            else:
                tail = self.positions.dequeue()
                self.empty.append(tail)
    
    def gameover(self):
        self.reset()
    
    def draw(self, surface):
        current = self.positions.front
        
        colour = list(SNAKE)
        while current:
            r = pygame.Rect(
                (current.data[0] * GRID_SIZE, current.data[1] * GRID_SIZE),
                (GRID_SIZE, GRID_SIZE)
            )
            colour[1] -= 255 // self.length
            
            pygame.draw.rect(surface, tuple(colour), r)
            pygame.draw.rect(surface, GRID, r, 1)
            current = current.next


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption('Snake')
    
    apple = Apple()
    snake = Snake(apple)

    while True:
        screen.fill(BG)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.turn([0, -1])
                elif event.key == pygame.K_DOWN:
                    snake.turn([0, 1])
                elif event.key == pygame.K_LEFT:
                    snake.turn([-1, 0])
                elif event.key == pygame.K_RIGHT:
                    snake.turn([1, 0])
        
        snake.move()

        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
