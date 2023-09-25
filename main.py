# <----- PILOT ----->
#By James Li for Mr Seger final project

from tkinter import *
from math import *
from time import *
from random import *
from random import choices

root = Tk()
screen = Canvas(root, width=800, height=600, background="white")

#------------------------------------------->
def setInitialValues():
  #GLOBAL EVERYTHING, multiple globals to organize it a bit.
  global X_airplane, Y_airplane, time, AP_moveX, AP_moveY, AP_move, Ball_move, Baloon_move, Missile_move, Boost_spd, xMouse, yMouse, xSpeed, ySpeed, maxSpeed, AP, obedience, mouseAngle
  global Airplanefiles, angleOutput, airplaneDrawing, xAirplane, yAirplane, AirplaneImage
  global x,y,Missile_spawnx, Missile_spawny, Ball_spawnx, Ball_spawny, Baloon_spawnx, Baloon_spawny, MissileDrawing, BallDrawing, BaloonDrawing, obsList, MissileAngle, obsChoice, spawnTimer, Missilefiles, MissileImage, BallSpawn, BaloonSpawn, MissileSpawn, died
  global SkyGIF, BallPNG, BaloonPNG, HgwPNG, HomePNG, InstrucPNG, CrashPNG, WinPNG
  global HomeScreen, HgwScreen, InstrucScreen, WinScreen, CrashScreen, GameStart, breakloop
#ALL THE VARIABLES
  time = 0
  Boost_spd = 100
  AP_moveX = 1
  AP_moveY = -1
  xMouse=0
  yMouse=0
  xSpeed=0
  ySpeed=0
  mouseAngle=0
  maxSpeed=2
  AP = 0
  obedience = 0.05
  
  
  Ball_move = 7
  Missile_move = 10
  Baloon_move = 3

  X_airplane = 0
  Y_airplane = 200

  #PHOTO IMAGES
  SkyGIF = PhotoImage(file = "skys.gif") 
  BaloonPNG = PhotoImage(file = "BALOON.png")
  BallPNG = PhotoImage(file = "BALL.png")
  MissilePNG = PhotoImage(file = "Missiles/Missile1.png")

  HomePNG = PhotoImage(file = "HOME.png")
  InstrucPNG = PhotoImage(file = "INSTRUCTIONS.png")
  HgwPNG = PhotoImage(file = "HOW GAME WORKS.png")
  CrashPNG = PhotoImage(file = "CRASH.png")
  WinPNG = PhotoImage(file = "WIN.png")

  #add all images of airplanes to a list, for the rotation
  Airplanefiles=[]

  for i in range(1,72):
    Airplanefiles.append(PhotoImage (file = "Airplanes/airplane " + str(i) + ".png"))

  angleOutput = 0
  airplaneDrawing = 0
  AirplaneImage = Airplanefiles[1]
  print(X_airplane)

  #Variables for obstacles

  x = [100,200,300,400,500,600,700,800,900,1000]
  y=[100,200,300,400,500,600]
  Missile_spawnx = 0
  Missile_spawny = 0
  Ball_spawnx = 0
  Ball_spawny = 0
  Baloon_spawnx = 0
  Baloon_spawny = 0
  
  MissileDrawing = 0
  BallDrawing = 0
  BaloonDrawing=0
  MissileAngle = 0
  spawnTimer = 0
  BallSpawn = False
  BaloonSpawn = False
  MissileSpawn = False
#add all images of missiles to list, just like the airplane

  Missilefiles = []
  for i in range(1,38):
    Missilefiles.append(PhotoImage (file="Missiles/Missile" + str(i) + ".png"))
    
  MissileImage = Missilefiles[1]

  obsList = []
  obsChoice = []

  died = False
  breakloop = False

  #Values for HomeScreen/End Screen
  HomeScreen = True
  HgwScreen = False
  InstrucScreen = False
  WinScreen = False
  CrashScreen = False
  GameStart = False
  
