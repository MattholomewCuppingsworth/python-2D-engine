import pygame, random, entityComponent, gameUtils

#Window Size constant
size = (640, 480)


def main():
	pygame.init()
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption("Movey Abouty time")
	clock = pygame.time.Clock()
	done = False

	char_sprites = gameUtils.SpriteSheet("./sprites.png")

	blueHairedBack = char_sprites.load_strip((0,128,24,32), 3, -1)
	blueHairedRight = char_sprites.load_strip((0,160,24,32), 3, -1)
	blueHairedForward = char_sprites.load_strip((0,192,24,32), 3, -1)
	blueHairedLeft = char_sprites.load_strip((0,224,24,32), 3, -1)

	gogglesBack = char_sprites.load_strip((144,0,24,32), 3, -1)
	gogglesRight = char_sprites.load_strip((144,32,24,32), 3, -1)
	gogglesForward = char_sprites.load_strip((144,64,24,32), 3, -1)
	gogglesLeft = char_sprites.load_strip((144,96,24,32), 3, -1)
	
	forestMap = entityComponent.Map("./CTForestBG.png", (0,0))

	frames = 5
	frameIter = gameUtils.FrameIter(gogglesBack, True, frames)

	mainDude = entityComponent.Character(frameIter, entityComponent.Position(size[0]/2,size[1]/2), entityComponent.Movement(0,0, 2))

	theCamera = entityComponent.Camera(mainDude.position, size)

	while(not done):	#game loop



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
					mainDude.movement.dy =-1*(mainDude.movement.movespeed)
					mainDude.moving = True
				elif(keys[pygame.K_DOWN]):
					mainDude.movement.dy = mainDude.movement.movespeed
					mainDude.moving = True
				elif(keys[pygame.K_LEFT]):
					mainDude.movement.dx = -1*(mainDude.movement.movespeed)
					mainDude.moving = True
				elif(keys[pygame.K_RIGHT]):
					mainDude.movement.dx = mainDude.movement.movespeed
					mainDude.moving = True
				#if(keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]):
				#	mainDude.movement.dx = 0
				#if(keys[pygame.K_UP] and keys[pygame.K_DOWN]):
				#	mainDude.movement.dy = 0
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
					mainDude.moving = False
#			elif event.type == pygame.MOUSEMOTION:
#				location = pygame.mouse.get_pos()
#				print location
#			elif event.type == pygame.MOUSEBUTTONDOWN:
#				print "whoa buddy, lay off"
#			elif event.type == pygame.MOUSEBUTTONUP:
#				print "thanks, geez. Stop it then."

		#	Run calculations to determine where objects move, what happens when objects collide, etc.
		mainDude.position.update(mainDude.movement.dx, mainDude.movement.dy)


		if(mainDude.movement.dx > 0): #Determine facing based on character's last direction.
			mainDude.frames.images = gogglesRight
		elif(mainDude.movement.dx < 0):
			mainDude.frames.images = gogglesLeft
		if(mainDude.movement.dy > 0):
			mainDude.frames.images = gogglesForward
		elif(mainDude.movement.dy < 0):
			mainDude.frames.images = gogglesBack

		theCamera.position = (mainDude.position.x, mainDude.position.y)

		#	Clear the screen
		screen.fill((0,0,0))

		#	Draw everything
		theCamera.drawWithinBounds(screen, forestMap, mainDude)
		print theCamera.position

		pygame.display.update()

		msElapsed = clock.tick(30) #advances frame, 30 FPS

if __name__ == '__main__' : main()