import random, pygame, sys, os, math
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
fpsClock = pygame.time.Clock()
scale = 3
DISPLAYSURF = pygame.display.set_mode((480 * scale, 270 * scale))
pygame.display.set_caption('Barons 2055: Tackle Baseball')
pygame.mouse.set_visible(False)

bg = pygame.image.load('bgb.png').convert()
bg = pygame.transform.scale(bg, (480 * scale, 270 * scale))

font = pygame.font.Font('bit1.ttf', 10 * scale)
font2 = pygame.font.Font('bit1.ttf', 24 * scale)

black = (0, 0, 0)
white = (255, 255, 255)
gold = (255, 205, 0)
two = 2 * scale
four = 4 * scale
eight = 8 * scale
ten = 10 * scale
oneSix = 16 * scale
threeTwo = 32 * scale
sixFour = 64 * scale
bottomEdge = 236 * scale
rightEdge = 454 * scale

gameMode = 'Season'
gameState = 'Beisbol'

outDisplay = False
displayTimer = 0

pos0 = [220 * scale, 120 * scale]
pos00 = [220 * scale, 200 * scale]
pos1 = [400 * scale, 110 * scale]
pos2 = [222 * scale, 22 * scale]
pos3 = [50 * scale, 110 * scale]
battingPosRH = [208 * scale, 226 * scale]
battingPosLH = [238 * scale, 226 * scale]


    
def ReadyPitch():
    player.safes = 0
    for mate in homeTeamList:
        mate.running = False
        mate.tackled = False
        mate.tackling = False
        mate.throwing = False
        mate.throwTimer = 0
        mate.accel = 3 * scale
        if mate.offense and mate.base < 0:
            if mate.righty:
                mate.pos[0] = battingPosRH[0]
                mate.pos[1] = battingPosRH[1]
            else:
                mate.pos[0] = battingPosLH[0]
                mate.pos[1] = battingPosLH[1]
        if mate.position == 0 and mate.offense == False:
            mate.pos[0] = pos0[0]
            mate.pos[1] = pos0[1]
        elif mate.position == 1 and mate.offense == False:
            mate.pos[0] = pos1[0]
            mate.pos[1] = pos1[1]
        elif mate.position == 2 and mate.offense == False:
            mate.pos[0] = pos2[0]
            mate.pos[1] = pos2[1]
        elif mate.position == 3 and mate.offense == False:
            mate.pos[0] = pos3[0]
            mate.pos[1] = pos3[1]
    i = 0
    while i <= 3:
        if homeTeamList[i].base >= 0 and player.homeBatter == i:
            player.homeBatter += 1
            homeTeamList[i].batting = False
        if player.homeBatter > 3:
            player.homeBatter = 0
            i = 0
        else:
            i += 1
    
    for mate in awayTeamList:
        mate.running = False
        mate.tackled = False
        mate.tackling = False
        mate.throwing = False
        mate.throwTimer = 0
        mate.pursuit = -1
        if mate.offense and mate.base < 0:
            if mate.righty:
                mate.pos[0] = battingPosRH[0]
                mate.pos[1] = battingPosRH[1]
            else:
                mate.pos[0] = battingPosLH[0]
                mate.pos[1] = battingPosLH[1]
        if mate.position == 0 and mate.offense == False:
            mate.pos[0] = pos0[0]
            mate.pos[1] = pos0[1]
        elif mate.position == 1 and mate.offense == False:
            mate.pos[0] = pos1[0]
            mate.pos[1] = pos1[1]
        elif mate.position == 2 and mate.offense == False:
            mate.pos[0] = pos2[0]
            mate.pos[1] = pos2[1]
        elif mate.position == 3 and mate.offense == False:
            mate.pos[0] = pos3[0]
            mate.pos[1] = pos3[1]
    i = 0
    while i <= 3:
        if awayTeamList[i].base >= 0 and player.awayBatter == i:
            player.awayBatter += 1
            awayTeamList[i].batting = False
        if player.awayBatter > 3:
            player.awayBatter = 0
            i = 0
        else:
            i += 1
    ball.pitched = False
    ball.hit = False
    player.ballCon = 0
    player.previousOuts = player.outs
    if player.inning % 2 != 0:    
        ball.pos[0] = homeTeamList[0].pos[0] + four
        ball.pos[1] = homeTeamList[0].pos[1] + eight
        player.control = 0
    else:
        ball.pos[0] = awayTeamList[0].pos[0] + four
        ball.pos[1] = awayTeamList[0].pos[1] + eight
        player.control = player.homeBatter        
        
def out():
    player.outs += 1

