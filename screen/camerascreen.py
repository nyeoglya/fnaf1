import pygame

from screen.screenbase import Screen
from widget import *

class CameraScreen(Screen):
    def __init__(self, gameManager, gameUi):
        super().__init__()
        self.font = pygame.font.Font("./resources/font/lcdsolid.ttf", 30)

        self.cameraMapBtnImg = getImgList("./resources/img/ui/camerabtn.png", 2, 2, scale=0.8)
        self.cameraMapBtnTextImg = getImgList("./resources/img/ui/camerabtntext.png", 11, 5)
        
        self.backgroundShowStageImgFull = getImg("./resources/img/camera/showstage.png")
        self.backgroundShowStageImgWidth = self.backgroundShowStageImgFull.get_width()
        self.backgroundShowStageImgHeight = self.backgroundShowStageImgFull.get_height() // 7

        self.backgroundBackStageImg = getImgList("./resources/img/camera/backstage.png", 4, 1, scale=(self.backgroundShowStageImgHeight / baseHeight))
        self.backgroundShowStageImg = getImgList("./resources/img/camera/showstage.png", 7, 1, scale=(self.backgroundShowStageImgHeight / baseHeight))
        self.backgroundDiningAreaImg = getImgList("./resources/img/camera/diningarea.png", 6, 1, scale=(self.backgroundShowStageImgHeight / baseHeight))
        self.backgroundEastHallImg = getImgList("./resources/img/camera/easthall.png", 8, 1, scale=(self.backgroundShowStageImgHeight / baseHeight))
        self.backgroundWestHallImg = getImgList("./resources/img/camera/westhall.png", 6, 1, scale=(self.backgroundShowStageImgHeight / baseHeight))
        self.backgroundWestHallFoxyRunImg = DirectionalAnimatedImage("./resources/img/camera/westhallfoxy.png", 31, 1, delayTime=0.02)
        self.backgroundRestroomImg = getImgList("./resources/img/camera/restroom.png", 4, 1, scale=(self.backgroundShowStageImgHeight / baseHeight))
        self.backgroundSupplyClosetImg = getImgList("./resources/img/camera/supplycloset.png", 2, 1, scale=(self.backgroundShowStageImgHeight / baseHeight))
        self.backgroundPirateCoveImg = getImgList("./resources/img/camera/piratecove.png", 5, 1, scale=(self.backgroundShowStageImgHeight / baseHeight))
        self.backgroundKitchenSurface = pygame.Surface((baseWidth, baseHeight))

        backgroundKitchenText1Surface = self.font.render("-CAMERA DISABLED-", False, (255, 255, 255))
        backgroundKitchenText2Surface = self.font.render("AUDIO ONLY", False, (255, 255, 255))
        backgroundKitchenText1Rect = backgroundKitchenText1Surface.get_rect()
        backgroundKitchenText1Rect.centerx = baseWidth // 2
        backgroundKitchenText1Rect.top = 100
        backgroundKitchenText2Rect = backgroundKitchenText2Surface.get_rect()
        backgroundKitchenText2Rect.centerx = baseWidth // 2
        backgroundKitchenText2Rect.top = 140
        self.backgroundKitchenSurface.blit(backgroundKitchenText1Surface, backgroundKitchenText1Rect)
        self.backgroundKitchenSurface.blit(backgroundKitchenText2Surface, backgroundKitchenText2Rect)

        self.flickeringRedCircle = AnimatedImage("resources/img/ui/flickeringcircle.png", 2, 2, delayTime=0.5, scale=0.9)

        self.cameraStaticImg = AnimatedImage("resources/img/effect/static.png", 8, 1, 0.05)
        self.cameraStaticImg.setAlpha(40)

        self.cameraFlickeringImg = DirectionalAnimatedImage("resources/img/effect/blip.png", 17, 1, 0.01)

        self.gameManager = gameManager
        self.gameUi = gameUi

        self.cameraMapImg = getImg("./resources/img/ui/cameramap.png")
        self.cameraImgWidth, self.cameraImgHeight = self.cameraMapImg.get_size()
        self.cameraControlSurfaceLoc = (baseWidth - self.cameraImgWidth - 15, baseHeight - self.cameraImgHeight - 15)
        self.cameraControlSurface = pygame.Surface((self.cameraImgWidth, self.cameraImgHeight), pygame.SRCALPHA)
        self.cameraBackgroundSurface = pygame.Surface((self.backgroundShowStageImgWidth, self.backgroundShowStageImgHeight), pygame.SRCALPHA)

        self.cam1aBtn = ImageButton((110, 20), self.cameraMapBtnImg[0], self.cameraMapBtnImg[1], self.cameraMapBtnTextImg[0], self.cameraControlSurfaceLoc)
        self.cam1bBtn = ImageButton((90, 70), self.cameraMapBtnImg[0], self.cameraMapBtnImg[1], self.cameraMapBtnTextImg[1], self.cameraControlSurfaceLoc)
        self.cam1cBtn = ImageButton((50, 150), self.cameraMapBtnImg[0], self.cameraMapBtnImg[1], self.cameraMapBtnTextImg[2], self.cameraControlSurfaceLoc)
        self.cam2aBtn = ImageButton((110, 275), self.cameraMapBtnImg[0], self.cameraMapBtnImg[1], self.cameraMapBtnTextImg[3], self.cameraControlSurfaceLoc)
        self.cam2bBtn = ImageButton((110, 310), self.cameraMapBtnImg[0], self.cameraMapBtnImg[1], self.cameraMapBtnTextImg[4], self.cameraControlSurfaceLoc)
        self.cam3Btn = ImageButton((40, 250), self.cameraMapBtnImg[0], self.cameraMapBtnImg[1], self.cameraMapBtnTextImg[5], self.cameraControlSurfaceLoc)
        self.cam4aBtn = ImageButton((200, 275), self.cameraMapBtnImg[0], self.cameraMapBtnImg[1], self.cameraMapBtnTextImg[6], self.cameraControlSurfaceLoc)
        self.cam4bBtn = ImageButton((200, 310), self.cameraMapBtnImg[0], self.cameraMapBtnImg[1], self.cameraMapBtnTextImg[7], self.cameraControlSurfaceLoc)
        self.cam5Btn = ImageButton((0, 100), self.cameraMapBtnImg[0], self.cameraMapBtnImg[1], self.cameraMapBtnTextImg[8], self.cameraControlSurfaceLoc)
        self.cam6Btn = ImageButton((310, 240), self.cameraMapBtnImg[0], self.cameraMapBtnImg[1], self.cameraMapBtnTextImg[9], self.cameraControlSurfaceLoc)
        self.cam7Btn = ImageButton((320, 100), self.cameraMapBtnImg[0], self.cameraMapBtnImg[1], self.cameraMapBtnTextImg[10], self.cameraControlSurfaceLoc)
        
        self.cameraBtnMap = {
            self.cam1aBtn: 'cam1a',
            self.cam1bBtn: 'cam1b',
            self.cam1cBtn: 'cam1c',
            self.cam2aBtn: 'cam2a',
            self.cam2bBtn: 'cam2b',
            self.cam3Btn: 'cam3',
            self.cam4aBtn: 'cam4a',
            self.cam4bBtn: 'cam4b',
            self.cam5Btn: 'cam5',
            self.cam6Btn: 'cam6',
            self.cam7Btn: 'cam7'
        }
        self.cameraImgMap = {
            'cam1a': (self.backgroundShowStageImg, 0),
            'cam1b': (self.backgroundDiningAreaImg, 0),
            'cam1c': (self.backgroundPirateCoveImg, 0),
            'cam2a': (self.backgroundWestHallImg, 3),
            'cam2b': (self.backgroundWestHallImg, 0),
            'cam3': (self.backgroundSupplyClosetImg, 0),
            'cam4a': (self.backgroundEastHallImg, 0),
            'cam4b': (self.backgroundEastHallImg, 4),
            'cam5': (self.backgroundBackStageImg, 0),
            'cam6': ([self.backgroundKitchenSurface], 0),
            'cam7': (self.backgroundRestroomImg, 0),
        }
        self.cameraImgStateMap = { # freddy, bonny, chicca
            'cam1a': {
                'ooo': 0,
                'oxo': 2,
                'oox': 3,
                'oxx': 4,
                'xxx': 6
            },
            'cam1b': {
                'xxx': 0,
                'xox': 1,
                'xxo': 3,
                'xoo': 4,
                'oxx': 5,
            },
            'cam2a': {
                'xxx': 3,
                'xox': 5,
            },
            'cam2b': {
                'xxx': 0,
                'xox': 2,
            },
            'cam3': {
                'xxx': 0,
                'xox': 1,
            },
            'cam4a': {
                'xxx': 0,
                'oxx': 1,
                'oxo': 2,
                'xxo': 3,
            },
            'cam4b': {
                'xxx': 4,
                'xxo': 5,
                'oxo': 6,
                'oxx': 7,
            },
            'cam5': {
                'xxx': 0,
                'xox': 3,
            },
            'cam6': {
                'xxx': 0,
                'oxx': 0,
                'xxo': 0,
                'oxo': 0
            },
            'cam7': {
                'xxx': 0,
                'oxo': 1,
                'xxo': 2,
                'oxx': 3,
            },
        }
        self.cameraLocTextMap = {
            'cam1a': 'Show Stage',
            'cam1b': 'Dining Area',
            'cam1c': 'Priate\'s Cove',
            'cam2a': 'W. Hall',
            'cam2b': 'W. Hall Corner',
            'cam3': 'Supply Closet',
            'cam4a': 'E. Hall',
            'cam4b': 'E. Hall Corner',
            'cam5': 'Back Stage',
            'cam6': 'Kitchen',
            'cam7': 'Restroom',
        }
        self.currentBtn = self.cam1aBtn
        self.currentBtn.setHovered(True)

        self.hoxyRunning = False

        self.offsetX = 0
        self.offsetDirection = 'right'
        self.offsetMoveSpeed = 2
        # TODO: 한쪽 끝에 도달하면 잠깐 멈췄다가 다른 쪽으로 이동하기
        # self.idleMax = 1
        # self.idleCurrent = 0
    
    def resetGame(self):
        self.currentBtn.setHovered(False)
        self.currentBtn = self.cam1aBtn
        self.currentBtn.setHovered(True)

        self.cameraImgMap = {
            'cam1a': (self.backgroundShowStageImg, 0),
            'cam1b': (self.backgroundDiningAreaImg, 0),
            'cam1c': (self.backgroundPirateCoveImg, 0),
            'cam2a': (self.backgroundWestHallImg, 3),
            'cam2b': (self.backgroundWestHallImg, 0),
            'cam3': (self.backgroundSupplyClosetImg, 0),
            'cam4a': (self.backgroundEastHallImg, 0),
            'cam4b': (self.backgroundEastHallImg, 4),
            'cam5': (self.backgroundBackStageImg, 0),
            'cam6': ([self.backgroundKitchenSurface], 0),
            'cam7': (self.backgroundRestroomImg, 0),
        }

        self.hoxyRunning = False
    
    def changeFoxyState(self):
        self.cameraImgMap['cam1c'] = (self.backgroundPirateCoveImg, self.gameManager.hoxyStageLevel)
        if self.gameManager.hoxyPos == 'running' and not self.hoxyRunning:
            self.backgroundWestHallFoxyRunImg.currentImageIndex = min(30, self.gameManager.foxyRunFrameShift)
            self.backgroundWestHallFoxyRunImg.startAnimatePlaying()
            self.hoxyRunning = True
        elif self.gameManager.hoxyPos == 'fail':
            self.hoxyRunning = False

    def changeCameraState(self, stateQuery):
        posState, animatronicsLoc = stateQuery
        zzaihongPos, zannyPos, ziccaPos, hoxyPos = animatronicsLoc
        if posState in ['door', 'fail', 'cam1c', 'running']:
            return

        locValue = ''
        if zzaihongPos == posState:
            locValue += 'o'
        else:
            locValue += 'x'
        if zannyPos == posState:
            locValue += 'o'
        else:
            locValue += 'x'
        if ziccaPos == posState:
            locValue += 'o'
        else:
            locValue += 'x'
        
        imgData, _ = self.cameraImgMap[posState]
        print("inspect:", posState, locValue)
        self.cameraImgMap[posState] = (imgData, self.cameraImgStateMap[posState][locValue])

    def resolveCameraQuery(self):
        for stateQuery in self.gameManager.cameraStateChangeQueryMap.items():
            self.changeCameraState(stateQuery)
        self.gameManager.cameraStateChangeQueryMap = dict()

        clickedBtnText = self.cameraBtnMap[self.currentBtn]
        self.updateCameraBackgroundSurface(self.cameraImgMap[clickedBtnText])

    def eventHandler(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                self.nextScreen = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.cameraBtnMap.keys():
                    if btn.isClicked(event.pos) and btn != self.currentBtn:
                        clickedBtnText = self.cameraBtnMap[btn]
                        self.updateCameraBackgroundSurface(self.cameraImgMap[clickedBtnText])
                        print(self.cameraBtnMap[btn], "버튼이 클릭되었습니다!")
                        if self.cameraBtnMap[btn] == 'cam6':
                            cameraErrorAudio.play()
                            cameraKitchenAudio.play()
                            if self.gameManager.zzaihongPos == 'cam6' or self.gameManager.ziccaPos == 'cam6':
                                cameraKitchenMoveAudio.play()
                        else:
                            cameraKitchenAudio.stop()
                            cameraKitchenMoveAudio.stop()
                        cameraBlipAudio.play()
                        self.cameraFlickeringImg.direction = 'right'
                        self.cameraFlickeringImg.currentImageIndex = 0
                        self.cameraFlickeringImg.startAnimatePlaying()
                        btn.setHovered(True)
                        self.currentBtn.setHovered(False)
                        self.currentBtn = btn
                if self.gameUi.cameraToggleBtn.isClicked(event.pos):
                    print("카메라 꺼짐")
                    cameraCloseAudio.play()
                    self.gameUi.cameraOpenImg.direction = 'left'
                    self.gameUi.cameraOpenImg.startAnimatePlaying()
                    self.gameManager.setIsCameraOn(False)
                    self.running = False

    def initial(self):
        self.resolveCameraQuery()
        self.gameManager.setIsCameraOn(True)

        self.backgroundWestHallFoxyRunImg.currentImageIndex = min(30, self.gameManager.foxyRunFrameShift)

        cameraMainAudio.play()
        officeFanAudio.stop()

    def draw(self, screen, events):
        if self.gameManager.isGameEnd:
            self.running = False
            return
        
        self.eventHandler(events)
        self.gameManager.gameCalculate()
        self.gameManager.cameraPos = self.cameraBtnMap[self.currentBtn]

        self.changeFoxyState()
        
        self.updateCameraControlSurface()

        if self.backgroundShowStageImgWidth + self.offsetX < baseWidth and self.offsetDirection == 'right':
            self.offsetDirection = 'left'
        elif self.offsetX > 0 and self.offsetDirection == 'left':
            self.offsetDirection = 'right'

        screen.fill((0, 0, 0, 0))
        if self.gameManager.cameraPos == 'cam6':
            screen.blit(self.cameraBackgroundSurface, (0, 0))
        elif self.gameManager.hoxyPos == 'running' and self.backgroundWestHallFoxyRunImg.currentImageIndex < 30 and self.cameraBtnMap[self.currentBtn] == 'cam2a':
            screen.blit(self.backgroundWestHallFoxyRunImg.getCurrentImg(), (self.offsetX, 0))
        elif self.gameManager.hoxyPos == 'cam2a' and self.cameraBtnMap[self.currentBtn] == 'cam2a':
            screen.blit(self.backgroundWestHallFoxyRunImg.imageList[0], (self.offsetX, 0))
        else:
            screen.blit(self.cameraBackgroundSurface, (self.offsetX, 0))

        if self.cameraFlickeringImg.isAnimatePlaying and self.cameraFlickeringImg.currentImageIndex < 5:
            screen.blit(self.cameraFlickeringImg.getCurrentImg(), (0, 0))
        
        screen.blit(self.cameraStaticImg.getCurrentImg(), (0, 0))
        screen.blit(self.font.render(self.cameraLocTextMap[self.gameManager.cameraPos], True, (255, 255, 255)), (baseWidth - self.cameraImgWidth - 15, baseHeight - self.cameraImgHeight - 45))
        pygame.draw.rect(screen, (255, 255, 255), (15, 15, baseWidth - 30, baseHeight - 30), 2)
        screen.blit(self.flickeringRedCircle.getCurrentImg(), (40, 40))
        screen.blit(self.cameraControlSurface, self.cameraControlSurfaceLoc)

        if self.offsetDirection == 'left':
            self.offsetX += self.offsetMoveSpeed
        elif self.offsetDirection == 'right':
            self.offsetX -= self.offsetMoveSpeed

        self.gameUi.draw(screen, self.gameManager)

        pygame.display.update()
    
    def updateCameraControlSurface(self):
        self.cameraControlSurface.fill((0, 0, 0, 0))
        self.cameraControlSurface.blit(self.cameraMapImg, (0, 0))
        for btn in self.cameraBtnMap.keys():
            btn.draw(self.cameraControlSurface)
    
    def updateCameraBackgroundSurface(self, data):
        imgList, index = data
        self.cameraBackgroundSurface.fill((0, 0, 0, 0))
        self.cameraBackgroundSurface.blit(imgList[index], (0, 0))