#------------------------------------------->
def drawSky():
  #DRAWS THE SKY BACKGROUND
  global SkyIMG, SkyGIF, WinLine
  SkyIMG = screen.create_image(0,0, anchor=NW, image = SkyGIF)

  #LINE OF SAFETY
  screen.create_line(780,0,780,600, width = 3, fill='white')

  #Draws warning thing
  screen.create_rectangle(20,20,300,60, fill='red')
  screen.create_text(160,40, text = "Beware of Falling Objects!", font = "_monospace_" , fill='orange')
#------------------------------------------->
#This and all the "draws" below - to be called to draw the background that I need at certain times
def drawHome():
  global home
  home = screen.create_image(0,0,image = HomePNG, anchor = NW)
#------------------------------------------->
def drawHgw():
  global Hgw
  Hgw = screen.create_image(0,0,image = HgwPNG, anchor = NW)
#------------------------------------------->
def drawInstructions():
  global Instruction
  Instruction = screen.create_image(0,0, image = InstrucPNG, anchor = NW)
#------------------------------------------->
def drawCrash():
  global Crash
  screen.delete('all')
  Crash = screen.create_image(0,0, image = CrashPNG, anchor = NW)
#------------------------------------------->
def drawWin():
  global Win
  screen.delete('all')
  Win = screen.create_image(0,0, image = WinPNG, anchor = NW)
#------------------------------------------->
#So you can right click the end screen to return to the home screen
def EndScreen(event):
  global HomeScreen, CrashScreen, WinScreen, breakloop
  while CrashScreen == True:
    CrashScreen = False
    HomeScreen = True
    breakloop = True
    break
  while WinScreen == True:
    WinScreen = False
    HomeScreen = True
    breakloop = True
    break
  
#------------------------------------------->
#For TELEPORTATION. 
def KeyDownHandler( event ):
  global X_airplane, Y_airplane

  #Teleport
  if event.keysym == "e" or event.keysym == "E":
    minusX= randint(0,int(X_airplane))
    minusY = randint(0,int(Y_airplane))

    X_airplane = minusX
    Y_airplane = minusY

#-------------------------------------------> 
#Finds the MouseAngle, for Airplane rotation
def mouseMotionHandler (event):
  global xMouse, yMouse, mouseAngle

  xMouse = event.x
  yMouse = event.y

  mouseAngle = getAngle()
  printAngle()
  if GameStart == True:
    drawAirplane()
        
#------------------------------------------->
#This is the whole Home Screen. Uses where the Mouse is relative to the button locations, and selects the correct image to show when clicked. 
def mouseClickHandler(event):
  global Mousex, Mousey, HomeScreen, HgwScreen, InstrucScreen, WinScreen, CrashScreen, GameStart

  Mousex = event.x
  Mousey = event.y
  if HomeScreen == True:

    #This one sets HOW GAME WORKS(HGW) screen to true when mouse click is in this area. 
    #The other code here are the same, but for the other screens.
    if 200 <= Mousex <= 600 and 170 <= Mousey <= 270:
      if HomeScreen == True:
        HomeScreen = False
        HgwScreen = True
        InstrucScreen = False
        WinScreen = False
        CrashScreen = False
        GameStart = False
      
        
    if 200 <= Mousex <= 600 and 330 <= Mousey <= 430:
      if HomeScreen == True:
        HomeScreen = False
        HgwScreen = False
        InstrucScreen = True
        WinScreen = False
        CrashScreen = False
        GameStart = False

        
    if 150 <= Mousex <= 650 and 450 <= Mousey <= 550:
      if HomeScreen == True:
        HomeScreen = False
        HgwScreen = False
        InstrucScreen = False
        WinScreen = False
        CrashScreen = False
        GameStart = True
        drawSky()

    return

  if HgwScreen == True:
      if 625 <= Mousex <= 760 and 490 <= Mousey <= 580:
        HomeScreen = True
        HgwScreen = False
        InstrucScreen = False
        GameStart = False
        screen.delete(Hgw)
      return
    
  if InstrucScreen == True:
      if 625 <= Mousex <= 760 and 490 <= Mousey <= 580:
        HomeScreen = True
        HgwScreen = False
        InstrucScreen = False
        GameStart = False
        screen.delete(Instruction)
      return

  if WinScreen == True:
    if 400<= Mousex <= 600 and 300 <= Mousey <= 400:
      HomeScreen = True
      HgwScreen = False
      InstrucScreen = False
      CrashScreen = False
      WinScreen = False
      GameStart = False
      screen.delete(Win)
    return

  if CrashScreen == True:
    if 400<= Mousex <= 600 and 300 <= Mousey <= 400:
      HomeScreen = True
      HgwScreen = False
      InstrucScreen = False
      CrashScreen = False
      WinScreen = False
      GameStart = False
      screen.delete(Crash)
    return

