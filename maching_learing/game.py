import pygame
import global_val as Gvar
from player import Player
from enemy import Enemy
from enemy import enemy_creator
import numpy as np
from GUI_base.text_box_base import TextBoxBase


class Game:

    def init(self):
        pygame.init()
        surface = pygame.display.set_mode((1200, 700))
        Gvar.surface = surface
        self.surfRect = surface.get_rect()
        self.player1 = Player()
        self.player1.set(50, 5, 600, 350)
        self.enemylist = enemy_creator(2)
        self.command=''
        self.text_box=TextBoxBase(Gvar.surface)

    def render(self):
        Gvar.event_list=pygame.event.get()

        for EV in Gvar.event_list:
            if EV.type == pygame.KEYDOWN:
                if EV.key == pygame.K_ESCAPE:
                    # quit()
                    self.command='exit'
        Gvar.surface.fill([255, 255, 255])
        self.text_box.use()
        self.player1.control()
        xn,yn=self.boundary_limit(self.player1.x,self.player1.y,self.player1.speed)
        self.player1.set_xy(xn,yn)

        self.player1.show()

        for enemyI in self.enemylist:
            enemyI.track(self.player1.x, self.player1.y)
            enemyI.show()

        # if pygame.time.get_ticks()//1%100==0:
        #     enemyI=enemy_creator(1)[0]
        #     enemylist.append(enemyI)


        pygame.display.flip()

    def get_infomation(self):
        player = [self.player1.x, self.player1.y]
        enemy = []
        for enemyI in self.enemylist:
            enemy.append([enemyI.x, enemyI.y])
        return np.append(player,enemy)

    def reward_judgment(self):
        enemy_rect_list = []
        for enemyI in self.enemylist:
            enemy_rect_list.append(enemyI.rect)
        reward = len(self.player1.rect.collidelistall(enemy_rect_list))
        done = False
        if reward >= 2:
            done = True
        return -reward*1000, done

    def boundary_limit(self,x,y,s):
        xn=x
        yn=y
        if x < 0:
            xn=x+2*s
        if x > self.surfRect.w:
            xn=x-2*s
        if y < 0:
            yn = y + 2*s
        if y > self.surfRect.h:
            yn = y - 2*s
        return xn,yn

if __name__ == '__main__':

    game1 = Game()
    game1.init()
    i = 1
    while 1:
        i = i + 1
        # command=int(input())
        import math

        game1.player1.set_xy(500 + math.sin(i) * 200, 500 + math.cos(i) * 200)
        game1.render()
        print(game1.player1.x)
