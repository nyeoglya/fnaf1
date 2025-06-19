import random

import pygame

from screen.screenbase import Screen
from widget import *
from const import *


class GameOverScreen(Screen):
    def __init__(self, gameManager):
        super().__init__()
        self.font = pygame.font.Font("./resources/font/lcdsolid.ttf", 40)

        self.gameManager = gameManager

        self.officeBackgroundImg = getImgList("./resources/img/office/office.png", 7, 1)
        self.officeBackgroundWidth, self.officeBackgroundHeight = self.officeBackgroundImg[0].get_size()

        self.jumpscareZzaihong = DirectionalAnimatedImage("./resources/img/jumpscare/zzaihong.png", 28, 1, 0.03, scale=(self.officeBackgroundHeight / baseHeight))
        self.jumpscareZanny = DirectionalAnimatedImage("./resources/img/jumpscare/zanny.png", 11, 1, 0.03, scale=(self.officeBackgroundHeight / baseHeight))
        self.jumpscareZicca = DirectionalAnimatedImage("./resources/img/jumpscare/zicca.png", 16, 1, 0.03, scale=(self.officeBackgroundHeight / baseHeight))
        self.jumpscareHoxy = DirectionalAnimatedImage("./resources/img/jumpscare/hoxy.png", 21, 1, 0.03, scale=(self.officeBackgroundHeight / baseHeight))
        self.jumpscareBatteryOut = DirectionalAnimatedImage("./resources/img/jumpscare/batteryout.png", 21, 1, 0.03, scale=(self.officeBackgroundHeight / baseHeight))

        self.staticImg = AnimatedImage("resources/img/effect/static.png", 8, 1, 0.05)

        self.backgroundBatteryOut = self.officeBackgroundImg[5]
        self.backgroundBatteryOutWithZzaihong = self.officeBackgroundImg[6]
        self.sceneIndex = 0
        self.batteryOutZzaihongDelay = 0
        self.batteryOutScenePeriod = [100, 1, 40, 1, 30, 1, 20, 1, 10, 1] + [5, 1] * 15 + [random.randint(50, 100), 1]

        self.winDelay = 0

        self.tempImage = None
        self.repeatedTime = 0
    
    def eventHandler(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                self.nextScreen = None

    def getGameOverCurrentImg(self, gameOverType):
        if gameOverType == "zzaihong":
            if self.sceneIndex == 0:
                if not self.jumpscareZzaihong.isAnimatePlaying and self.repeatedTime < 2:
                    self.jumpscareZzaihong.startAnimatePlaying()
                    self.repeatedTime += 1
                if self.repeatedTime >= 2 and self.tempImage == self.jumpscareZzaihong.getCurrentImg():
                    self.sceneIndex = -1
                self.tempImage = self.jumpscareZzaihong.getCurrentImg()
                return self.tempImage
        
        elif gameOverType == "zanny":
            if self.sceneIndex == 0:
                if not self.jumpscareZanny.isAnimatePlaying and self.repeatedTime < 3:
                    self.jumpscareZanny.startAnimatePlaying()
                    self.jumpscareZanny.currentImageIndex = 0
                    self.repeatedTime += 1
                if self.repeatedTime >= 3 and self.tempImage == self.jumpscareZanny.getCurrentImg():
                    self.sceneIndex = -1
                self.tempImage = self.jumpscareZanny.getCurrentImg()
                return self.tempImage

        elif gameOverType == "zicca":
            if self.sceneIndex == 0:
                if not self.jumpscareZicca.isAnimatePlaying and self.repeatedTime < 3:
                    self.jumpscareZicca.startAnimatePlaying()
                    self.jumpscareZicca.currentImageIndex = 0
                    self.repeatedTime += 1
                if self.repeatedTime >= 3 and self.tempImage == self.jumpscareZicca.getCurrentImg():
                    self.sceneIndex = -1
                self.tempImage = self.jumpscareZicca.getCurrentImg()
                return self.tempImage

        elif gameOverType == "hoxy":
            if self.sceneIndex == 0:
                if not self.jumpscareHoxy.isAnimatePlaying and self.repeatedTime < 2:
                    self.jumpscareHoxy.startAnimatePlaying()
                    self.repeatedTime += 1
                if self.repeatedTime >= 2 and self.tempImage == self.jumpscareHoxy.getCurrentImg():
                    self.sceneIndex = -1
                self.tempImage = self.jumpscareHoxy.getCurrentImg()
                return self.tempImage
        
        elif gameOverType == "batteryout":
            if self.sceneIndex == 0:
                self.batteryOutZzaihongDelay = 1
                self.sceneIndex = 1
                return self.officeBackgroundImg[5]
            elif self.sceneIndex == 1:
                self.batteryOutZzaihongDelay -= 1
                
                if self.batteryOutZzaihongDelay <= 0:
                    self.batteryOutZzaihongDelay = self.batteryOutScenePeriod[self.repeatedTime]
                    self.repeatedTime += 1
                if self.repeatedTime >= len(self.batteryOutScenePeriod):
                    self.sceneIndex = 2
                    return self.officeBackgroundImg[5]

                selectedBatteryImg = None
                if self.repeatedTime % 2 == 0:
                    selectedBatteryImg = self.officeBackgroundImg[6]
                else:
                    selectedBatteryImg = self.officeBackgroundImg[5]
                return selectedBatteryImg
            elif self.sceneIndex == 2:
                musicBoxAudio.stop()
                if not self.jumpscareBatteryOut.isAnimatePlaying:
                    screamAudio.play()
                    self.jumpscareBatteryOut.startAnimatePlaying()
                if self.tempImage == self.jumpscareBatteryOut.getCurrentImg():
                    self.sceneIndex = -1
                self.tempImage = self.jumpscareBatteryOut.getCurrentImg()
                return self.tempImage
        
        elif gameOverType == "win":
            if self.winDelay == 100:
                winYayAudio.play()
            if self.winDelay >= 350:
                winMainAudio.stop()
                winYayAudio.stop()
                self.sceneIndex = -1
            else:
                self.winDelay += 1
                
                winSurface = pygame.Surface((baseWidth, baseHeight), pygame.SRCALPHA)
                winSurface.fill((0, 0, 0))

                text5 = self.font.render("5 AM", True, (255, 255, 255))
                text6 = self.font.render("6 AM", True, (255, 255, 255))
                maxOffset = text5.get_height()

                center = winSurface.get_rect().center
                rect5 = text5.get_rect(center=center)
                rect6 = text6.get_rect(center=center)

                yOffset = self.winDelay - 50
                if self.winDelay < 50:
                    winSurface.blit(text5, rect5)
                elif yOffset < maxOffset:
                    rect5.y += yOffset
                    rect6.y -= maxOffset - yOffset

                    winSurface.blit(text6, rect6)
                    winSurface.blit(text5, rect5)
                    maskTop = center[1] - maxOffset // 2
                    maskBottom = center[1] + maxOffset // 2
                    pygame.draw.rect(winSurface, (0,0,0), (0, 0, baseWidth, maskTop))
                    pygame.draw.rect(winSurface, (0,0,0), (0, maskBottom, baseWidth, baseHeight - maskBottom))
                else:
                    winSurface.blit(text6, rect6)
                
                return winSurface

        if self.sceneIndex == -1:
            screamAudio.stop()
            
            self.repeatedTime += 1
            if self.repeatedTime >= 30:
                self.running = False
            return self.staticImg.getCurrentImg()
    
    def initial(self):
        cameraMainAudio.stop()
        cameraKitchenAudio.stop()
        cameraKitchenMoveAudio.stop()
        officeMainAudio.stop()
        officeFanAudio.stop()

        if self.gameManager.gameEndReason not in ['win', 'batteryout']:
            screamAudio.play()
        elif self.gameManager.gameEndReason == 'batteryout':
            musicBoxAudio.play()
        elif self.gameManager.gameEndReason == 'win':
            winMainAudio.play()
        
        self.sceneIndex = 0
        self.batteryOutZzaihongDelay = 0
        self.winDelay = 0
        self.tempImage = None
        self.repeatedTime = 0

    def draw(self, screen, events):
        self.eventHandler(events)

        screen.fill((200, 200, 200))
        currentGameOverImg = self.getGameOverCurrentImg(self.gameManager.gameEndReason)
        jumpscareImgRect = currentGameOverImg.get_rect(center=screen.get_rect().center)
        if self.gameManager.gameEndReason == "batteryout" or self.gameManager.gameEndReason == "hoxy":
            jumpscareImgRect = (0, 0)
        screen.blit(currentGameOverImg, jumpscareImgRect)
        
        pygame.display.update()
