import pygame, csv, random, entityComponent, gameUtils

#Window Size constant
size = (640, 640)


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Walk about time")
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
    
    frames = 5
    frameIter = gameUtils.FrameIter(gogglesBack, True, frames)

    mainDude = entityComponent.Character(frameIter, entityComponent.Position(size[0]/2,size[1]/2), entityComponent.Movement(2))

    # Making the tileset
    tileset = entityComponent.Tileset(
        floor={'img':'purple-octagon-tile', 'collide':False},
        nwall={'img':'purple-wall-north', 'collide':True},
        swall={'img':'purple-wall-south', 'collide':True},
        ewall={'img':'purple-wall-east', 'collide':True},
        wwall={'img':'purple-wall-west', 'collide':True},
        newall={'img':'purple-wall-northeast-corner', 'collide':True},
        nwwall={'img':'purple-wall-northwest-corner', 'collide':True},
        sewall={'img':'purple-wall-southeast-corner', 'collide':True},
        swwall={'img':'purple-wall-southwest-corner', 'collide':True}
    )

    # First room layout
    layout = []
    with open('test-floorplan.csv', mode='rb') as floorplan:
        reader = csv.reader(floorplan,delimiter=',')
        for row in reader:
            layout.append(row)
    firstMap = entityComponent.Map(tileset, layout)

    # game loop
    while(not done):
        # For each event (keypress, mouse click, etc.):
        keys = pygame.key.get_pressed()
        keyPressed = False
        for event in pygame.event.get(): # User did something
            # Use a chain of if statements to run code to handle each event.
            if event.type == pygame.QUIT:
                print 'quittin' 
                done = True
            elif event.type == pygame.KEYDOWN: 
                keyPressed = True
                if(event.key == pygame.K_ESCAPE):
                    print 'quittin'
                    done = True
        if(keys[pygame.K_UP]):
            mainDude.position.y -= mainDude.movement.speed
            mainDude.frames.images = gogglesBack                    
        elif(keys[pygame.K_DOWN]):
            mainDude.position.y += mainDude.movement.speed
            mainDude.frames.images = gogglesForward                    
        elif(keys[pygame.K_LEFT]):
            mainDude.position.x -= mainDude.movement.speed
            mainDude.frames.images = gogglesLeft                    
        elif(keys[pygame.K_RIGHT]):
            mainDude.position.x += mainDude.movement.speed
            mainDude.frames.images = gogglesRight                    

        #	Clear the screen
        screen.fill((0,0,0))

        #	Draw everything
        firstMap.drawMap(screen)
        mainDude.drawCharacter(screen)
        pygame.display.update()

        msElapsed = clock.tick(30) #advances frame, 30 FPS

if __name__ == '__main__' : main()