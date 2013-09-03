import pygame

#Components
class Position:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def update(self, dx, dy):
		self.x += dx
		self.y += dy

class Movement:
	def __init__(self, dx, dy, movespeed):
		self.dy = dy
		self.dx = dx
		self.movespeed = movespeed

class Graphic(pygame.sprite.Sprite):
	def __init__(self, width, height, image):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([width, height])
		self.image.blit(image, (0,0))

class Map:
	def __init__(self, background, position):
		self.background = pygame.image.load(background)
		self.position = (0,0)

#Entities
class Character:
	def __init__(self, frames, position, movement):
		self.frames = frames
		self.position = position
		self.movement = movement
		self.moving = False

class Camera:
	def __init__(self, center, (width, height)):
		self.center = center
		self.size = (width, height)
	def drawWithinBounds(self, surface, map, pc, npcs = []):
		surface.blit(map.background, map.position)
		if pc.moving: #Only animate the character if the character is actually moving. Otherwise, stay in standing frame
			surface.blit(pc.frames.next(), (pc.position.x, pc.position.y))
		else:
			surface.blit(pc.frames.images[0], (pc.position.x, pc.position.y))
		for npc in npcs:
			surface.blit(npc.frames.next(), (npc.position.x, npc.position.y))