#------------------------------------------->  
#Gets the angle, later used to determine the exact image for the airplane that is used per frame. Look in the Airplanes folder to see what I'm talking about.
def getAngle():

  #Uses the user's mouse
  dx = xMouse - X_airplane
  dy = Y_airplane - yMouse

  radianAngle = atan2(dy, dx)
  degAngle = degrees (radianAngle)

  if dy>= 0:
    return degAngle
  else:
    return degAngle + 360
#------------------------------------------->
#Prints and angle for the user to see (Display)
def printAngle():
  global angleOutput

  #Makes sure to update every frame by deleting.
  screen.delete(angleOutput)
  if GameStart == True:
    if died == False:
      angleOutput = screen.create_text(100,100,text = "Mouse angle is " + str(int(mouseAngle)), fill = "red", anchor=W)
#------------------------------------------->
#Moves the airplane to your mouse curser, the further your curser is, the faster the airplane, but if it is too far, airplane would slow down more.

#obedience is set in SetInitialValues, it controls how fast plane moves. the smaller the slower
def apUpdate():
  global X_airplane, Y_airplane, obedience, maxSpeed

  obedience = 0.05

  #Max speed is set. If curser is too far, speed becomes slower
  if X_airplane > maxSpeed:
    obedience = 0.03
  if Y_airplane> maxSpeed:
    obedience = 0.03

  X_airplane = X_airplane + (xMouse - X_airplane) * obedience
  Y_airplane = Y_airplane + (yMouse - Y_airplane) * obedience

#------------------------------------------->
#Draws the airplane with the correct image, figured out from the angle calculation above. 
def drawAirplane():
  global airplaneDrawing, airplaneImage, AirplaneDX, AirplaneDY

  screen.delete(airplaneDrawing)

  #gets the write image from the file I already made.
  angle = mouseAngle
  z = int(angle/-5)
  airplaneImage = Airplanefiles[z]

  AirplaneDX = 10
  AirplaneDY = 10
  if died == False:
    airplaneDrawing = screen.create_image( X_airplane, Y_airplane, image = airplaneImage, anchor=CENTER )
  screen.update()

#------------------------------------------->
  #EVERYTHING OBSTACLE RELATED
def spawnObstacle():
  global obstacle,BallDrawing, BaloonDrawing, MissileDrawing, MissileIMG, obsList, obsChoice, spawnTimer,MissileAngle, Missilefiles, Ball_spawnx, Ball_spawny, Baloon_spawnx, Baloon_spawny
  #   #Generate random values for Ball Parabola movement
  Ball_moveX = randint(10,15)
  Ball_moveY = randint(2,7)
  Ball_moveY /= 5
  Ball_moveY2 = randint(10,25)

  #Random values for Balloon Trig movement
  Baloon_moveX = randint(-5,-4)
  Baloon_moveY = randint(39,50)
  Baloon_moveY2 = randint(5,6) / 10


  #Choses a random object, weighted to make the game more smoothly
  #The SpawnTimer counter and the if statement under determines how quick obstacles spawn
  angle = randint(90,270)
  spawnTimer+= 1
  if spawnTimer%8 == 0:
    if died == False:
      obsList = ["Missile", "Ball", "Baloon"]
      obstacle = choices(obsList, weights = (45,40,15))
      obsChoice.append(obstacle[-1])

      #Animation for Balls
      if obsChoice[-1] == "Ball":
        Ball_spawnx = choices(x,weights = (0,0,0,5,5,15,15,20,20,20)) [0]
        Ball_spawny = 500
        
        for b in range(1,100):
          Ball = screen.create_image(Ball_spawnx, Ball_spawny, image = BallPNG, anchor = N)
          Ball_spawnx = Ball_moveX*b +1
          Ball_spawny = Ball_moveY*b**2 - Ball_moveY2*b - 100
  
          BX = int(Ball_spawnx/ 150)
          BY = int(Ball_spawny/ 150)

