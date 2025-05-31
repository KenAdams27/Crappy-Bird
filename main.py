import pygame
import random
from sys import exit 
import asyncio

def score():
    score=pygame.time.get_ticks()//100
    score_surf=font.render(f'{score}',False,'White')
    score_rect=score_surf.get_rect(center=(50,50))
    screen.blit(score_surf,score_rect)
#initialize lib
pygame.init()
screen=pygame.display.set_mode((1080,700))
pygame.display.set_caption('Crappy Bird')

#background
bg=pygame.image.load('bg.png').convert_alpha()
bg_rect=bg.get_rect(center=(0,0))

#imp variables
obstacle_timer=pygame.USEREVENT+1
pygame.time.set_timer(obstacle_timer,1000)
gravity=0
clock=pygame.time.Clock()
game_active=True
game_over=False
font=pygame.font.Font('Font3.ttf',80)

#birb
bird=pygame.image.load('bird.png').convert_alpha()
bird_rect=bird.get_rect(center=(100,300))

#obstacles
obs_1=pygame.image.load('obs1.upper.png').convert_alpha()
obs_1l=pygame.image.load('obs1.lower.png').convert_alpha()
obstacles_rectu=[]
obstacles_rectl=[]

#gameover
game_over_text=font.render("Game Over",False,'White')
game_over_text_rect=game_over_text.get_rect(center=(525,350))

#main game loop
async def main():
    global clock,bird_rect,gravity,obstacles_rect,game_over,game_active
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
            #restart game mechanic
            if game_over is True:
                if event.type==pygame.MOUSEBUTTONDOWN:game_active=True
            #staying afloat mechanic 
            if event.type==pygame.MOUSEBUTTONDOWN and game_active is True and bird_rect.top>30:gravity-=10
            #randomizing obstacles
            if event.type==obstacle_timer and game_active is True:
                obstacles_rectu.append(obs_1.get_rect(center=(1100,random.randint(-95,90))))
                obstacles_rectl.append(obs_1l.get_rect(center=(1100,random.randint(728,900))))
        if game_active is True: 
            if bird_rect.top<-70:bird_rect.top=-70
            #gravity mechanic
            gravity+=0.4
            bird_rect.y+=gravity

            #obstacle movement
            for obstacle in obstacles_rectu:obstacle.x-=7
            for obstacle in obstacles_rectl:obstacle.x-=7

            #collision detection
            for obstacle in obstacles_rectu:
                if obstacle.collidepoint(bird_rect.centerx,bird_rect.centery):
                    game_active=False
                    game_over=True
            for obstacle in obstacles_rectl:
                if obstacle.collidepoint(bird_rect.centerx,bird_rect.centery):
                    game_active=False
                    game_over=True
            if bird_rect.bottom>=800:game_over=True

            #displaying the surfaces
            screen.blit(bg,bg_rect)
            #displaying obstacles
            for i in obstacles_rectu:
                screen.blit(obs_1,i)
            for j in obstacles_rectl:
                screen.blit(obs_1l,j)
            #displaying birb
            screen.blit(bird,bird_rect)       
            score()
        #game over
        if game_over is True:
            screen.fill('#ADD8E6')
            screen.blit(game_over_text,game_over_text_rect)
        #updating 
        clock.tick(60)
        await asyncio.sleep(0)
        pygame.display.update()

asyncio.run(main())