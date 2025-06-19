import pygame

from screen.screenbase import Screen
from widget import *
from const import *


class GameScreen(Screen):
    def __init__(self, gameManager, gameUi, gameOverScreen):
        super().__init__()
        self.font = pygame.font.Font("./resources/font/lcdsolid.ttf", 40)

        self.officeBackgroundImg = getImgList("./resources/img/office/office.png", 7, 1)
        self.leftDoorBtnImg = getImgList("./resources/img/ui/leftdoorbutton.png", 4, 2)
        self.rightDoorBtnImg = getImgList("./resources/img/ui/rightdoorbutton.png", 4, 2)
        self.rightDoorBtnImgWidth = self.rightDoorBtnImg[0].get_width()

        self.rotatedImage = RotatedImage(self.officeBackgroundImg[0], 1.5)

        self.officeBackgroundWidth, self.officeBackgroundHeight = self.officeBackgroundImg[0].get_size()
        self.screenOffset = 0
        self.screenOffsetMaxSpeed = 30
        self.currentBackgroundIndex = 0

        self.gameManager = gameManager
        self.gameUi = gameUi
        self.gameOverScreen = gameOverScreen

        self.leftDoorBtnRect = pygame.Rect(25, 300, 40, 70)
        self.leftLightBtnRect = pygame.Rect(25, 400, 40, 70)
        self.rightDoorBtnRect = pygame.Rect(self.officeBackgroundWidth - self.rightDoorBtnImgWidth - 5, 300, 40, 70)
        self.rightLightBtnRect = pygame.Rect(self.officeBackgroundWidth - self.rightDoorBtnImgWidth - 5, 400, 40, 70)

        self.leftDoorImg = DirectionalAnimatedImage("./resources/img/ui/doormove.png", 16, 6, 0.03, reversed=True)
        self.rightDoorImg = DirectionalAnimatedImage("./resources/img/ui/doormove.png", 16, 6, 0.03)
        self.officeFanImg = AnimatedImage("./resources/img/office/officefan.png", 3, 3)

    def eventHandler(self, events):
        mouseX, mouseY = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                self.nextScreen = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.leftDoorBtnRect.collidepoint(mouseX + self.screenOffset, mouseY):
                    print("왼쪽 문 버튼 눌림!")
                    officeDoorAudio.play()
                    self.gameManager.toggleLeftDoorBtnClicked()
                    if self.gameManager.leftDoorBtnClicked:
                        self.leftDoorImg.direction = 'right'
                    else:
                        self.leftDoorImg.direction = 'left'
                    self.leftDoorImg.startAnimatePlaying()
                elif self.leftLightBtnRect.collidepoint(mouseX + self.screenOffset, mouseY):
                    print("왼쪽 조명 버튼 눌림!")
                    officeLightAudio.play()
                    self.gameManager.setLeftLightBtnClicked(True)
                    if self.gameManager.zannyPos == 'door':
                        self.currentBackgroundIndex = 3
                    else:
                        self.currentBackgroundIndex = 1
                elif self.rightDoorBtnRect.collidepoint(mouseX + self.screenOffset, mouseY):
                    print("오른쪽 문 버튼 눌림!")
                    officeDoorAudio.play()
                    self.gameManager.toggleRightDoorBtnClicked()
                    if self.gameManager.rightDoorBtnClicked:
                        self.rightDoorImg.direction = 'right'
                    else:
                        self.rightDoorImg.direction = 'left'
                    self.rightDoorImg.startAnimatePlaying()
                elif self.rightLightBtnRect.collidepoint(mouseX + self.screenOffset, mouseY):
                    print("오른쪽 조명 버튼 눌림!")
                    officeLightAudio.play()
                    self.gameManager.setRightLightBtnClicked(True)
                    if self.gameManager.ziccaPos == 'door':
                        self.currentBackgroundIndex = 4
                    else:
                        self.currentBackgroundIndex = 2
                elif self.gameUi.cameraToggleBtn.isClicked(event.pos):
                    if not self.gameUi.cameraOpenImg.isAnimatePlaying:
                        print("카메라 켜짐")
                        cameraOpenAudio.play()
                        self.gameUi.cameraOpenImg.direction = 'right'
                        self.gameUi.cameraOpenImg.currentImageIndex = 0
                        self.gameUi.cameraOpenImg.startAnimatePlaying()
            elif event.type == pygame.MOUSEBUTTONUP:
                print("마우스 올림")
                officeLightAudio.stop()
                self.gameManager.setLeftLightBtnClicked(False)
                self.gameManager.setRightLightBtnClicked(False)
                self.currentBackgroundIndex = 0
    
    def initial(self):
        cameraMainAudio.stop()
        cameraKitchenAudio.stop()
        cameraKitchenMoveAudio.stop()
        officeMainAudio.play()
        officeFanAudio.play()

    def draw(self, screen, events):
        if self.gameManager.isGameEnd:
            self.nextScreen = self.gameOverScreen
            self.running = False
        else:
            self.gameManager.gameCalculate()
            self.eventHandler(events)
        
        mouseX, _ = pygame.mouse.get_pos()

        mergedImg = pygame.Surface((self.officeBackgroundWidth, self.officeBackgroundHeight), pygame.SRCALPHA)
        mergedImg.blit(self.officeBackgroundImg[self.currentBackgroundIndex], (0, 0))
        mergedImg.blit(self.officeFanImg.getCurrentImg(), (779, 306))
        
        if self.gameManager.leftDoorBtnClicked:
            mergedImg.blit(self.leftDoorBtnImg[1], (10, 306))
        else:
            mergedImg.blit(self.leftDoorBtnImg[0], (10, 306))
        if self.currentBackgroundIndex == 1 or self.currentBackgroundIndex == 3:
            mergedImg.blit(self.leftDoorBtnImg[3], (10, 392))
        else:
            mergedImg.blit(self.leftDoorBtnImg[2], (10, 392))
        
        rightBtnLocX = self.officeBackgroundWidth - self.rightDoorBtnImgWidth - 10
        if self.gameManager.rightDoorBtnClicked:
            mergedImg.blit(self.rightDoorBtnImg[1], (rightBtnLocX, 306))
        else:
            mergedImg.blit(self.rightDoorBtnImg[0], (rightBtnLocX, 306))
        if self.currentBackgroundIndex == 2 or self.currentBackgroundIndex == 4:
            mergedImg.blit(self.rightDoorBtnImg[3], (rightBtnLocX, 392))
        else:
            mergedImg.blit(self.rightDoorBtnImg[2], (rightBtnLocX, 392))
        
        mergedImg.blit(self.leftDoorImg.getCurrentImg(), (72, 0))
        mergedImg.blit(self.rightDoorImg.getCurrentImg(), (1270, 0))
        
        self.rotatedImage.changeImg(mergedImg)

        screen.fill((200, 200, 200))

        if mouseX > baseWidth * 0.7:
            self.screenOffset += int(self.screenOffsetMaxSpeed * ((mouseX / baseWidth - 0.7) / 0.3))
            self.screenOffset = min(self.screenOffset, self.officeBackgroundWidth - baseWidth)
        elif mouseX < baseWidth * 0.3:
            self.screenOffset -= int(self.screenOffsetMaxSpeed * (1 - mouseX / (baseWidth * 0.3)))
            self.screenOffset = max(0, self.screenOffset)

        self.rotatedImage.draw(screen, self.screenOffset)

        self.gameUi.draw(screen, self.gameManager)
        if self.gameUi.cameraOpenImg.isAnimatePlaying:
            screen.blit(self.gameUi.cameraOpenImg.getCurrentImg(), (0, baseHeight - self.gameUi.cameraOpenImgHeight))
            if self.gameUi.cameraOpenImg.direction == 'right' and self.gameUi.cameraOpenImg.currentImageIndex >= 10:
                self.running = False

        pygame.display.update()
