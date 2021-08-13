import pygame, pygame.freetype, sys

'''
   This is a tool to debug a DualShock4 (PS4) controller
   It will read and represent both analog sticks
'''

def readAnalogSticks():
   analogSticksMap = {"L_H": joystick.get_axis(0),
                      "L_V": joystick.get_axis(1),
                      "R_H": joystick.get_axis(2),
                      "R_V": joystick.get_axis(3)}
   return analogSticksMap

def drawAnalogStick(frame, center, analogValues, font):
   centerX, centerY = center
   analogX, analogY = analogValues
   # Draw stick representation
   pygame.draw.circle(frame, (255, 255, 255), (centerX, centerY), 60, 3)
   pygame.draw.circle(frame, (255, 0, 0), (int(centerX+30*analogX), int(centerY+30*analogY)), 30, 0)
   # Draw stick values
   font.render_to(frame, (centerX-70, centerY+75), "Horizontal: " + str(round(analogX, 2)), (255, 255, 255))
   font.render_to(frame, (centerX-70, centerY+105), "Vertical: " + str(round(analogY, 2)), (255, 255, 255))


# setup the pygame window
pygame.init()
pygame.font.init()
BACKGROUND = (20, 20, 20)
WIDTH   = 800
HEIGHT  = 400
TITLE_FONT = pygame.freetype.SysFont(name="ariblk", size=40)
FONT       = pygame.freetype.SysFont(name="ariblk", size=25)


window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
joystick_count = pygame.joystick.get_count()
print("There is " + str(joystick_count) + " joystick/s")
if joystick_count == 0:
   # if no joysticks, quit program safely
   print("Error, I did not find any joysticks")
   pygame.quit()
   sys.exit()
else:
   # initialise joystick
   joystick = pygame.joystick.Joystick(0)
   joystick.init()



newFrame = pygame.Surface((WIDTH, HEIGHT))
newFrame.fill(BACKGROUND)

while True:
   for event in pygame.event.get():
      # loop through events, if window shut down, quit program
      if event.type == pygame.QUIT:
         pygame.quit()
         sys.exit()

   # Build new frame
   newFrame = pygame.Surface((WIDTH, HEIGHT))
   newFrame.fill(BACKGROUND)

   # Draw title
   TITLE_FONT.render_to(newFrame, (int(WIDTH/2 - 180), 60), "Controller Debugger", (255, 255, 255))

   # Read analog stick values
   analogValues = readAnalogSticks()

   # Draw analog Sticks
   drawAnalogStick(newFrame, (int(WIDTH/2) - 200, int(HEIGHT/2)), (analogValues['L_H'], analogValues['L_V']), FONT)
   drawAnalogStick(newFrame, (int(WIDTH/2) + 200, int(HEIGHT/2)), (analogValues['R_H'], analogValues['R_V']), FONT)

   # Update frame
   window.blit(newFrame, (0, 0))
   pygame.display.flip()