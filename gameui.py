import pygame
from widget import *
from const import *

class GameUi:
    def __init__(self):
        self.midFont = pygame.font.Font("./resources/font/lcdsolid.ttf", 30)
        self.smallFont = pygame.font.Font("./resources/font/lcdsolid.ttf", 20)

        self.batteryImg = getImgList("./resources/img/ui/battery.png", 5, 5)
        self.batteryImgWidth, self.batteryImgHeight = self.batteryImg[0].get_size()

        self.cameraToggleImg = getImg("./resources/img/ui/cameratoggle.png", scale=0.7)
        self.cameraToggleBtn = ImageButton(((baseWidth - self.cameraToggleImg.get_width()) // 2, baseHeight - self.cameraToggleImg.get_height() - 30), self.cameraToggleImg, self.cameraToggleImg)

        self.cameraOpenImgFull = getImg("./resources/img/ui/cameraopen.png")
        self.cameraOpenImgWidth = self.cameraOpenImgFull.get_width() // 4
        self.cameraOpenImgHeight = int(self.cameraOpenImgFull.get_height() * (baseWidth / self.cameraOpenImgWidth)) // 3
        self.cameraOpenImg = DirectionalAnimatedImage("./resources/img/ui/cameraopen.png", 11, 4, delayTime=0, scale=(baseWidth / self.cameraOpenImgWidth))

    def draw(self, screen, gameManager):
        self.cameraToggleBtn.draw(screen)
        batteryImgStartY = baseHeight - self.batteryImgHeight - 30
        usageTextSurface = self.smallFont.render(f"Usage:", False, (255, 255, 255))
        screen.blit(usageTextSurface, (30, batteryImgStartY + (self.batteryImgHeight - usageTextSurface.get_height()) // 2))
        for i in range(min(5, len(gameManager.batteryUsage) + 1)):
            screen.blit(self.batteryImg[i], (35 + usageTextSurface.get_width() + self.batteryImgWidth * i, batteryImgStartY))

        powerLeftTextSurface = self.smallFont.render(f"Power left:", False, (255, 255, 255))
        powerTextSurface = self.midFont.render(f"{gameManager.batteryLeft}", False, (255, 255, 255))
        percentTextSurface = self.smallFont.render("%", False, (255, 255, 255))
        powerTextStartY = baseHeight - self.batteryImgHeight - usageTextSurface.get_height() - 50
        screen.blit(powerLeftTextSurface, (30, powerTextStartY + (powerTextSurface.get_height() - powerLeftTextSurface.get_height())))
        screen.blit(powerTextSurface, (35 + powerLeftTextSurface.get_width(), powerTextStartY))
        screen.blit(percentTextSurface, (35 + powerLeftTextSurface.get_width() + powerTextSurface.get_width(), powerTextStartY + (powerTextSurface.get_height() - percentTextSurface.get_height())))
        
        timeTextSurface = self.midFont.render(f"{gameManager.gameTimeText}", False, (255, 255, 255))
        screen.blit(timeTextSurface, (baseWidth - timeTextSurface.get_width() - 30, 30))

        nightTextSurface = self.smallFont.render(f"{gameManager.currentNightText}", False, (255, 255, 255))
        screen.blit(nightTextSurface, (baseWidth - nightTextSurface.get_width() - 35, 65))