def Tackling(oList, dList, self):
    for mate in oList:   ## player and AI tackling
        if mate.offense:
            if dList[self.ballCon].rect.colliderect(mate.rect) and not mate.safe and ball.passed == False and ball.pitched and ball.held and not dList[player.ballCon].tackled and not dList[player.ballCon].tackling and not mate.tackled and mate.base >= 0:
                dList[self.ballCon].tackling = True
                dList[self.ballCon].tackleLeader = True
                dList[self.ballCon].pos[0] = mate.pos[0] - four
                dList[self.ballCon].pos[1] = mate.pos[1]
                ball.pos[0] = dList[self.ballCon].pos[0] + eight
                ball.pos[1] = dList[self.ballCon].pos[1] + oneSix
                mate.tackling = True
                mate.accel = 0
            if mate.tackling:
                if not mate.tackleLeader:
                    dList[self.ballCon].pos[0] = mate.pos[0] - four
                    dList[self.ballCon].pos[1] = mate.pos[1]
                    if random.randint(1, 100) > 96:
                        mate.base = -1
                        mate.tackling = False
                        mate.tackled = True
                        mate.running = False
                        self.onBase -= 1
                        out()
                        mate.accel = 3 * scale
                        break
                    if random.randint(1, 100) > 98:
                        mate.tackleLeader = True
                        dList[player.ballCon].tackleLeader = False
                else:
                    dList[self.ballCon].pos[0] = mate.pos[0] + four
                    dList[self.ballCon].pos[1] = mate.pos[1]
                    if random.randint(1, 100) > 98:
                        mate.tackling = False
                        mate.tackleLeader = False
                        mate.accel = 3 * scale
                        dList[player.ballCon].tackling = False
                        dList[player.ballCon].tackled = True
                    elif random.randint(1, 100) > 98:
                        mate.tackleLeader = False
                        dList[player.ballCon].tackleLeader = True
def RepositionDefense(self, dest, position):    
    if player.inning % 2 != 0:
        if player.control != position:
            if self.pos[1] < dest[1] - ten:
                self.pos[1] += self.accel
                self.running = True
            elif self.pos[1] > dest[1] + ten:
                self.pos[1] -= self.accel
                self.running = True
            elif self.pos[0] < dest[0] - ten:
                self.pos[0] += self.accel
                self.running = True
            elif self.pos[0] > dest[0] + ten:
                self.pos[0] -= self.accel
                self.running = True
            else:
                self.running = False
            
    else:
        if player.aiControl != position:
            if self.pos[1] < dest[1] - ten:
                self.pos[1] += self.accel
                self.running = True
            elif self.pos[1] > dest[1] + ten:
                self.pos[1] -= self.accel
                self.running = True
            elif self.pos[0] < dest[0] - ten:
                self.pos[0] += self.accel
                self.running = True
            elif self.pos[0] > dest[0] + ten:
                self.pos[0] -= self.accel
                self.running = True
            else:
                self.running = False
class Player():
    def __init__(self):
        self.control = 0
        self.aiControl = 0
        self.ballCon = 0
        self.strikes = 0
        self.outs = 0
        self.previousOuts = 0
        self.runsAway = 0
        self.runsHome = 0
        self.inning = 1
        self.awayBatter = 0
        self.homeBatter = 0
        self.onBase = 0
        self.safes = 0
        self.offense = False

        self.rect = Rect(0, 0, threeTwo, threeTwo)
        self.base1Rect = Rect(424 * scale, 144 * scale, threeTwo, threeTwo)
        self.base2Rect = Rect(232 * scale, 68 * scale, threeTwo, threeTwo)
        self.base3Rect = Rect(44 * scale, 144 * scale, threeTwo, threeTwo)
        self.base4Rect = Rect(232 * scale, 244 * scale, threeTwo, threeTwo)
    def update(self):
        self.rect = Rect(homeTeamList[self.control].pos[0] + eight, homeTeamList[self.control].pos[1] + four, oneSix, 24 * scale)
        if self.inning % 2 == 0 and ball.held:
            self.aiControl = self.ballCon
        Tackling(homeTeamList, awayTeamList, self)
        Tackling(awayTeamList, homeTeamList, self)
        for mate in homeTeamList:  ## player movement
            if self.control == mate.position and ball.pitched and not mate.tackling and not mate.throwing and not mate.batting and not mate.tackled and not mate.safe:
                if mate.base != -1 or not mate.offense:
                    if pressed[K_UP] and mate.pos[1] > -four:
                        mate.pos[1] -= mate.accel
                    if pressed[K_DOWN] and mate.pos[1] < bottomEdge:
                        mate.pos[1] += mate.accel
                    if pressed[K_LEFT]:
                        if mate.pos[0] > -four:
                            mate.pos[0] -= mate.accel
                        if mate.left == False:
                            mate.image = pygame.transform.flip(mate.image, 1, 0)
                            mate.left = True
                    if pressed[K_RIGHT]:
                        if mate.pos[0] < rightEdge:
                            mate.pos[0] += mate.accel
                        if mate.left:
                            mate.image = pygame.transform.flip(mate.image, 1, 0)
                            mate.left = False
                    if pressed[K_UP] or pressed[K_DOWN] or pressed[K_LEFT] or pressed[K_RIGHT]:
                        mate.running = True
                    else:
                        mate.running = False
                        mate.runTimer = 0
            elif not ball.pitched and self.control == mate.position:
                if mate.batting:
                    if pressed[K_RIGHT] and mate.pos[0] < 246 * scale:
                        mate.pos[0] += mate.accel / 2
                    if pressed[K_LEFT] and mate.pos[0] > 190 * scale:
                        mate.pos[0] -= mate.accel / 2
                else:
                    if pressed[K_RIGHT] and mate.pos[0] < 246 * scale:
                        mate.running = True
                        mate.pos[0] += mate.accel / 2
                    elif pressed[K_LEFT] and mate.pos[0] > 202 * scale:
                        mate.running = True
                        mate.pos[0] -= mate.accel / 2
                    else:
                        mate.running = False
                        mate.runTimer = 0



