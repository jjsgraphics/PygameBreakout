import pygame
import time
import random
import math
import asyncio
pygame.font.init()

#  We need to create a window (TOP LEFT IS 0,0. DOWN IS +Y, RIGHT IS +X)

FPS = 300
WIDTH = 1000
HEIGHT = 1200
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gaming time mfers")

class Object():
  def __init__(self, w, h, x, y, v, c):
    self.w = w
    self.h = h
    self.x = x
    self.y = y
    self.v = v
    self.colour = c
    self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

  def drawObject(self):
    self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
    pygame.draw.rect(WIN, self.colour, self.rect)

class Bricks(Object):
  def __init__(self, h, col, row, s, c):
    self.spacing = s
    self.columns = col
    self.totalSpace = s * (col + 1)
    self.w = (WIDTH - self.totalSpace) / col
    self.h = h
    self.colour = c
    self.exist = True
    
    self.x0 = s
    self.y0 = s
    
    self.bricks = []

    for i in range(col):
      for j in range(row):
        x = self.x0 + (i * (s + self.w))
        y = self.y0 + (j * (s + self.h))
        rect = pygame.Rect(x, y, self.w, self.h)
        self.bricks.append(rect)
        print(f"Brick i = {i}, j = {j}, x = {x}, y = {y}")
    
  def drawBricks(self):
    for rect in self.bricks:
      pygame.draw.rect(WIN, self.colour, rect)
      
  def checkBrickCollision(self,ball):
    # maybe make a getRect function which uses a hashmap to find a specific brick
    for rect in self.bricks:
      if rect.colliderect(ball.rect):
        print(f"collision with brick x: {rect.x}")
        self.bricks.remove(rect)
        ball.vy *= -1


class Ball(Object):
  def __init__(self, w, h, x, y, v, c):
    self.w = w
    self.h = h
    self.x = x
    self.y = y
    self.v = v
    self.vx = 0
    self.vy = 0
    self.colour = c
    self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

  def checkCollisions(self, p):
    if self.rect.colliderect(p.rect):
      print("collision")
       # Calculate relative X position of the ball to the center of the paddle
      relativeX = (self.x + self.w/2) - (p.x + p.w/2)
      normX = relativeX / (p.w/0.5)
      maxAngle = 4
      bounceAngle = normX * maxAngle

      self.v = 2
      self.vx = self.v * math.sin(bounceAngle)
      self.vy = -self.v * math.cos(bounceAngle)
      
      #print(f"maxAngle = {maxAngle}")
      #print(f"relativeX = {relativeX}")
      print(f"normX = {normX}")
      print(f"bounceAngle = {bounceAngle}")
      #print(f"vx = {self.vx}")
      #print(f"vy = {self.vy}")
      #print(f"x = {self.x}")
      #print(f"y = {self.y}")

    if self.y > HEIGHT - self.h/2 or self.y + self.h/2 < 0:
      self.vy *= -1

    if self.x > WIDTH - self.w/2 or self.x + self.w/2 < 0:
      self.vx *= -1

  def updateBall(self, p):
    self.checkCollisions(p)
    self.x = self.x + self.vx
    self.y = self.y + self.vy


class Player(Object):
  def __init__(self, w, h, x, y, lives, v, c):
    self.w = w
    self.h = h
    self.x = x
    self.y = y
    self.v = v
    self.lives = lives
    self.colour = c
    self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

  @staticmethod
  def keyPressed(self, keys):
    #if keys[pygame.K_w] and self.y - self.v >= 0:
    #  self.y -= self.v
    if keys[pygame.K_a] and self.x - self.v + self.w*0.75 >= 0:
      self.x -= self.v
    #if keys[pygame.K_s] and self.y + self.v + self.h <= HEIGHT:
    #  self.y += self.v
    if keys[pygame.K_d] and self.x + self.v + 0.25*self.w <= WIDTH:
      self.x += self.v

def draw(objs, bricks):
  WIN.fill((0,0,0))
  for object in objs:  
    object.drawObject()
  bricks.drawBricks()
  pygame.display.update()
  
def resetBall(p, b):
  p.lives -= 1
  b.x = WIDTH/2 - b.w/2
  b.y = HEIGHT/2 - b.h/2

async def main():
  run = True
  p1w, p1h = 100, 10
  p1 = Player(p1w, p1h, WIDTH/2 - p1w/2, HEIGHT - HEIGHT/10, 3, 5, (0,0,255))
  bricks = Bricks(30, 5, 5, 10, (255, 0, 255))
  ball = Ball(15, 15, WIDTH/2, HEIGHT/2, 1.5, (255,255,255))
  ball.vy = 1
  clock = pygame.time.Clock()
  start_time = time.time()
  
  #initialiseBricks()

  while run:

    clock.tick(FPS)
    elapsed_time = time.time() - start_time

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        break

    objs = [p1, ball] # objects to draw
    keys = pygame.key.get_pressed()
    p1.keyPressed(p1, keys)
    ball.updateBall(p1)
    bricks.checkBrickCollision(ball)
     
    if ball.y > p1.y + (p1.h/2):
      print("restart")
      resetBall(p1,ball)
      if p1.lives <= 0:
        run = False

    #print(f"x = {ball.x}")
    #print(f"y = {ball.y}")

    draw(objs, bricks)

    await asyncio.sleep(0)

  pygame.quit()

asyncio.run(main())

if __name__ == "__main__":
  main()