import pygame
from pygame.locals import *
import random

pygame.init()
font = pygame.font.SysFont('arial', 25)

SPEED = 100

class Game:
    
    def __init__(self, w=640, h=600):
        self.w = w
        self.h = h
        # init display
        self.clock = pygame.time.Clock()
        self.road_w = int(self.w / 1.6)
        self.roadmark_w = int(self.w / 80)
        self.right_lane = self.w / 2 + self.road_w / 4
        self.left_lane = self.w / 2 - self.road_w / 4

        self.car = pygame.image.load("car.png")
        #resize image
        self.car = pygame.transform.scale(self.car, (150, 250))
        self.car_loc = self.car.get_rect()
        self.car_loc.center = self.right_lane, self.h * 0.8

        # load enemy vehicle
        self.car2 = pygame.image.load("otherCar.png")
        #resize image
        self.car2 = pygame.transform.scale(self.car2, (150, 250))
        self.car2_loc = self.car2.get_rect()
        self.car2_loc.center = self.left_lane, self.h * 0.2
        self.score = 0

    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Final Score', self.score)
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.car_loc.x - int(self.road_w / 2) == 145:
                    self.car_loc = self.car_loc.move([-int(self.road_w / 2), 0])
                elif event.key == pygame.K_RIGHT and self.car_loc.x + int(self.road_w / 2) == 345:
                    self.car_loc = self.car_loc.move([int(self.road_w / 2), 0])
        
        # 3. check if game over
        game_over = False
        if self.is_colission():
            game_over = True
            return game_over, self.score
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    def is_colission(self):
        if self.car_loc[0] == self.car2_loc[0] and self.car2_loc[1] > self.car_loc[1] - 250:
            return True
        else:
            return False

    def _update_ui(self):
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Car Dodge')
        pygame.draw.rect(
        self.display,
        (50, 50, 50),
        (self.w / 2- self.road_w/2, 0,  self.road_w, self.h))
        # draw centre line
        pygame.draw.rect(
        self.display,
        (255, 240, 60),
        (self.w / 2 - self.roadmark_w/2, 0, self.roadmark_w, self.h))
        # draw left road marking
        pygame.draw.rect(
        self.display,
        (255, 255, 255),
        (self.w / 2 -  self.road_w/2 + self.roadmark_w*2, 0, self.roadmark_w, self.h))
        # draw right road marking
        pygame.draw.rect(
        self.display,
        (255, 255, 255),
        (self.w / 2 +  self.road_w/2 - self.roadmark_w*3, 0, self.roadmark_w, self.h))
        self.display.blit(self.car, self.car_loc)
        self.display.blit(self.car2, self.car2_loc)
        self.car2_loc[1] += 5 #CAR SPEED
        if self.car2_loc[1] > self.h:
            self.score += 1
            # randomly select lane
            if random.randint(0,1) == 0:
                self.car2_loc.center = self.right_lane, - 150
            else:
                self.car2_loc.center = self.left_lane, - 150
        
        
        text = font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.display.blit(text, [0, 0])
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    
    # game loop
    while True:
        game_over, score = game.play_step()
        
        if game_over == True:
            break

    print('Final Score', score)
    pygame.quit()