class Teammate():
    def __init__(self, position, team, name, righty):
        self.meterImage = pygame.image.load('health.png').convert_alpha()
        self.meterImage = pygame.transform.scale(self.meterImage, (oneSix, oneSix))
        self.meterPos = [0, 0]
        self.pos = [0, 0]
        self.position = position
        self.name = name
        self.image = pygame.image.load(str(name) + '.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (384 * scale, threeTwo))
        self.righty = righty
        self.bat = Bat('Wooden bat', self.righty)
        if team == 'moose':
            self.team = 1
            self.offense = False
            if position == 0:
                self.pos[0] = pos0[0]
                self.pos[1] = pos0[1]
            elif position == 1:
                self.pos[0] = pos1[0]
                self.pos[1] = pos1[1]
            elif position == 2:
                self.pos[0] = pos2[0]
                self.pos[1] = pos2[1]
            elif position == 3:
                self.pos[0] = pos3[0]
                self.pos[1] = pos3[1]
        if team == 'hobo':
            self.team = 2
            self.offense = True
            if self.righty:
                self.pos[0] = battingPosRH[0]
                self.pos[1] = battingPosRH[1]
            else:
                self.pos[0] = battingPosLH[0]
                self.pos[1] = battingPosLH[1]
                
        self.speed = [0, 0]
        self.accel = 3 * scale
        self.frame = 0
        self.angle = -70
        self.left = True
        
        ##defense
        self.dive = False
        self.diveTimer = 0
        self.tackling = False
        self.tackleTimer = 0
        self.tackleLeader = False
        self.tackled = False
        self.catching = False
        self.catchTimer = 0
        
        self.throwing = False
        self.throwTimer = 0
        self.meterUp = True
        self.running = False
        self.runTimer = 0
        self.pursuit = -1
        self.target = 0

        ##offense
        self.batting = False
        if position == 0 and self.offense:
            self.batting = True
        self.swinging = False
        self.tackled = False
        self.base = -1
        self.safe = False


        self.rect = Rect(self.pos[0], self.pos[1], threeTwo, threeTwo)
        
    def update(self):
        self.rect = Rect(self.pos[0] + eight, self.pos[1] + four, oneSix, 24 * scale)
        if self.offense:  ##Offense
            if player.inning % 2 != 0:
                if self.running == False and self.base == -1 and self.position == player.awayBatter and ball.hit == False:
                    self.batting = True
                    self.bat.update()
            else:
                if self.running == False and self.base == -1 and self.position == player.homeBatter and ball.hit == False:
                    self.batting = True
                    self.bat.update()
                

            if self.batting:            ## Batting
                if ball.pos[1] > 210 * scale and self.team == 2:
                    self.bat.swinging = True
                if ball.hit:
                    self.running = True
                    player.strikes = 0
                    self.base = 0
                    if player.inning % 2 != 0:
                        player.awayBatter += 1
                        if player.awayBatter > 3:
                            player.awayBatter = 0
                    else:
                        player.homeBatter += 1
                        if player.homeBatter > 3:
                            player.homeBatter = 0
                    self.batting = False
                    
            if self.running and ball.hit and not self.safe and not self.tackling:
                if player.control != self.position or self.team == 2:       ## AI baserunning
                    if self.base == 0:
                        self.pos[0] += math.sin(math.radians(self.angle)) * -self.accel
                        self.pos[1] += math.cos(math.radians(self.angle)) * -self.accel
                        if self.pos[0] > 425 * scale:
                            self.running = False
                            self.safe = True
                            player.safes += 1
                            self.base = 1
                            self.pos[0] = player.base1Rect[0] - eight
                            self.pos[1] = player.base1Rect[1] - (24 * scale)
                    elif self.base == 1:
                        self.pos[0] -= math.sin(math.radians(self.angle)) * -self.accel
                        self.pos[1] += math.cos(math.radians(self.angle)) * -self.accel
                        if self.pos[1] < 50 * scale:
                            self.running = False
                            self.safe = True
                            player.safes += 1
                            self.base = 2
                            self.pos[0] = player.base2Rect[0] - eight
                            self.pos[1] = player.base2Rect[1] - (24 * scale)
                    elif self.base == 2:
                        self.pos[0] -= math.sin(math.radians(self.angle)) * -self.accel
                        self.pos[1] -= math.cos(math.radians(self.angle)) * -self.accel
                        if self.pos[0] < 24 * scale:
                            self.running = False
                            self.safe = True
                            player.safes += 1
                            self.base = 3
                            self.pos[0] = player.base3Rect[0] - eight
                            self.pos[1] = player.base3Rect[1] - (24 * scale)
                    elif self.base == 3:
                        self.pos[0] += math.sin(math.radians(self.angle)) * -self.accel
                        self.pos[1] -= math.cos(math.radians(self.angle)) * -self.accel
                        if self.pos[1] > 200 * scale:
                            if self.team == 2:
                                player.runsAway += 1
                            else:
                                player.runsHome += 1
                            player.onBase -= 1
                            self.running = False
                            self.base = -1
                            self.safe = False
                            if self.righty:
                                self.pos[0] = battingPosRH[0]
                                self.pos[1] = battingPosRH[1]
                            else:
                                self.pos[0] = battingPosLH[0]
                                self.pos[1] = battingPosLH[1]
            if player.control == self.position and player.inning % 2 == 0:  ## player baserunning
                if player.rect.colliderect(player.base1Rect) and self.base == 0:
                    self.running = False
                    self.safe = True
                    player.safes += 1
                    self.base = 1
                    self.pos[0] = player.base1Rect[0] - eight
                    self.pos[1] = player.base1Rect[1] - (24 * scale)
                if player.rect.colliderect(player.base2Rect) and self.base == 1:
                    self.running = False
                    self.safe = True
                    player.safes += 1
                    self.base = 2
                    self.pos[0] = player.base2Rect[0] - eight
                    self.pos[1] = player.base2Rect[1] - (24 * scale)
                if player.rect.colliderect(player.base3Rect) and self.base == 2:
                    self.running = False
                    self.safe = True
                    player.safes += 1
                    self.base = 3
                    self.pos[0] = player.base3Rect[0] - eight
                    self.pos[1] = player.base3Rect[1] - (24 * scale)
                if player.rect.colliderect(player.base4Rect) and self.base == 3:
                    self.running = False
                    self.base = -1
                    player.runsHome += 1
                    player.onBase -= 1
                    self.safe = False
                    if self.righty:
                        self.pos[0] = battingPosRH[0]
                        self.pos[1] = battingPosRH[1]
                    else:
                        self.pos[0] = battingPosLH[0]
                        self.pos[1] = battingPosLH[1]
                
        else:             ##Defense
            if self.dive:
                self.diveTimer += timePassed
            if self.diveTimer > 300:
                self.dive = False
                self.diveTimer = 0
            if ball.hit and not self.tackled:
                if self.position == 0:
                    RepositionDefense(self, pos00, self.position)
                if self.position == 1:
                    RepositionDefense(self, pos1, self.position)
                if self.position == 2:
                    RepositionDefense(self, pos2, self.position)
                if self.position == 3:
                    RepositionDefense(self, pos3, self.position)
                
            if self.team == 2 and player.aiControl == self.position: ## Defense AI
                if ball.pitched == False:
                    if self.throwing and random.randint(1, 100) > 90:
                        ball.accel = int(self.throwTimer * two / 24)
                        self.throwing = False
                        self.throwTimer = 0
                        self.meterUp = True
                        ball.pitched = True
                        ball.held = False
                        if ball.accel < four:
                            ball.accel = four
                    if random.randint(1, 100) > 97 and not self.throwing:
                        self.throwing = True
                if ball.hit and not ball.held and not ball.passed:
                    if ball.height == 0 or ball.pos[1] < self.pos[1]:
                        self.running = True             ## chasing ball
                        self.speed[0] = 3 * scale
                        self.speed[1] = 3 * scale
                        if ball.pos[0] > self.pos[0] and self.pos[0] < rightEdge:
                            self.pos[0] += self.speed[0]
                        elif ball.pos[0] < self.pos[0] and self.pos[0] > -four:
                            self.pos[0] -= self.speed[0]
                        if ball.pos[1] > self.pos[1] and self.pos[1] < bottomEdge:
                            self.pos[1] += self.speed[1]
                        elif ball.pos[1] < self.pos[1] and self.pos[1] > -four:
                            self.pos[1] -= self.speed[1]
                elif ball.hit and ball.held and not self.tackling and not self.tackled: ## choosing lead base runner
                    if not self.throwing:
                        self.running = True
                        self.speed[0] = 3 * scale
                        self.speed[1] = 3 * scale
                    for mate in homeTeamList:
                        if mate.base >= 0 and not mate.safe and self.pursuit == -1:
                            self.pursuit = mate.position
                        if self.pursuit >= 0:
                            if mate.base > homeTeamList[self.pursuit].base and not mate.safe:
                                if abs(self.pos[0] - homeTeamList[self.pursuit].pos[0]) > sixFour or abs(self.pos[1] - homeTeamList[self.pursuit].pos[1]) > sixFour:
                                    if mate.base == 1 and abs(player.base2Rect[0] - mate.pos[0]) > 100 * scale or abs(player.base2Rect[1] - mate.pos[1]) > 80 * scale:
                                        self.pursuit = mate.position
                                    elif mate.base == 2 and abs(player.base3Rect[0] - mate.pos[0]) > 100 * scale or abs(player.base3Rect[1] - mate.pos[1]) > 80 * scale:
                                        self.pursuit = mate.position
                                    elif mate.base == 3 and abs(player.base4Rect[0] - mate.pos[0]) > 100 * scale or abs(player.base4Rect[1] - mate.pos[1]) > 80 * scale:
                                        self.pursuit = mate.position
                    if abs(homeTeamList[self.pursuit].pos[0]  - self.pos[0]) > 150 * scale or abs(homeTeamList[self.pursuit].pos[1] - self.pos[1]) > 150 * scale and homeTeamList[self.pursuit].base + 1 != self.position:
                        if not self.throwing and not ball.passed:   #### throwing in front of runner
                            self.throwing = True    
                            self.running = False
                            self.runTimer = 0
                            self.speed = [0, 0]
                        if self.throwing:
                            if random.randint(1, 100) > 90:
                                ball.target = homeTeamList[self.pursuit].base + 1
                                if ball.target == self.position:
                                    ball.target += 1
                                if ball.target > 3:
                                    ball.target = 0
                                ball.accel = int(self.throwTimer * two / 24)
                                if ball.accel < four:
                                    ball.accel = four
                                ball.angle = math.degrees(math.atan2(ball.pos[0] - (awayTeamList[ball.target].pos[0] + eight), ball.pos[1] - (awayTeamList[ball.target].pos[1] + oneSix)))
                                ball.speed[0] = math.sin(math.radians(ball.angle)) * -ball.accel
                                ball.speed[1] = math.cos(math.radians(ball.angle)) * -ball.accel
                                self.throwing = False
                                self.throwTimer = 0
                                self.meterUp = True
                                ball.passed = True
                                ball.held = False
                                player.aiControl = ball.target
                    else:                           ### chasing runner
                        if homeTeamList[self.pursuit].pos[0] > self.pos[0] and self.pos[0] < rightEdge:
                            self.pos[0] += self.speed[0]
                        elif homeTeamList[self.pursuit].pos[0] < self.pos[0] and self.pos[0] > -four:
                            self.pos[0] -= self.speed[0]
                        if homeTeamList[self.pursuit].pos[1] > self.pos[1] and self.pos[1] < bottomEdge:
                            self.pos[1] += self.speed[1]
                        elif homeTeamList[self.pursuit].pos[1] < self.pos[1] and self.pos[1] > -four:
                            self.pos[1] -= self.speed[1]
                else:
                    self.speed[0] = 0
                    self.speed[1] = 0
                    self.running = False
                    self.runTimer = 0
                    
                
        if self.catching:  ## catching
            self.catchTimer += timePassed
            if self.righty:
                if not self.left:
                    self.left = True
                    self.image = pygame.transform.flip(self.image, 1, 0)
            if self.catchTimer > 100:
                self.catchTimer = 0
                self.catching = False
        if self.running:   ## running
            self.runTimer += timePassed
            if self.runTimer > 240:
                self.runTimer = 0
                
        if self.throwing:  ## throwing
            if not self.left:
                self.left = True
                self.image = pygame.transform.flip(self.image, 1, 0)
            if player.inning % 2 != 0:
                if pressed[K_DOWN] and player.ballCon != 0:
                    ball.target = 0
                if pressed[K_RIGHT] and player.ballCon != 1:
                    ball.target = 1
                if pressed[K_UP] and player.ballCon != 2:
                    ball.target = 2
                if pressed[K_LEFT] and player.ballCon != 3:
                    ball.target = 3
            if self.meterUp:
                self.throwTimer += timePassed
            else:
                self.throwTimer -= timePassed
            if self.throwTimer >= 0:
                self.meterImage = pygame.transform.scale(self.meterImage, (int(self.throwTimer * scale / 4 + 1), oneSix))
            if self.throwTimer > 160:
                self.meterUp = False
            if self.throwTimer < 0 and not self.meterUp:  ## throw at minimum speed if meter goes up
                if ball.pitched:                        ## and then all the way back down
                    if player.inning % 2 != 0:
                        if ball.target == self.position:
                            ball.target += 1
                        if ball.target > 3:
                            ball.target = 0
                        ball.angle = math.degrees(math.atan2(ball.pos[0] - (homeTeamList[ball.target].pos[0] + eight), ball.pos[1] - (homeTeamList[ball.target].pos[1] + oneSix)))
                    else:
                        ball.angle = math.degrees(math.atan2(ball.pos[0] - (awayTeamList[ball.target].pos[0] + eight), ball.pos[1] - (awayTeamList[ball.target].pos[1] + oneSix)))
                    ball.accel = four
                    ball.passed = True
                    ball.held = False
                    ball.speed[0] = math.sin(math.radians(ball.angle)) * -ball.accel
                    ball.speed[1] = math.cos(math.radians(ball.angle)) * -ball.accel
                    self.throwing = False
                    self.throwTimer = 0
                    self.meterUp = True
                else:
                    ball.pitched = True
                    ball.accel = four
                    ball.held = False
                    self.throwing = False
                    self.throwTimer = 0
                    self.meterUp = True
                
        if self.tackling:  ## tackling
            ball.held = True
            if not self.left:
                self.left = True
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.tackleTimer += timePassed
            if self.tackleTimer > 320:
                self.tackleTimer = 0

      


        if not self.tackling:
            if self.left:    ## frame selection if left
                if self.running and self.catching == False and self.throwing == False and self.dive == False:
                    if self.runTimer < 60:
                        self.frame = 1
                    elif self.runTimer >= 60 and self.runTimer < 120:
                        self.frame = 2
                    elif self.runTimer >= 120 and self.runTimer < 180:
                        self.frame = 3
                    elif self.runTimer >= 180:
                        self.frame = 4
                elif self.catching:
                    self.frame = 5
                elif self.throwing:
                    self.frame = 6
                elif self.dive or self.tackled:
                    self.frame = 7
                elif self.batting:
                    self.frame = 8
                else:
                    self.frame = 0

            else:       ## frame selection if right
                if self.running and self.catching == False and self.throwing == False and self.dive == False:
                    if self.runTimer < 60:
                        self.frame = 10
                    elif self.runTimer >= 60 and self.runTimer < 120:
                        self.frame = 9
                    elif self.runTimer >= 120 and self.runTimer < 180:
                        self.frame = 8
                    elif self.runTimer >= 180:
                        self.frame = 7
                elif self.catching:
                    self.frame = 6
                elif self.throwing:
                    self.frame = 5
                elif self.dive or self.tackled:
                    self.frame = 4
                elif self.batting:
                    self.frame = 3
                else:
                    self.frame = 11
        
        elif self.tackling:    ## tackle frames
            if self.tackleLeader:
                if self.tackleTimer < 80:
                    self.frame = 8
                elif self.tackleTimer >= 80 and self.tackleTimer < 160:
                    self.frame = 9
                elif self.tackleTimer >= 160 and self.tackleTimer < 240:
                    self.frame = 10
                elif self.tackleTimer >= 240:
                    self.frame = 9
            else:
                if self.tackleTimer < 80:
                    self.frame = 1
                elif self.tackleTimer >= 80 and self.tackleTimer < 160:
                    self.frame = 2
                elif self.tackleTimer >= 160 and self.tackleTimer < 240:
                    self.frame = 3
                elif self.tackleTimer >= 240:
                    self.frame = 4

            ###### draw
        if self.offense == False or self.batting == True or self.base >= 0:
            DISPLAYSURF.blit(self.image, self.pos, (self.frame * threeTwo, 0, threeTwo, threeTwo))
        elif self.tackled and self.pos != battingPosRH and self.pos != battingPosLH:
            DISPLAYSURF.blit(self.image, self.pos, (self.frame * threeTwo, 0, threeTwo, threeTwo))
        if self.throwing:
            DISPLAYSURF.blit(self.meterImage, [self.pos[0], self.pos[1] + threeTwo])
       

class Bat():
    def __init__(self, bat, righty):
        self.righty = righty
        if self.righty:
            self.pos = [232 * scale, 246 * scale]
        else:
            self.pos = [246 * scale, 246 * scale]
        self.swinging = False
        self.swingTimer = 0
        self.rotation = 0
        if bat == 'Wooden bat':
            self.bat = 'Wooden bat'
            self.image = pygame.image.load('bat1.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.image.get_width() / 4 * scale, self.image.get_height() /  4 * scale))
            if not self.righty:
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.power = 2
        if bat == 'Stick':
            self.bat = 'Stick'
            self.image = pygame.image.load('bat1.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.image.get_width() / 4 * scale, self.image.get_height() /  4 * scale))
            if not self.righty:
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.power = 1
            

    def update(self):
        self.rotated = pygame.transform.rotate(self.image, self.rotation)
        self.pos1 = (self.pos[0] - self.rotated.get_rect().width/2, self.pos[1] - self.rotated.get_rect().height/2)
        
        if player.inning % 2 != 0:
            if awayTeamList[player.awayBatter].righty:
                self.pos[0] = awayTeamList[player.awayBatter].pos[0] + + 24 * scale
            else:
                self.pos[0] = awayTeamList[player.awayBatter].pos[0] + + eight
        else:
            if homeTeamList[player.homeBatter].righty:
                self.pos[0] = homeTeamList[player.homeBatter].pos[0] + + 24 * scale
            else:
                self.pos[0] = homeTeamList[player.homeBatter].pos[0] + + eight
        if self.swinging:
            self.swingTimer += timePassed
        self.rotation = self.swingTimer
        if self.swingTimer > 150:
            self.swingTimer = 0
            self.swinging = False
            
        
        DISPLAYSURF.blit(self.rotated, self.pos1)
        
        
class Ball():
    def __init__(self):
        self.image = pygame.image.load('16ball.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (48 * scale, 6 * scale))
        self.imageAir = pygame.image.load('softball.png').convert_alpha()
        self.imageAir = pygame.transform.scale(self.imageAir, (oneSix, oneSix))
        self.pos = [0, 0]
        self.speed = [0, 10 * scale]
        self.accel = two
        self.frame = 0
        self.defaultSpeed = 10 * scale
        self.angle = 0
        self.pitched = False
        self.hit = False
        self.passed = False
        self.held = True
        self.target = 1
        self.flightTimer = 0
        self.height = 0
    def update(self):
        self.rect = Rect(self.pos[0], self.pos[1], 25, 25)
        if self.held == False:
            self.flightTimer += timePassed
            if self.flightTimer > 240:
                self.flightTimer = 0
        if self.pitched == False:
            if player.inning % 2 != 0:
                self.pos[0] = homeTeamList[0].pos[0] + eight
                self.pos[1] = homeTeamList[0].pos[1] + oneSix
            else:
                self.pos[0] = awayTeamList[0].pos[0] + eight
                self.pos[1] = awayTeamList[0].pos[1] + oneSix
            self.held = True
        else: ##after pitch
            if self.hit == False:
                self.pos[1] += self.accel
                if self.pos[1] > 240 * scale and player.inning % 2 != 0: ## AI hitting
                    if random.randint(1, 2) < 2:
                        player.strikes += 1
                        self.pitched = False
                        self.pos = [homeTeamList[0].pos[0] + four, homeTeamList[0].pos[1] + eight]
                    else:
                        self.hit = True
                        self.angle = random.randint(-65, 65)
                        player.onBase += 1
                        if self.angle < -30:
                            player.control = 1
                        elif self.angle >= -30 and self.angle < 30:
                            player.control = 2
                        elif self.angle >= 30:
                            player.control = 3
                        if random.randint(1, 2) > 1:
                            self.height = 30
                        for mate in awayTeamList:
                            if mate.base >= 0:
                                mate.running = True
                                mate.safe = False
                elif player.inning % 2 == 0:  ## Player strikes
                    if self.pos[1] > 260 * scale:
                        player.strikes += 1
                        self.pitched = False
                        self.pos = [awayTeamList[0].pos[0] + four, awayTeamList[0].pos[1] + eight]
            else: ##after hit
                if self.held:
                    if player.inning % 2 != 0:
                        self.pos[0] = homeTeamList[player.ballCon].pos[0] + eight
                        self.pos[1] = homeTeamList[player.ballCon].pos[1] + oneSix
                    else:
                        self.pos[0] = awayTeamList[player.ballCon].pos[0] + eight
                        self.pos[1] = awayTeamList[player.ballCon].pos[1] + oneSix
                if self.height > 0:
                    self.height -= 1
                if self.pos[1] > oneSix and self.pos[0] > oneSix and self.pos[0] < 466 * scale and not self.passed and not self.held:
                    self.pos[1] += math.cos(math.radians(self.angle)) * (-10 * scale)
                    self.pos[0] += math.sin(math.radians(self.angle)) * (-10 * scale)
                for mate in homeTeamList:  ## picking up and catching ball
                    if mate.offense == False:
                        if self.rect.colliderect(mate.rect) and not self.passed and not self.held and self.height == 0:
                            player.control = mate.position
                            player.ballCon = mate.position
                            self.passed = False
                            self.held = True
                            break
                        elif self.rect.colliderect(mate.rect) and self.passed and mate.position != player.control:
                            player.control = mate.position
                            player.ballCon = mate.position
                            mate.catching = True
                            self.passed = False
                            self.held = True
                            break
                for mate in awayTeamList:
                    if mate.offense == False:
                        if self.rect.colliderect(mate.rect) and not self.passed and not self.held and self.height == 0:
                            player.ballCon = mate.position
                            player.aiControl = mate.position
                            self.passed = False
                            self.held = True
                            break
                        elif self.rect.colliderect(mate.rect) and self.passed and mate.position != player.ballCon:
                            player.ballCon = mate.position
                            player.aiControl = mate.position
                            mate.catching = True
                            self.passed = False
                            self.held = True
                            break
                if self.passed:
                    self.pos[0] += self.speed[0]
                    self.pos[1] += self.speed[1]
                    if self.pos[0] < 20 or self.pos[0] > 460 * scale or self.pos[1] < 20 or self.pos[1] > 240 * scale:
                        self.passed = False
                        self.speed = [0, 0]
                
        if self.flightTimer < 30:
            self.frame = 0
        elif self.flightTimer >= 30 and self.flightTimer < 60:
            self.frame = 1
        elif self.flightTimer >= 60 and self.flightTimer < 90:
            self.frame = 2
        elif self.flightTimer >= 90 and self.flightTimer < 120:
            self.frame = 3
        elif self.flightTimer >= 120 and self.flightTimer < 150:
            self.frame = 4
        elif self.flightTimer >= 150 and self.flightTimer < 180:
            self.frame =5
        elif self.flightTimer >= 180 and self.flightTimer < 210:
            self.frame = 6
        elif self.flightTimer >= 210:
            self.frame = 7
        if self.height == 0:
            DISPLAYSURF.blit(self.image, self.pos, (self.frame * (6 * scale), 0, 6 * scale, 6 * scale))
        else:
            DISPLAYSURF.blit(self.imageAir, self.pos)

player = Player()
homeTeamList = []
homeTeamList.append(Teammate(0, 'moose', 'robot', True))
homeTeamList.append(Teammate(1, 'moose', 'robot2', True))
homeTeamList.append(Teammate(2, 'moose', 'robot3', True))
homeTeamList.append(Teammate(3, 'moose', 'robot4', True))
awayTeamList = []
awayTeamList.append(Teammate(0, 'hobo', 'babyman', False))
awayTeamList.append(Teammate(1, 'hobo', 'babybrown', True))
awayTeamList.append(Teammate(2, 'hobo', 'bear', True))
awayTeamList.append(Teammate(3, 'hobo', 'peter', True))
ball = Ball()
while True: # main game loop
    pressed = pygame.key.get_pressed()
    timePassed = fpsClock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key in [K_ESCAPE]:
                pygame.quit()
                sys.exit()
            if event.key in [K_SPACE] and player.inning % 2 != 0:
                if ball.pitched == False:
                    if homeTeamList[player.control].throwing:
                        ball.accel = int(homeTeamList[player.control].throwTimer * two / 24)
                        if ball.speed[1] < four:
                            ball.speed[1] = four
                        homeTeamList[player.control].throwing = False
                        homeTeamList[player.control].throwTimer = 0
                        homeTeamList[player.control].meterUp = True
                        ball.pitched = True
                        ball.held = False
                    else:
                        homeTeamList[player.control].throwing = True
                elif ball.passed == False and ball.held:
                    if homeTeamList[player.control].throwing:
                        ball.accel = int(homeTeamList[player.control].throwTimer * two / 24)
                        if ball.accel < four:
                            ball.accel = four
                        homeTeamList[player.control].throwing = False
                        homeTeamList[player.control].throwTimer = 0
                        homeTeamList[player.control].meterUp = True
                        ball.passed = True
                        ball.held = False
                        ball.angle = math.degrees(math.atan2(ball.pos[0] - (homeTeamList[ball.target].pos[0] + eight), ball.pos[1] - (homeTeamList[ball.target].pos[1] + oneSix)))
                        ball.speed[0] = math.sin(math.radians(ball.angle)) * -ball.accel
                        ball.speed[1] = math.cos(math.radians(ball.angle)) * -ball.accel
                    else:
                        homeTeamList[player.control].throwing = True
                        ball.target = player.control + 1
                        if ball.target > 3:
                            ball.target = 0
            
            if event.key in [K_SPACE] and player.inning % 2 == 0:
                if ball.pitched and not ball.hit:
                    homeTeamList[player.homeBatter].swinging = True
                    homeTeamList[player.homeBatter].bat.swinging = True
                    if ball.pos[1] >= 210 * scale and random.randint(1, 100) > 20:
                        ball.hit = True
                        if ball.pos[1] < 220 * scale:
                            if homeTeamList[player.homeBatter].righty:
                                ball.angle = random.randint(30, 65)
                            else:
                                ball.angle = random.randint(-65, -30)
                        elif ball.pos[1] >= 220 * scale and ball.pos[1] < 230 * scale:
                            if homeTeamList[player.homeBatter].righty:
                                ball.angle = random.randint(10, 30)
                            else:
                                ball.angle = random.randint(-30, -10)
                        elif ball.pos[1] >= 230 * scale and ball.pos[1] < 240 * scale:
                            ball.angle = random.randint(-10, 10)
                        elif ball.pos[1] >= 240 * scale and ball.pos[1] < 250 * scale:
                            if homeTeamList[player.homeBatter].righty:
                                ball.angle = random.randint(-30, -10)
                            else:
                                ball.angle = random.randint(10, 30)
                        elif ball.pos[1] >= 250 * scale:
                            if homeTeamList[player.homeBatter].righty:
                                ball.angle = random.randint(-65, -30)
                            else:
                                ball.angle = random.randint(30, 65)
                        ball.speed[0] = math.sin(math.radians(ball.angle)) * -ball.accel
                        ball.speed[1] = math.cos(math.radians(ball.angle)) * -ball.accel
                        player.onBase += 1
                        if random.randint(1, 8) > 6:
                            ball.height = 30
                        if ball.angle < -30:
                            player.aiControl = 1
                        elif ball.angle >= -30 and ball.angle < 30:
                            player.aiControl = 2
                        elif ball.angle >= 30:
                            player.aiControl = 3
                        for mate in homeTeamList:
                            if mate.base >= 0:
                                mate.running = True
                                mate.safe = False
                            if mate.base > homeTeamList[player.control].base:
                                player.control = mate.position
                        
            if event.key in [K_z]:
                if homeTeamList[player.control].dive == False:
                    homeTeamList[player.control].dive = True
                            
                        
    
                
    if player.strikes >= 3:
        player.strikes = 0
        player.outs += 1
        if player.inning % 2 != 0:
            awayTeamList[player.awayBatter].batting = False
            player.awayBatter += 1
            if player.awayBatter > 3:
                player.awayBatter = 0
        else:
            homeTeamList[player.homeBatter].batting = False
            player.homeBatter += 1
            if player.homeBatter > 3:
                player.homeBatter = 0
        outDisplay = True
        ReadyPitch()
    
    if player.previousOuts < player.outs:
        outDisplay = True
        player.previousOuts = player.outs
    elif player.safes >= player.onBase and ball.pitched and ball.hit and not outDisplay:  ## end of play
        ReadyPitch()
    elif player.outs >= 3:
        player.ballCon = 0
        player.onBase = 0
        player.safes = 0
        player.outs = 0
        player.strikes = 0
        player.inning += 1
        for mate in homeTeamList:
            mate.base = -1
            mate.safe = False
            if mate.offense:
                mate.offense = False
                mate.batting = False
                player.control = 0
            else:
                mate.offense = True
                player.control = player.homeBatter
        for mate in awayTeamList:
            mate.base = -1
            mate.safe = False
            if mate.offense:
                mate.offense = False
                mate.batting = False
            else:
                mate.offense = True
        ReadyPitch()
    if outDisplay:
        displayTimer += timePassed
        if displayTimer > 300:
            outDisplay = False
            displayTimer = 0
            if player.inning % 2 != 0:
                for mate in awayTeamList:
                    if mate.base == -1:
                        if mate.righty:
                            mate.pos[0] = battingPosRH[0]
                            mate.pos[1] = battingPosRH[1]
                        else:
                            mate.pos[0] = battingPosLH[0]
                            mate.pos[1] = battingPosLH[1]
            else:
                for mate in homeTeamList:
                    if mate.base == -1:
                        if mate.righty:
                            mate.pos[0] = battingPosRH[0]
                            mate.pos[1] = battingPosRH[1]
                        else:
                            mate.pos[0] = battingPosLH[0]
                            mate.pos[1] = battingPosLH[1]
                    


    DISPLAYSURF.blit(bg, [0, 0])
    player.update()
    for mate in homeTeamList:
        if not mate.tackleLeader:
            mate.update()
    for mate in awayTeamList:
        mate.update()
    for mate in homeTeamList:
        if mate.tackleLeader:
            mate.update()
    ball.update()
    
    runText = font.render(str(player.runsAway), 1, white)
    runText1 = font.render(str(player.runsHome), 1, white)
    strikeText = font.render('Strikes: ' + str(player.strikes), 1, white)
    outText = font.render('Outs: ' + str(player.outs), 1, white)
    outT = font2.render('OUT', 1, white)
    DISPLAYSURF.blit(runText, [0, 5 * scale])
    DISPLAYSURF.blit(runText1, [15 * scale, 5 * scale])
    DISPLAYSURF.blit(strikeText, [0, 15 * scale])
    DISPLAYSURF.blit(outText, [98 * scale, 15 * scale])
    if outDisplay:
        DISPLAYSURF.blit(outT, [200 * scale, 100 * scale])
    
    pygame.display.flip()
    
    fpsClock.tick(60)
