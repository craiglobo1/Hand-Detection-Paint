from handDetector import HandDetector
import pygame as pg
import math
import cv2

def midpoint(p1, p2):
    return ((p1[0] + p2[0])//2, (p1[1] + p2[1])//2)

size = width, height  = 700, 700

canvasSize = canWidth, canHeight = 700, 575
canSurf = pg.Surface(canvasSize)
canSurf.fill((255,255,255))

toolbarSize = toolWidth, toolHeight = 700, height-canHeight

toolbarSurf = pg.Surface(toolbarSize)
toolbarSurf.fill((240,250,255))

trackSurf = pg.Surface(canvasSize, pg.SRCALPHA, 32)
# trackSurf = trackSurf.convert_alpha()

FPS = 60
pixel = 2


class Game:
    def __init__(self) -> None:
        pg.font.init()
        pg.init()

        self.capture = cv2.VideoCapture(0)
        self.detector = HandDetector()

        self.win = pg.display.set_mode(size)
        pg.display.set_caption("platformer")
        self.lastClicked = None
        self.posClicked = False
        # self.clock = pg.time.Clock()
    
    def new(self):

        return self.run()
    
    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            # self.dt = self.clock.tick(FPS)/1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        pos = pg.mouse.get_pos()
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False

        
        # if pg.mouse.get_pressed()[0] and pos[0] < canWidth and pos[1] < canHeight:
        #     self.lastClicked = self.posClicked
        #     self.posClicked = pos
        # else:
        #     self.posClicked = None

    def update(self):

        pg.display.update()
        # self.clock.tick(60)


    def draw(self):
        self.win.fill((255,255,255))


        colorSize = 20
        colors = [(0,0,0), (255,0,0), (0,255,0)]

        # for color in colors:
        #     pg.draw.rect(toolbarSurf)

        sucess, img = self.capture.read()
        handPos = self.detector.getPositions(img,0,False,canvasSize)

        mouseThreshold = 40
        
        if len(handPos) != 0:
            tmbPos = (handPos[4][0],handPos[4][1])
            idxPos = (handPos[8][0],handPos[8][1])
            cursorPos = midpoint(tmbPos,idxPos)
            if math.dist(tmbPos,idxPos) > mouseThreshold:
                width = 1
                self.posClicked =None
            else:
                width = 0
                cursorPos = midpoint(tmbPos,idxPos)
                self.lastClicked = self.posClicked
                self.posClicked = cursorPos


            pg.draw.circle(trackSurf, (200,0,0),tmbPos, 5, width)
            pg.draw.circle(trackSurf, (200,0,0), idxPos, 5, width)
            pg.draw.circle(trackSurf, (0,0,0),cursorPos,2)
            pg.draw.line(trackSurf, (200,200,200),tmbPos, idxPos, 1)
        
            # print(midpoint(tmbPos,idxPos),math.dist(tmbPos,idxPos))

            if math.dist(tmbPos,idxPos) < mouseThreshold and self.lastClicked and self.posClicked:
                pg.draw.line(canSurf, (0, 0, 0), self.lastClicked, self.posClicked, 2)

        self.win.blit(canSurf, (0,0))
        self.win.blit(trackSurf, (0,0))

        self.win.blit(toolbarSurf, (0, canHeight))
        trackSurf.fill((0, 0, 0, 0))
        


game = Game()
game.new()
pg.quit()

