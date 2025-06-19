import sys
import gamemanager
import pygame

from gamemanager import GameManager
from gameui import GameUi

from screen.gameoverscreen import GameOverScreen
from screen.titlescreen import TitleScreen
from screen.introscreen import IntroScreen
from screen.gamescreen import GameScreen
from screen.camerascreen import CameraScreen
from const import *

class ScreenManager:
    def __init__(self):
        self.running = True
        self.screen = 0
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((baseWidth, baseHeight), pygame.SRCALPHA | pygame.FULLSCREEN | pygame.SCALED)

        self.gameManager = GameManager()
        self.gameUi = GameUi()

        self.gameOverScreen = GameOverScreen(self.gameManager)
        self.introScreen = IntroScreen(self.gameManager)
        self.gameScreen = GameScreen(self.gameManager, self.gameUi, self.gameOverScreen)
        self.cameraScreen = CameraScreen(self.gameManager, self.gameUi)
        self.titleScreen = TitleScreen(self.introScreen, self.gameScreen, self.cameraScreen)
        
        self.titleScreen.nextScreen = self.introScreen
        self.introScreen.nextScreen = self.gameScreen
        self.gameScreen.nextScreen = self.cameraScreen
        self.cameraScreen.nextScreen = self.gameScreen
        self.gameOverScreen.nextScreen = self.titleScreen

        pygame.display.set_caption("Five Nights at Zzaihong's (ver0.1_alpha)")
    
    def start(self):
        self.currentScreen = self.titleScreen
        while self.currentScreen != None:
            self.running = True
            self.currentScreen.running = True
            self.currentScreen.initial()
            while self.running:
                self.currentScreen.draw(self.screen, pygame.event.get())
                self.running = self.currentScreen.running

                self.clock.tick(30)
            self.currentScreen = self.currentScreen.nextScreen

if __name__ == "__main__":
    pygame.init()
    screenManager = ScreenManager()
    screenManager.start()
    pygame.quit()
    sys.exit()
