import random

import pygame

from screen.screenbase import Screen
from widget import *

class TitleScreen(Screen):
    def __init__(self, introScreen, gameScreen, cameraScreen):
        super().__init__()
        self.font = pygame.font.Font("./resources/font/consolas.ttf", 50)
        self.newGameBtn = Button((150, 400, 250, 50), "New Game", self.font, (255, 255, 255))
        self.exitBtn = Button((150, 470, 150, 50), "Quit", self.font, (255, 255, 255))
        self.pointTextSurface = self.font.render(">>", True, (255, 255, 255))
        self.pointTextLoc = 400

        self.introScreen = introScreen
        self.gameScreen = gameScreen
        self.cameraScreen = cameraScreen
        
        self.titleBackgroundImg = getImgList("resources/img/screen/title.png", 2, 1)
        self.titleBackgroundImgNextFlipRemain = 0
        self.titleBlipImg = AnimatedImage("resources/img/effect/blip.png", 17, 1, 0.2)
        self.titleStaticImg = AnimatedImage("resources/img/effect/static.png", 8, 1, 0.05)
        self.titleLines = ["Five", "Nights", "at", "Zzaihong's"]
    
    def initial(self):
        titleMainAudio.play()
        titleStaticAudio.play()

    def draw(self, screen, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                self.nextScreen = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.newGameBtn.isHovered(event.pos):
                    print("게임 시작!")
                    if self.introScreen.screenStep >= 10:
                        self.introScreen.screenStep = 7
                    self.gameScreen.nextScreen = self.cameraScreen
                    self.cameraScreen.nextScreen = self.gameScreen
                    self.running = False
                elif self.exitBtn.isHovered(event.pos):
                    self.nextScreen = None
                    self.running = False

        mousePos = pygame.mouse.get_pos()

        screen.fill((0,0,0,0))
        if self.titleBackgroundImgNextFlipRemain == 0:
            self.titleBackgroundImgNextFlipRemain = random.randint(100, 150)
        elif self.titleBackgroundImgNextFlipRemain == 1:
            self.titleBackgroundImgNextFlipRemain = -5
        elif self.titleBackgroundImgNextFlipRemain > 0:
            self.titleBackgroundImgNextFlipRemain -= 1
        
        if self.titleBackgroundImgNextFlipRemain < 0:
            screen.blit(self.titleBackgroundImg[1], (0, 0))
            self.titleBackgroundImgNextFlipRemain += 1
        else:
            screen.blit(self.titleBackgroundImg[0], (0, 0))

        titleBlipCurrentImg = self.titleBlipImg.getCurrentImg()
        staticCurrentImg = self.titleStaticImg.getCurrentImg()
        titleBlipCurrentImg.set_alpha(80)
        staticCurrentImg.set_alpha(40)

        screen.blit(titleBlipCurrentImg, (0, 0))
        screen.blit(staticCurrentImg, (0, 0))

        if self.newGameBtn.isHovered(mousePos):
            self.pointTextLoc = 400
        elif self.exitBtn.isHovered(mousePos):
            self.pointTextLoc = 470
        
        titleLinePrintY = 70
        for titleLine in self.titleLines:
            textSurface = self.font.render(titleLine, False, (255, 255, 255))
            screen.blit(textSurface, (150, titleLinePrintY))
            titleLinePrintY += textSurface.get_height() + 10
        
        self.newGameBtn.draw(screen)
        self.exitBtn.draw(screen)
        screen.blit(self.pointTextSurface, (80, self.pointTextLoc))

        pygame.display.update()
