import pygame, os

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
    def __init__(self, tileset, layout):
        # tiles = dict in format {'name' : Tile Object}, all tiles used on this map
        # layout = 2D list, each value is a tile name as listed in self.tiles
        self.tileset = tileset
        self.layout = layout
        self.tiles = [[self.tileset.mappings[col] for col in row] for row in self.layout]
        
    def drawMap(self, displaySurf):
        # appending each tile to the 2d array and blitting them
        # displaySurf = pygame Surface to blit tiles onto
        for col_idx, col in enumerate(self.tiles, start=0):
            for row_idx, tile in enumerate(col, start=0):
                # all tiles are 16x16 so x-y coords are index*16
                coords = (row_idx*16, col_idx*16)
                tile.drawTile(displaySurf, coords)
                
class Tileset:
    def __init__(self, **kwargs):
        self.mappings = {}
        for k, v in kwargs.iteritems():
            self.mappings.update({k: Tile(v['img'], v['collide'])})

class Tile:
    def __init__(self, img, collision):
        # img = file path to tile graphic (16x16 png)        
        # collision = boolean, true = impassible
        fullpath = os.path.abspath(os.path.join('./', "{img}.png".format(img=img)))
        self.img = pygame.image.load(fullpath)
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


'''
class Camera:
# Each map should have a camera object. Starts centered on main character
    # but should not extend beyond map bounds
    def __init__(self, center, (width, height)):
        self.center = center
        self.size = (width, height)
    def drawWithinBounds(self, surface, map, pc, npcs = []):
        surface.blit(map.background, map.position)
        if pc.movement.up or pc.movement.down or pc.movement.left or pc.movement.right: #Only animate the character if the character is actually moving. Otherwise, stay in standing frame
            surface.blit(pc.frames.next(), (pc.position.x, pc.position.y))
        else:
            surface.blit(pc.frames.images[0], (pc.position.x, pc.position.y))
        for npc in npcs:
            surface.blit(npc.frames.next(), (npc.position.x, npc.position.y))
'''