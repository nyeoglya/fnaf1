import random
import time

import pygame
from const import *


class GameManager:
    def __init__(self):
        self.zzaihongLevel = 1
        self.zannyLevel = 2
        self.ziccaLevel = 4
        self.hoxyLevel = 3

        self.zzaihongPos = 'cam1a'
        self.zannyPos = 'cam1a'
        self.ziccaPos = 'cam1a'
        self.hoxyPos = 'cam1c'
        self.hoxyStageLevel = 0
        
        self.batteryLeft = 100
        self.batteryUsage = set()
        self.batteryDecreaseUnitTime = 1.2
        self.gameStartTime = time.time()
        self.batteryDecreaseTime = self.batteryDecreaseUnitTime
        self.gameTimeCurrent = self.gameStartTime
        self.gameTimeInterval = 90
        self.gameTimeText = "12 AM"
        self.currentNight = 1
        self.currentNightText = "Night 1"

        self.isCameraOn = False
        self.cameraPos = 'cam1a'

        self.isGameEnd = False
        self.gameEndReason = ''

        self.leftDoorBtnClicked = False
        self.rightDoorBtnClicked = False
        self.leftLightBtnClicked = False
        self.rightLightBtnClicked = False

        self.zzaihongLocMap = {
            'cam1a': ['cam7'],
            'cam7': ['cam6'],
            'cam6': ['cam4a'],
            'cam4a': ['cam4b'],
            'cam4b': ['door'],
            'fail': ['cam6', 'cam4a']
        }

        self.zannyLocMap = {
            'cam1a': ['cam1b', 'cam5'],
            'cam1b': ['cam5', 'cam2a', 'cam3'],
            'cam5': ['cam1b', 'cam2a'],
            'cam3': ['cam2a'],
            'cam2a': ['cam3', 'cam2b'],
            'cam2b': ['door'],
            'fail': ['cam1b', 'cam3', 'cam2a']
        }

        self.ziccaLocMap = {
            'cam1a': ['cam1b'],
            'cam1b': ['cam7', 'cam6'],
            'cam7': ['cam6', 'cam4a'],
            'cam6': ['cam7', 'cam4a'],
            'cam4a': ['cam6', 'cam4b'],
            'cam4b': ['cam4a', 'door'],
            'fail': ['cam4a', 'cam6']
        }

        self.hoxyLocMap = {
            'cam1c': ['cam2a'],
            'cam2a': ['running'],
            'running': ['door'],
            'fail': ['cam1c']
        }

        initialBehaveTime = time.time() + 5.0
        self.nextBehaveDict = {
            'zzaihong': initialBehaveTime,
            'zanny': initialBehaveTime,
            'zicca': initialBehaveTime,
            'hoxy': initialBehaveTime
        }

        self.foxyRunFrameShift = 0

        self.cameraStateChangeQueryMap = dict()
    
    def resetGame(self):
        self.zzaihongPos = 'cam1a'
        self.zannyPos = 'cam1a'
        self.ziccaPos = 'cam1a'
        self.hoxyPos = 'cam1c'
        self.hoxyStageLevel = 0
        
        self.batteryLeft = 100
        self.batteryUsage = set()
        self.gameStartTime = time.time()
        self.batteryDecreaseTime = self.batteryDecreaseUnitTime
        self.gameTimeCurrent = self.gameStartTime
        self.gameTimeText = "12 AM"

        self.isCameraOn = False
        self.cameraPos = 'cam1a'

        self.isGameEnd = False
        self.gameEndReason = ''

        self.leftDoorBtnClicked = False
        self.rightDoorBtnClicked = False
        self.leftLightBtnClicked = False
        self.rightLightBtnClicked = False

        initialBehaveTime = time.time() + 5.0
        self.nextBehaveDict = {
            'zzaihong': initialBehaveTime,
            'zanny': initialBehaveTime,
            'zicca': initialBehaveTime,
            'hoxy': initialBehaveTime
        }

        self.foxyRunFrameShift = 0

    
    def setGameEndWithReason(self, reason):
        self.isGameEnd = True
        self.gameEndReason = reason
        print(f"게임이 끝났다. 사유: {reason}")
    
    def toggleLeftDoorBtnClicked(self):
        if self.leftDoorBtnClicked:
            self.batteryUsage.discard('ld')
        elif not self.leftDoorBtnClicked:
            self.batteryUsage.add('ld')
        self.leftDoorBtnClicked = not self.leftDoorBtnClicked

    def toggleRightDoorBtnClicked(self):
        if self.rightDoorBtnClicked:
            self.batteryUsage.discard('rd')
        elif not self.rightDoorBtnClicked:
            self.batteryUsage.add('rd')
        self.rightDoorBtnClicked = not self.rightDoorBtnClicked
    
    def setLeftLightBtnClicked(self, value):
        if value:
            self.batteryUsage.add('ll')
        else:
            self.batteryUsage.discard('ll')
        self.leftLightBtnClicked = value
    
    def setRightLightBtnClicked(self, value):
        if value:
            self.batteryUsage.add('rl')
        else:
            self.batteryUsage.discard('rl')
        self.rightLightBtnClicked = value
    
    def setIsCameraOn(self, value):
        if value:
            self.batteryUsage.add('cam')
        else:
            self.batteryUsage.discard('cam')
        self.isCameraOn = value
    
    def getAnimatronicsLevel(self, name):
        if name == 'zzaihong':
            return self.zzaihongLevel
        elif name == 'zanny':
            return self.zannyLevel
        elif name == 'zicca':
            return self.ziccaLevel
        elif name == 'hoxy':
            return self.hoxyLevel
    
    def tryAttack(self, name):
        print(f"{name} 공격 시도!")
        if name == 'zzaihong':
            if not self.rightDoorBtnClicked:
                self.setGameEndWithReason('zzaihong')
                return True
            else:
                officeKnockAudio.play()
                self.zzaihongPos = 'fail'
                return False
        elif name == 'zanny':
            if not self.leftDoorBtnClicked:
                self.setGameEndWithReason('zanny')
                return True
            else:
                officeKnockAudio.play()
                self.zannyPos = 'fail'
                return False
        elif name == 'zicca':
            if not self.rightDoorBtnClicked:
                self.setGameEndWithReason('zicca')
                return True
            else:
                officeKnockAudio.play()
                self.ziccaPos = 'fail'
                return False
        if name == 'hoxy':
            self.foxyRunFrameShift = 0
            if not self.leftDoorBtnClicked:
                self.setGameEndWithReason('hoxy')
                return True
            else:
                hoxyKnockAudio.play()
                self.hoxyPos = 'fail'
                self.hoxyStageLevel = 2
                return False

    def behave(self, name):
        tempPos, newPos = '', ''
        if name == 'zzaihong':
            if self.zannyPos == 'cam1a' or self.ziccaPos == 'cam1a' or self.zzaihongPos == self.cameraPos:
                return
            if self.zzaihongPos == 'door' and self.tryAttack(name):
                return
            newPos = random.choice(self.zzaihongLocMap[self.zzaihongPos])
            tempPos = self.zzaihongPos
            self.zzaihongPos = newPos
        elif name == 'zanny':
            if self.zannyPos == 'door' and self.tryAttack(name):
                return
            newPos = random.choice(self.zannyLocMap[self.zannyPos])
            tempPos = self.zannyPos
            self.zannyPos = newPos
        elif name == 'zicca':
            if self.ziccaPos == 'door' and self.tryAttack(name):
                return
            newPos = random.choice(self.ziccaLocMap[self.ziccaPos])
            tempPos = self.ziccaPos
            self.ziccaPos = newPos
        elif name == 'hoxy':
            if self.hoxyPos == 'running' and self.tryAttack(name):
                return

            if self.hoxyPos == 'fail' or self.hoxyStageLevel >= 3:
                newPos = self.hoxyLocMap[self.hoxyPos][0]
                tempPos = self.hoxyPos
                self.hoxyPos = newPos
                if newPos == 'running':
                    hoxyRunAudio.play()
                    self.foxyRunFrameShift = 1
                print(f"{name}: {tempPos} -> {newPos}")
            else:
                tempPos = 'cam1c'
                newPos = 'cam2a'
                print(f"hoxy: {self.hoxyStageLevel} -> {self.hoxyStageLevel + 1}")
                self.hoxyStageLevel += 1
        if name != 'hoxy':
            print(f"{name}: {tempPos} -> {newPos}")
        self.cameraStateChangeQueryMap[tempPos] = [self.zzaihongPos, self.zannyPos, self.ziccaPos, self.hoxyPos]
        self.cameraStateChangeQueryMap[newPos] = [self.zzaihongPos, self.zannyPos, self.ziccaPos, self.hoxyPos]

    def behaveCalculate(self):
        currentTime = time.time()
        
        for name, behaveTime in self.nextBehaveDict.items():
            if behaveTime < currentTime:
                self.nextBehaveDict[name] = currentTime + random.randint(3, 5)
                if name == 'hoxy' and self.hoxyPos == 'running':
                    self.behave("hoxy")
                elif self.getAnimatronicsLevel(name) >= random.randint(1, 20):
                    self.behave(name)

    def gameCalculate(self):
        self.gameTimeCurrent = time.time() - self.gameStartTime
        self.gameTimeText = f"{int(self.gameTimeCurrent / self.gameTimeInterval) + 1} AM"
        if self.gameTimeCurrent >= self.gameTimeInterval * 5:
            self.setGameEndWithReason('win')
        
        if self.gameTimeCurrent - self.batteryDecreaseTime >= self.batteryDecreaseUnitTime * (5 - min(4, len(self.batteryUsage))): # TODO: 배터리 감소 로직 고치기
            self.batteryDecreaseTime = self.gameTimeCurrent
            self.batteryLeft -= 1
        if self.batteryLeft <= 0:
            self.setGameEndWithReason('batteryout')
            return
        
        if self.foxyRunFrameShift > 0:
            self.foxyRunFrameShift += 1

        self.behaveCalculate()
