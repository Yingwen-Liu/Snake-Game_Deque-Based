import pygame
import random


WIDTH, HEIGHT = 800, 600
GRID_SIZE = 40
COLS = HEIGHT // GRID_SIZE
ROWS = WIDTH // GRID_SIZE
FPS = 8

BG = (255, 255, 255)
GRID = (0, 0, 0)
APPLE = (255, 0, 0)
SNAKE = (0, 255, 0)


class Apple:
    def __init__(self):
        self.position = [random.randint(0, ROWS-1), random.randint(0, COLS-1)]
        
    def update(self):
        self.position = [random.randint(0, ROWS-1), random.randint(0, COLS-1)]
    
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
        self.front = self.front.next
    
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
        
        self.length = 1
        self.positions = Queue([ROWS // 2 - 1, COLS // 2 - 1])
        self.direction = random.choice([[0, -1], [0, 1], [-1, 0], [1, 0]])
    
    def reset(self):
        self.length = 1
        self.positions = Queue([ROWS // 2 - 1, COLS // 2 - 1])
        self.direction = random.choice([[0, -1], [0, 1], [-1, 0], [1, 0]])
    
    def turn(self, point):
        if [point[0] * -1, point[1] * -1] != self.direction:
            self.direction = point
    
    def move(self):
        current = self.positions.rear
        new = [
            (current.data[0] + self.direction[0]) % ROWS,
            (current.data[1] + self.direction[1]) % COLS
        ]
        
        if self.positions.search(new):
            self.gameover()
        else:
            self.positions.enqueue(new)
            if new == self.apple.position:
                self.length += 1
                self.apple.update()
            else:
                self.positions.dequeue()
    
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
