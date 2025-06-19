import pygame
from screen.screenbase import Screen
from widget import *
from const import *

class IntroScreen(Screen):
    def __init__(self, gameManager):
        super().__init__()
        self.font = pygame.font.Font("./resources/font/d2coding.ttf", 30)
        self.pointTextLoc = 400
        
        self.gameManager = gameManager

        self.introBackgroundImg = getImg("resources/img/screen/intro.png")
        self.introText = [
            "백수인 당신은 구인 공고를 보고 짜이홍의 피자가게에 지원했다.",
            "낮에는 즐123거운 이곳.",
            "그러나 당신의 근무 시간은 낮이 아니다.",
            "제한된 전력, 제한된 시야, 그리고 제한된 시간..."
        ]
        self.typingText = 0

        self.introTitleText = "Five Nights at Zzaihong's"
        self.introTimeText = "12 AM"

        self.screenStep = 0
        self.currentAlpha = 0
        self.sleepTime = 0

    def typing(self, text):
        self.typingText = min(self.typingText + 1, len(text))
        return text[:self.typingText]

    def renderText(self, screen, text, pos, alpha=255):
        surface = self.font.render(text, False, (255, 255, 255))
        surface.set_alpha(alpha)
        screen.blit(surface, pos)

    def renderTextCentered(self, screen, text, centerPos, alpha=255):
        surface = self.font.render(text, False, (255, 255, 255))
        surface.set_alpha(alpha)
        rect = surface.get_rect(center=centerPos)
        screen.blit(surface, rect)

    def handleEvent(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            self.nextScreen = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.advanceStep()

    def advanceStep(self):
        if self.screenStep == 0 and self.currentAlpha >= 250:
            self.screenStep = 1
        elif 2 <= self.screenStep <= 4 and self.typingText >= len(self.introText[self.screenStep-2]):
            self.screenStep += 1
            self.typingText = 0
        elif self.screenStep == 5 and self.typingText >= len(self.introText[3]):
            self.screenStep = 6
            self.currentAlpha = 255
        elif self.screenStep == 6 and self.currentAlpha <= 0:
            self.screenStep = 7
            self.currentAlpha = 0
        elif self.screenStep in (7, 8) and self.currentAlpha >= 250:
            self.screenStep += 1
            self.currentAlpha = 0
            if self.screenStep == 9:
                self.sleepTime = 30
        elif self.screenStep == 9 and self.sleepTime <= 0:
            self.screenStep = 10
            self.currentAlpha = 255
        elif self.screenStep == 10 and self.currentAlpha <= 0:
            self.gameManager.resetGame()
            self.running = False

    def drawTextBlock(self, screen, lines, alpha=255):
        for i, text in enumerate(lines):
            self.renderText(screen, text, (50, 50 + i * 70), alpha)

    def draw(self, screen, events):
        for event in events:
            self.handleEvent(event)

        screen.fill((0, 0, 0))

        if self.screenStep == 0:
            titleMainAudio.stop()
            titleStaticAudio.stop()
            self.introBackgroundImg.set_alpha(self.currentAlpha)
            screen.blit(self.introBackgroundImg, (0, 0))
            self.currentAlpha = min(self.currentAlpha + 5, 255)

        elif self.screenStep == 1:
            self.introBackgroundImg.set_alpha(self.currentAlpha)
            screen.blit(self.introBackgroundImg, (0, 0))
            self.currentAlpha = max(self.currentAlpha - 5, 0)
            if self.currentAlpha <= 0:
                self.screenStep = 2

        elif 2 <= self.screenStep <= 5:
            self.drawTextBlock(screen, self.introText[:self.screenStep-2])
            currentLine = self.typing(self.introText[self.screenStep - 2])
            self.renderText(screen, currentLine, (50, 50 + (self.screenStep - 2) * 70))

        elif self.screenStep == 6:
            self.drawTextBlock(screen, self.introText, self.currentAlpha)
            self.currentAlpha = max(self.currentAlpha - 20, 0)
            self.advanceStep()

        elif self.screenStep == 7:
            self.renderTextCentered(screen, self.introTitleText, (screen.get_width() // 2, screen.get_height() // 2), self.currentAlpha)
            self.currentAlpha = min(self.currentAlpha + 5, 255)
            self.advanceStep()

        elif self.screenStep == 8:
            self.renderTextCentered(screen, self.introTitleText, (screen.get_width() // 2, screen.get_height() // 2))
            self.renderTextCentered(screen, self.introTimeText, (screen.get_width() // 2, screen.get_height() // 2 + 50), self.currentAlpha)
            self.currentAlpha = min(self.currentAlpha + 10, 255)
            self.advanceStep()

        elif self.screenStep == 9:
            self.renderTextCentered(screen, self.introTitleText, (screen.get_width() // 2, screen.get_height() // 2))
            self.renderTextCentered(screen, self.introTimeText, (screen.get_width() // 2, screen.get_height() // 2 + 50))
            self.sleepTime -= 1
            self.advanceStep()

        elif self.screenStep == 10:
            self.renderTextCentered(screen, self.introTitleText, (screen.get_width() // 2, screen.get_height() // 2), self.currentAlpha)
            self.renderTextCentered(screen, self.introTimeText, (screen.get_width() // 2, screen.get_height() // 2 + 50), self.currentAlpha)
            self.currentAlpha = max(self.currentAlpha - 5, 0)
            self.advanceStep()

        pygame.display.update()