#Checks for Collision, BX and BY are made 150 to make it more precise. The values are honestly guessed, but work quite well. There are sometimes where objects go through the plane... look at it like you got lucky.
          if BX == int(X_airplane/120) and BY == int(Y_airplane/120):
            return "Collision"
          if BX == int(X_airplane/120) and BY == int(Y_airplane/120):
            return "Collision"
          if BX == int( X_airplane/120) and BY == int( Y_airplane/120):
            return "Collision"
          if BX == int(X_airplane/120) and BY == int(Y_airplane/120):
            return "Collision"
        
          screen.update()
          sleep(0.001)
          screen.delete(Ball)

# Same thing for balloons
      elif obsChoice[-1] == "Baloon":
        Baloon_spawnx = 1200
        Baloon_spawny = choices(y,weights = (16,17,17,17,17,16))[0]
        for b in range(200):
          # print(Baloon_spawnx, Baloon_spawny)
          BaloonDrawing = screen.create_image(Baloon_spawnx, Baloon_spawny, image = BaloonPNG, anchor = CENTER)
    
          Baloon_spawnx = Baloon_moveX*b + 1200
          Baloon_spawny = Baloon_moveY * sin(Baloon_moveY2*b) + Baloon_spawny
          LX = int(Baloon_spawnx/95)
          LY = int(Baloon_spawny/95)
          
#LX and LY are different here, because Ballons are bigger, can be less precise. (Basically means that balloon can hit you from too far out, if LX and LY are divided by more)       
          if LX == int(X_airplane/100) and LY == int(Y_airplane/100):
            return "Collision"
          if LX == int(X_airplane/100) and LY == int(Y_airplane/100):
            return "Collision"
          if LX == int( X_airplane/100) and LY == int( Y_airplane/100):
            return "Collision"
          if LX == int(X_airplane/100) and LY == int(Y_airplane/100):
            return "Collision"
          
          screen.update()
          sleep(0.001)
          screen.delete(BaloonDrawing)
        Baloon_spawnx = 1200
        Baloon_spawny = choices(y,weights = (16,17,17,17,17,16))

# Lastly, Missiles.
      else:
        Missile_spawnx = choices(x, weights = (7,7,7,7,7,7,7,10,10,31))  
        Missile_spawny = choices(y, weights = (50,0,0,0,0,50))
#Gets a random Missile file with a random rotation. Check the Missile folder for the images. The Missile is calculated roughly to fly the direction it is turned in.
        MissileAngle = randint(90,270)
        f = int(MissileAngle/8) 
        MissileImg = Missilefiles[f]
        for m in range(200):
          MissileDrawing = screen.create_image(Missile_spawnx, Missile_spawny, image = MissileImg, anchor=CENTER)
#To see which direction and what angle it flies in
          if f <= 18:
            Missile_spawnx[0]-= 38/f + 5
            Missile_spawny[0]-= 38/f + 5
          else:
            Missile_spawnx[0] -= 38/f + 5
            Missile_spawny[0] += 38/f + 5
# Missile Collisions
          MX = int(Missile_spawnx[0] / 110)
          MY = int(Missile_spawny[0] / 110)
          if MX == int(X_airplane/100) and MY == int(Y_airplane/100):
            return "Collision"
          if MX == int(X_airplane/100) and MY == int(Y_airplane/100):
            return "Collision"
          if MX == int( X_airplane/100) and MY == int( Y_airplane/100):
            return "Collision"
          if MX == int(X_airplane/100) and MY == int(Y_airplane/100):
            return "Collision"
            
          screen.update()
          sleep(0.001)
          screen.delete(MissileDrawing)
          
      sleep(0.01)
  
