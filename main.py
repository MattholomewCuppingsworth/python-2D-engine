import pygame, random

#Window Size constant
size = (800, 600)

class Position:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def update(self, dx, dy):
		self.x += dx
		self.y += dy

class Movement:
	def __init__(self, dx, dy):
		self.dy = dy
		self.dx = dx

class Graphic(pygame.sprite.Sprite):
	def __init__(self, width, height, image):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([width, height])
		self.image.blit(image, (0,0))

class Character:
	def __init__(self, graphic, position, movement):
		self.graphic = graphic
		self.position = position
		self.movement = movement

class SpriteSheet(object):
	def __init__(self, filename):
		try:
			self.sheet = pygame.image.load(filename).convert()
		except pygame.error, message:
			print 'Unable to load spritesheet image:', filename
			raise SystemExit, message
	# Load a specific image from a specific rectangle
	def image_at(self, rectangle, colorkey = None):
		"Loads image from x,y,x+offset,y+offset"
		rect = pygame.Rect(rectangle)
		image = pygame.Surface(rect.size).convert()
		image.blit(self.sheet, (0, 0), rect)
		if colorkey is not None:
			if colorkey is -1:
				colorkey = image.get_at((0,0))
				image.set_colorkey(colorkey, pygame.RLEACCEL)
				return image
	# Load a whole bunch of images and return them as a list
	def images_at(self, rects, colorkey = None):
		"Loads multiple images, supply a list of coordinates" 
		return [self.image_at(rect, colorkey) for rect in rects]
	# Load a whole strip of images
	def load_strip(self, rect, image_count, colorkey = None):
		"Loads a strip of images and returns them as a list"
		tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
				for x in range(image_count)]
		return self.images_at(tups, colorkey)

def main():
	pygame.init()
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption("Whoa, this is a nice window, guy!")
	clock = pygame.time.Clock()
	done = False

	char_sprites = SpriteSheet("./sprites.png")

	blueHaired = char_sprites.image_at((0,192,24,224),-1)
	mainDude = Character(Graphic(24, 32, blueHaired), Position(0,0), Movement(0,0))

	while(not done):	

		#	For each event (keypress, mouse click, etc.):
		for event in pygame.event.get(): # User did something
			keys = pygame.key.get_pressed()
			#	Use a chain of if statements to run code to handle each event.
			if event.type == pygame.QUIT: # If user clicked close
				done = True # Flag that we are done so we exit this loop
			elif event.type == pygame.KEYDOWN: # 
				if(keys[pygame.K_ESCAPE]):
					print "We're outta here!"
					done = True
				if(keys[pygame.K_UP]):
					print "Move Up"
					mainDude.movement.dy = -2
				if(keys[pygame.K_DOWN]):
					print "Move Down"
					mainDude.movement.dy = 2
				if(keys[pygame.K_LEFT]):
					print "Move Left"
					mainDude.movement.dx = -2
				if(keys[pygame.K_RIGHT]):
					print "Move Right"
					mainDude.movement.dx = 2
			elif event.type == pygame.KEYUP:
				# Up or down is still pressed, stop left and right movement
				if (keys[pygame.K_DOWN] or keys[pygame.K_UP]):
					mainDude.movement.dx = 0
				# vica versa
				elif (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
					mainDude.movement.dy = 0
				# no keys are pressed, stop it all
				else:
					mainDude.movement.dx = 0
					mainDude.movement.dy = 0
			elif event.type == pygame.MOUSEMOTION:
				location = pygame.mouse.get_pos()
				print location
			elif event.type == pygame.MOUSEBUTTONDOWN:
				print "whoa buddy, lay off"
			elif event.type == pygame.MOUSEBUTTONUP:
				print "thanks, geez. Stop it then."

		#	Run calculations to determine where objects move, what happens when objects collide, etc.
		mainDude.position.update(mainDude.movement.dx, mainDude.movement.dy)

		#	Clear the screen
		screen.fill((1,1,1))

		#	Draw everything
		screen.blit(mainDude.graphic.image, (mainDude.position.x, mainDude.position.y))

		pygame.display.update()

		msElapsed = clock.tick(30) #advances frame, 30 FPS

if __name__ == '__main__' : main()