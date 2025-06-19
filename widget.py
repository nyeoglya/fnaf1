import time
import math

import pygame

from const import *


class Button:
    def __init__(self, rect, text, font, textColor, clickOffset=(0,0)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.textColor = textColor
        self.clickOffset = clickOffset
        self.textSurface = self.font.render(self.text, True, self.textColor)
        
    def draw(self, screen):
        screen.blit(self.textSurface, self.rect)

    def isHovered(self, pos=(0,0)):
        posX, posY = pos
        return self.rect.collidepoint(posX - self.clickOffset[0], posY - self.clickOffset[1])

class ImageButton:
    def __init__(self, pos, baseImg, hoverImg, textImg=None, clickOffset=(0,0)):
        self.baseImg = baseImg
        self.hoverImg = hoverImg
        self.textImg = textImg
        if textImg == None:
            self.textImg = pygame.Surface((0,0))
        self.clickOffset = clickOffset

        self.imgWidth, self.imgHeight = self.baseImg.get_size()
        self.rect = pygame.Rect(pos[0], pos[1], self.imgWidth, self.imgHeight)
        self.textImgRect = ((self.imgWidth - self.textImg.get_width()) // 2, (self.imgHeight - self.textImg.get_height()) // 2)
        self.hovered = False

        self.btnSurface = pygame.Surface((self.imgWidth, self.imgHeight), pygame.SRCALPHA)

    def draw(self, screen):
        if self.hovered:
            self.btnSurface.blit(self.hoverImg, (0,0))
        else:
            self.btnSurface.blit(self.baseImg, (0,0))
        self.btnSurface.blit(self.textImg, self.textImgRect)

        screen.blit(self.btnSurface, self.rect)

    def setHovered(self, hovered):
        self.hovered = hovered
    
    def isClicked(self, pos=(0,0)):
        posX, posY = pos
        return self.rect.collidepoint(posX - self.clickOffset[0], posY - self.clickOffset[1])

def getImg(path, scale=1.0):
    image = pygame.image.load(path).convert_alpha()
    w, h = image.get_size()
    newSize = (int(w * scale), int(h * scale))
    return pygame.transform.smoothscale(image, newSize)

def getImgList(path, totalCount, widthCount, scale=1.0):
    image = getImg(path, scale)
    
    heightCount = totalCount // widthCount
    if totalCount % widthCount != 0: heightCount += 1
    
    cropWidth = image.get_width() // widthCount
    cropHeight = image.get_height() // heightCount

    imgList = []
    k = 0
    for i in range(heightCount):
        for j in range(widthCount):
            cropRect = pygame.Rect(cropWidth * j, cropHeight * i, cropWidth, cropHeight)
            imgList.append(image.subsurface(cropRect).copy())
            k += 1
            if k >= totalCount:
                break

    return imgList

class AnimatedImage:
    def __init__(self, path, totalCount, widthCount, delayTime=0.2, scale=1.0):
        self.imageList = getImgList(path, totalCount, widthCount, scale)
        self.delayTime = delayTime
        self.savedTime = 0.0
        self.currentImageIndex = 0
    
    def setAlpha(self, value):
        if 0 <= value <= 255:
            for image in self.imageList:
                image.set_alpha(value)

    def getCurrentImg(self):
        currentTime = time.time()
        if currentTime - self.savedTime > self.delayTime:
            self.savedTime = currentTime
            self.currentImageIndex += 1
            if self.currentImageIndex >= len(self.imageList):
                self.currentImageIndex = 0

        return self.imageList[self.currentImageIndex]

class DirectionalAnimatedImage(AnimatedImage):
    def __init__(self, path, totalCount, widthCount, delayTime=0.2, scale=1.0, reversed=False):
        super().__init__(path, totalCount, widthCount, delayTime, scale)
        self.isAnimatePlaying = False
        self.direction = 'right'

        if reversed:
            for i in range(len(self.imageList)):
                self.imageList[i] = pygame.transform.flip(self.imageList[i], True, False)
    
    def startAnimatePlaying(self):
        self.isAnimatePlaying = True
        self.savedTime = time.time()

    def getCurrentImg(self):
        currentTime = time.time()
        if self.isAnimatePlaying and currentTime - self.savedTime > self.delayTime:
            self.savedTime = currentTime
            
            if self.direction == 'right':
                self.currentImageIndex += 1
            elif self.direction == 'left':
                self.currentImageIndex -= 1
            
            if self.currentImageIndex >= len(self.imageList):
                self.currentImageIndex = len(self.imageList) - 1
                self.isAnimatePlaying = False
            elif self.currentImageIndex < 0:
                self.currentImageIndex = 0
                self.isAnimatePlaying = False
        
        return self.imageList[self.currentImageIndex]

class RotatedImage:
    def __init__(self, image, compressRatio):
        self.image = image
        self.compressRatio = compressRatio

        self.imageWidth, self.imageHeight = self.image.get_size()

        self.imgFilter = []
        adjust = 1 - 1 / self.compressRatio
        for i in range(baseWidth):
            xNorm = i / baseWidth - 0.5
            projRatio = 1 - math.sqrt(max(0, 1 - xNorm ** 2)) / self.compressRatio
            self.imgFilter.append((xNorm, projRatio / adjust))
    
    def changeImg(self, newImg):
        self.image = newImg

    def draw(self, screen, offsetX):
        offsetIndex = max(0, min(int(offsetX), self.imageWidth - baseWidth))
        drawCount = min(baseWidth, self.imageWidth - offsetIndex)

        for i in range(drawCount):
            sliceIndex = offsetIndex + i
            xNorm, projRatio = self.imgFilter[i]
            projHeight = int(self.imageHeight * projRatio)
            drawX = int(baseWidth * (xNorm + 0.5))
            
            rect = pygame.Rect(sliceIndex, 0, 1, self.imageHeight)
            slicedImg = self.image.subsurface(rect)
            scaled = pygame.transform.smoothscale(slicedImg, (1, projHeight))

            screen.blit(scaled, (drawX, (self.imageHeight - projHeight) // 2))
            screen.blit(scaled, (drawX + 1, (self.imageHeight - projHeight) // 2))