#------------------------------------------->
#Animating the Collision with an array animation.
#When the airplane gets hit, smoke explodes out.
def Collision():
  global X_airplane, Y_airplane, Smoke
  xSmoke = []
  ySmoke = []
  Diameter = []
  Smoke = []
  SmokeColor = []
  SmokeSpeedX = []
  SmokeSpeedY = []
  NumSmoke = 40


  v = int(X_airplane-65)
  v2 = int(X_airplane+50)
  v3 = int(Y_airplane-30)
  v4 = int(Y_airplane+40)
  for t in range(NumSmoke):
      xSmoke.append(randint(v,v2))
      ySmoke.append(randint(v3,v4))
      SmokeSpeedX.append(randint(-10,10))
      SmokeSpeedY.append(randint(-7,7))
      SmokeColor.append(choice(["#737373", "#666666", "#595959", "#808080", "#4d4d4d"]))
      Diameter.append(randint(8,18))
      Smoke.append(0)
    
  for f in range(2):
    for s in range(NumSmoke):
      Smoke[s] = screen.create_oval(xSmoke[s], ySmoke[s], xSmoke[s]+Diameter[s], ySmoke[s]+Diameter[s], fill=SmokeColor[s])
      
      xSmoke[s]=xSmoke[s]+SmokeSpeedX[s]
      ySmoke[s]=ySmoke[s]+SmokeSpeedY[s]

      screen.update()  
      sleep(0.03)

    for i in range(NumSmoke):
        screen.delete(Smoke[s])

#Just to end the animation sort of, I don't use this anywhere.
  return "End Page"
        
#------------------------------------------->
#You win the game if you cross the line, (x>1000).
def Wingame():
  global X_airplane
  
  if X_airplane >= 750:
    return "Win"
#------------------------------------------->
#------------------------------------------->
#Finally, the game runs with all the buttons, plane movement.
def runGame():
  global died, HomeScreen, InstrucScreen, HgwScreen, CrashScreen, WinScreen, breakloop

  setInitialValues()
  while True:
    #This section make it so the screen changes actually work.
    if HomeScreen:
      screen.delete("all")
      drawHome()
      screen.update()
      sleep(0.01)
      screen.delete(home)

    if HgwScreen:
      screen.delete(home)
      drawHgw()
      screen.update()
      sleep(0.01)
      screen.delete(Hgw)

    if InstrucScreen:
      screen.delete(home)
      drawInstructions()
      screen.update()
      sleep(0.01)
      screen.delete(Instruction)

    if WinScreen:
      screen.delete("all")
      drawWin()
      screen.update()
      sleep(0.01)
      screen.delete(Win)

    if CrashScreen:
      screen.delete("all")
      drawCrash()
      screen.update()
      sleep(0.01)
      screen.delete(Crash)

    #The Loop where the actual game runs
    if GameStart == True:
      screen.delete("all")
      setInitialValues()
      drawSky()

      #Continues running until you either die or win. Breaks, and then calls the draw crash or draw win screen. There, you right click to the home screen like explained.
      while True:

        if breakloop == True:
          break
          
        apUpdate()
    
        spawnObstacle()
        if spawnObstacle() == "Collision":
          Collision()
          died = True
          CrashScreen = True
          drawCrash()

        Wingame()
        if Wingame() == "Win":
          died = True
          WinScreen = True
          drawWin()

        drawAirplane()

        screen.update()
        sleep(0.01)
#------------------------------------------>
#The other things required for game to function
root.after(1,runGame)

#BINDING
screen.bind("<Motion>", mouseMotionHandler)
screen.bind( "<Key>", KeyDownHandler)
screen.bind("<Button-1>", mouseClickHandler)
screen.bind("<Button-3>", EndScreen)

screen.pack()
screen.focus_set()
root.mainloop()