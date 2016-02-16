import pygame, os
from math import floor

#Components
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def update(self, dx, dy):
        self.x += dx
        self.y += dy

class Movement:
    def __init__(self, movespeed):
        self.up = False
        self.down = False
        self.left = False						
        self.right = False
        self.speed = movespeed

class Graphic(pygame.sprite.Sprite):
    def __init__(self, width, height, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.blit(image, (0,0))

class Map:
    def __init__(self, tileset, layout, displaySurf):
        # tileset = all tiles used on this map
        # layout = 2D list, each value is a tile name as listed in self.tiles
        # displaySurf = surface we draw map onto, usually the base screen surface
        self.tileset = tileset
        self.layout = layout
        self.displaySurf = displaySurf
        # 2D Array where we match each item in the layout with the associated tile
        self.tiles = [[self.tileset.mappings[col] for col in row] for row in self.layout]
        # Offset: added x+y coords to help draw map centered on screen, measured in tiles
        pxAcrossScreen = self.displaySurf.get_width()
        pxDownScreen = self.displaySurf.get_height()
        pxAcrossMap = len(self.tiles[0])*16
        pxDownMap = len(self.tiles)*16
        self.offsetX = int(floor(pxAcrossScreen/2) - floor(pxAcrossMap/2))
        self.offsetY = int(floor(pxDownScreen/2) - floor(pxDownMap/2))

    def drawMap(self):
        for col_idx, col in enumerate(self.tiles, start=0):
            for row_idx, tile in enumerate(col, start=0):
                # all tiles are 16x16 so x-y coords are index*16
                coords = (row_idx*16+self.offsetX, col_idx*16+self.offsetY)
                tile.drawTile(self.displaySurf, coords)
                
class Tileset:
    def __init__(self, **kwargs):
        self.mappings = {}
        for k, v in kwargs.iteritems():
            self.mappings.update({k: Tile(v['img'], v['collide'])})

class Tile:
    def __init__(self, img, collision):
        # img = file path to tile graphic (16x16 png)        
        # collision = boolean, true = impassible
        fullpath = os.path.abspath(os.path.join('./img/', "{img}.png".format(img=img)))
        self.img = pygame.image.load(fullpath).convert()
        self.collision = collision
    
    def drawTile(self, displaySurf, (x, y)):
        # displaySurf = the surface we are blitting tile onto
        displaySurf.blit(self.img, (x, y))
        
#Entities
class Character:
    def __init__(self, frames, position, movement):
        self.frames = frames
        self.position = position
        self.movement = movement
    
    def drawCharacter(self, displaySurf):
        if self.movement.up or self.movement.down or self.movement.left or self.movement.right:
            displaySurf.blit(self.frames.next(), (self.position.x, self.position.y))
        else:
            displaySurf.blit(self.frames.images[0], (self.position.x, self.position.y))
            