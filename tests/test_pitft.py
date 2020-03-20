import os, pygame, time

def setSDLVariables():
    print("Setting SDL variables...")
    os.environ["SDL_FBDEV"] = "/dev/fb1"
    os.environ["SDL_VIDEODRIVER"] = driver
    print("...done") 

def printSDLVariables():
    print("Checking current env variables...")
    print("SDL_VIDEODRIVER = {0}".format(os.getenv("SDL_VIDEODRIVER")))
    print("SDL_FBDEV = {0}".format(os.getenv("SDL_FBDEV")))

def runHW5():
    print("Running HW5...")
    try:
        pygame.init()
    except pygame.error:
        print("Driver '{0}' failed!".format(driver))
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    print("Detected screen size: {0}".format(size))
    lcd = pygame.display.set_mode(size)
    lcd.fill((10,50,100))
    pygame.display.update()
    time.sleep(sleepTime)
    print("...done")

driver = 'fbcon'
sleepTime= 10

printSDLVariables()
setSDLVariables()
printSDLVariables()
runHW5()
