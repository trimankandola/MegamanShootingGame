# Shane Nesarajah and Triman Kandola

from pygame import *
from datetime import datetime
from math import *
from random import *
from glob import *
font.init()
init()
mm=image.load("mainmenu.png") #main menu image file

size = width, height = 1024, 850
screen = display.set_mode(size)
showbar=image.load("showbar.png") #info bar at bottom of screen
levels=['1','2','3','4'] # shows level in the showbar of the screen
GREEN=(0,255,0)
actions=['right'] #list of directions faced by hero
actionshoot="none" #tells whether hero is shooting
bullets=[]  #bullets from hero
bad2bullets=[] #bullets from bad3
direction="right"
move= -1    #for hero's sprites
frame=0 #frame for sprites of the main hero
counter=0
backnum=0 #level
drops=[] #health drops
keyactions=[] #keys that will light up in showbar

ffont=font.SysFont("Comic Sans MS",50)

def drawhealthbar(per,x,y,size,thick):    #healthbar at bottom of screen for hero, and for bad guys, right above them
    diff=int((size-per.w)/2)
    x1=x-diff
    y1=y+per.l-30
    x2=x1+per.hb  
    y2=y1
    draw.line(screen,(0,100,0),(x1,y1),(x2,y2),thick)
#-----------------------------Movement of hero and Bad1-----------------------------------
def moveRight(guy):
    keys=key.get_pressed()
    if guy.vx<5:
        guy.vx+=0.4
    for i in range (int(guy.vx*10)):
        guy.x+=0.1

def moveLeft(guy):
    keys=key.get_pressed()
    if guy.vx>-5:
        guy.vx-=0.4
    for i in range (int(guy.vx*-10)):
        guy.x-=0.1                                                  

def moveUp(guy):
    keys=key.get_pressed()
    for i in range (int(guy.vy*-10)):
        guy.y -= 0.1


def moveDown(guy):
    keys=key.get_pressed()
    for i in range(int(guy.vy*10)):
        if getPixel(maskPic,guy.x,guy.y+1) != GREEN or getPixel(maskPic,guy.x,guy.y) == GREEN or (keys[K_DOWN]==True and guy==hero):
            guy.y += 0.1

        else:
            guy.vy = 0
            guy.og = True
            guy.dj = True
            if isinstance(guy,Bad1):
                if guy.d=="left":
                    guy.m=1
                elif guy.d=="right":
                    guy.m=0
#------------------------------------class for main hero----------------------------------------------------
class Guy:

    def __init__(self,x,y,w,l,vx,vy,og,dj,h,hb): #x, y, width, length,horiz. velocity, vertic. velocity, onground, double jump, health, healthbar
        self.x=x
        self.y=y
        self.w=w
        self.l=l
        self.vx=vx
        self.vy=vy
        self.og=og
        self.dj=dj
        self.h=10
        self.hb=hb
    def move(self):
        global move, frame, direction, actionshoot
        keys=key.get_pressed()
        newm=-1
        makeguyrect(self)
        actionshoot="none"

        if keys[K_SPACE]:
            keyactions.append(4)                #makes hero shoot
            actionshoot="shooting"
            if counter%7==0:
                bullets.append([self.x,self.y-20,actions[-1]])

        if keys[K_SPACE]==False and 4 in keyactions:
            keyactions.remove(4)

        if len(actions)>1 and actions[-1]!=actions[-2]:
            self.vx=0

        if keys[K_LEFT] and self.x > 0: #moves left
            keyactions.append(1)
            if actionshoot=="shooting":
                newm=5
            else:
                newm=3
            moveLeft(self)
            actions.append('left')
            direction="left"

        if keys[K_LEFT]==False and 1 in keyactions:
            keyactions.remove(1)

        if keys[K_RIGHT] and self.x < 1024: #moves right
            keyactions.append(3)
            if actionshoot=="shooting":
                newm=4
            else:
                newm=0
            moveRight(self)
            actions.append('right')
            direction="right"

        if keys[K_RIGHT]==False and 3 in keyactions:
            keyactions.remove(3)

        if keys[K_UP] and self.og==True: #makes hero jump
            keyactions.append(0)
            if direction=="right":
                if actionshoot=="shooting": 
                    newm=6
                else:
                    newm=2
            if direction=="left":
                if actionshoot=="shooting":
                    newm=7
                else:
                    newm=1
            self.vy = -10
            self.og=False

        if keys[K_UP]==False and 0 in keyactions:
            keyactions.remove(0)

        if keys[K_DOWN]: #makes hero fall faster/through platform
            keyactions.append(2)
            newm=-1
            self.og=False
            self.vy=+10

        if keys[K_DOWN]==False and 2 in keyactions:
            keyactions.remove(2)

        if self.vy<0:
            moveUp(self)

        elif self.vy>0:
            moveDown(self)

            
        if keys[K_RIGHT]==False and keys[K_LEFT]==False: #slows down hero's momentum when not moving


            if self.vx>0:
                if self.og==True:
                    self.vx-=0.4
                    if self.vx<0:
                        self.vx=0
                else:
                    self.vx-=0.2

            if self.vx>-0.1 and self.vx<0:
                self.vx=0


            if self.vx<0:
                if self.og==True:
                    self.vx+=0.4
                else:
                    self.vx+=.2


            self.x+=self.vx

        if keys[K_RIGHT]==False and keys[K_LEFT]==False and keys[K_UP]==False and keys[K_DOWN]==False and self.og: #for when standing still
            frame=0
            move=-1

        if move==newm:
            frame+=0.5
            if frame>=len(pics[move]): #changes sprite frames
                frame=1
        elif newm!=-1:
            move=newm
            frame=1
         
        if self.y >= 560:
            self.y = 560
            self.vy = 0
            self.og=True
            self.dj=True
        self.vy+=.5



#------------------------------------------class for the enemy (ZERO)----------------------------------------

class Bad1:

    def __init__(self,x,y,w,l,vx,vy,og,h,hb):
        self.x=x
        self.y=y
        self.w=w
        self.l=l
        self.vy=vy
        self.vx=vx
        self.og=og
        self.h=h
        self.hb=hb
        self.m=0 # sprite frames
        self.f=0 #
        self.d="right" #direction facing

    def move(self):

        if self.x- hero.x > 19: #move left
            self.m=1
            self.d="left"
            if self.vx>-3:
                self.vx-=0.4
            for i in range (int(self.vx*-10)):
                if getPixel(maskPic,self.x-47,self.y)!=GREEN:
                    self.x-=0.1
        elif self.x-hero.x < -19: #move right
            self.m=0
            self.d="right"
            if self.vx<3:
                self.vx+=0.4
            for i in range (int(self.vx*10)):
                if getPixel(maskPic,self.x+2,self.y)!=GREEN:
                    self.x+=0.1

        if hero.x<self.x+25 and hero.x>self.x-25 and self.og==True and self.y> hero.y: #jump
            self.vy-=13
            self.og= False

        if self.vy<0:
            if self.d=="left":  #sprites for jumping
                self.m=3
            elif self.d=="right":
                self.m=2
            moveUp(self)

        elif self.vy>0:
            moveDown(self)


        if self.y >= 560:
            self.y=560
            self.vy=0
            self.og=True
        self.vy+=.5

        if self.f>=len(zpics[self.m])-1: #change sprite frames
            self.f=0
        self.f+=0.5

#----------------------------------class for goomba------------------------------------------------
class Bad2:

    def __init__(self,x,y,w,l,h,d,hb):
        self.x=x
        self.y=y
        self.w=w
        self.l=l
        self.h=h
        self.d=d
        self.hb=hb
        self.f=0
        self.m=0

    def move(self):
        if self.d=='right':
            self.m=0
            if getPixel(maskPic,self.x+1,self.y+5)==GREEN:           #move back and forth to both ends of platform
                self.x+=2
            else:
                self.d='left'
        else:
            self.m=1
            if getPixel(maskPic,self.x+self.w-1,self.y+5)==GREEN:
                self.x-=2
            else:
                self.d='right'
        if self.f==len(gpics[self.m])-1:
            self.f=0
        self.f+=0.5
        
#-----------------------------class for missile shooter-----------------------------------
class Bad3:

    def __init__(self,x,y,w,l,h,hb):
        self.x=x
        self.y=y
        self.w=w
        self.l=l
        self.h=h
        self.hb=hb
        self.m=0
        self.f=0
        self.a=0  #angle from positive x axis to hero, for path of bullets
        self.d="right"
        self.s=randint(10,55) #tells time when bad3 will shoot

    def move(self):
        xdist=hero.x-20-(self.x-30)
        ydist=hero.y-20-(self.y-30)
        dist=((xdist)**2+(ydist)**2)**0.5
        if dist>70:# wont shoot if hero is too close
            if xdist>-1 and ydist<0:
                self.a=fabs(degrees(atan(ydist/xdist)))
            elif xdist<0 and ydist<0:
                self.a=180-fabs(degrees(atan(ydist/xdist)))   #calculate shooting angle
            elif xdist<0 and ydist>-1:
                self.a=fabs(degrees(atan(ydist/xdist)))+180
            else:
                self.a=360-fabs(degrees(atan(ydist/xdist)))
                
            if 90>self.a and self.a>78.75:   #these angles require separate if statements becasue there are two sprite sets for both 90 and 270 degrees
                self.m=4
            elif self.a>270 and self.a<281.26:
                self.m=14
            else:
                for i in range (0,3599,225):
                    if i/10>348.74:
                        self.m=0
                    if self.a>i/10-11.25 and self.a<i/10+11.25: #changes sprite sets
                        if self.a>89.999 and self.a<270:
                            self.m=int(i/225)+1
                        elif self.a>281.2499:
                            self.m=int(i/225)+2
                        else:
                            self.m=int(i/225)
                            
            for i in range(18):
                if self.m==i:
                    if counter%70==self.s:
                        m=randint(0,9) #m is chance of bad3 shooting green missile which is 1/10
                        if i==0:
                            bad2bullets.append([self.x+12,self.y-27,xdist,ydist,dist,transform.rotate(ms[m],self.a),m])
                        elif i==1:
                            bad2bullets.append([self.x+15,self.y-35,xdist,ydist+20,dist,transform.rotate(ms[m],self.a),m])
                        elif i==2:
                            bad2bullets.append([self.x+12,self.y-55,xdist,ydist,dist,transform.rotate(ms[m],self.a),m])
                        elif i==3:
                            bad2bullets.append([self.x,self.y-60,xdist,ydist,dist,transform.rotate(ms[m],self.a),m])
                        elif i==4:
                            bad2bullets.append([self.x-13,self.y-70,xdist,ydist,dist,transform.rotate(ms[m],self.a),m])
                        elif i==5:
                            bad2bullets.append([self.x-55,self.y-67,xdist,ydist,dist,transform.rotate(ms[m],self.a),m])
                        elif i==6:
                            bad2bullets.append([self.x-77,self.y-70,xdist,ydist,dist,transform.rotate(ms[m],self.a),m])
                        elif i==7:
                            bad2bullets.append([self.x-85,self.y-60,xdist,ydist,dist,transform.rotate(ms[m],self.a),m])
                        elif i==8:
                            bad2bullets.append([self.x-90,self.y-50,xdist,ydist,dist,transform.rotate(ms[m],self.a),m]) #since bad3's hand changes positionwith each 
                        elif i==9:                                                                                      #angle, we must change the starting point of the bullet
                            bad2bullets.append([self.x-85,self.y-29,xdist,ydist,dist,transform.rotate(ms[m],self.a),m])
                        elif i==10:
                            bad2bullets.append([self.x-85,self.y-10,xdist,ydist+30,dist,transform.rotate(ms[m],self.a),m])
                        elif i==11:
                            bad2bullets.append([self.x-75,self.y-5,xdist,ydist+30,dist,transform.rotate(ms[m],self.a),m])
                        elif i==12:
                            bad2bullets.append([self.x-65,self.y,xdist+30,ydist,dist,transform.rotate(ms[m],self.a),m])
                        elif i==13:
                            bad2bullets.append([self.x-60,self.y,xdist+50,ydist,dist,transform.rotate(ms[m],self.a),m])
                        elif i==14:
                            bad2bullets.append([self.x-5,self.y,xdist,ydist,dist,transform.rotate(ms[m],self.a),m])
                        elif i==15:
                            bad2bullets.append([self.x+5,self.y,xdist,ydist,dist,transform.rotate(ms[m],self.a),m])
                        elif i==16:
                            bad2bullets.append([self.x+13,self.y-3,xdist,ydist+30,dist,transform.rotate(ms[m],self.a),m])
                        elif i==17:
                            bad2bullets.append([self.x+18,self.y-10,xdist,ydist,dist,transform.rotate(ms[m],self.a),m])
                                           
            if counter%5==0 and counter%70>self.s-11 and counter%70<self.s+15:
                self.f+=1
                if self.f==len(bad3pics[self.m]):       #change sprite frame
                    self.f=0
            if counter%70==self.s+15:
                self.f=0
        else:
            self.f=0

#-----------------------------------class for boo (floating ghost)------------------------------------------------
class Bad4:

    def __init__(self,x,y,w,l,h,hb):
        self.x=x
        self.y=y
        self.w=w
        self.l=l
        self.h=h
        self.hb=hb
        self.m=0
        self.f=0
    def move(self):
        xdist=self.x-hero.x
        ydist=self.y-hero.y
        dist=((xdist)**2+(ydist)**2)**0.5                                                   
        if ((xdist>0 and actions[-1]=='left') or (xdist<1 and actions[-1]=='right') or fabs(ydist)>250 or fabs(xdist)>300): #move if hero is not looking or is far away
            if fabs(xdist)>2:
                self.x-=xdist/dist*2
                self.y-=ydist/dist*2
            if xdist>0:
                self.m=1
            else:
                self.m=0
            if counter%15==0:
                self.f+=1
                if self.f==len(bad4pics[self.m]):
                    self.f=0
        else:
            if xdist>0:             #else, will stop and cover eyes
                self.m=3
            else:
                self.m=2
            if self.f>2:
                self.f=0
            if counter%5==0 and self.f!=2:
                self.f+=1
            
       

def getPixel(mask,x,y):
    if 0<= x < mask.get_width() and 0 <= y < mask.get_height(): #checks mask colour
        return mask.get_at((int(x),int(y)))
    else:
        return (-1,-1,-1)

def makeMove(name):
    lmove=glob(name+"\\*.png")  #gets all sprite images from folder, and puts them into a list
    lmove.sort()
    move=[]
    for l in lmove:
        move.append(image.load(l))
    return move

def lightuprect(rect): #lights up arrow keys in information bar
    draw.rect(screen,rect[4],Rect(rect[0],rect[1],rect[2],rect[3]),2) 

def makeguyrect(guy):
    newrect=Rect(guy.x-guy.w//2,guy.y,guy.w,guy.l) #creates rect around 'guy'
    newrect.normalize()
    return newrect

def bulletmove():
    for b in bullets:
        if b[2]=='right':
            b[0]+=10
        else:
            b[0]-=10
        if b[0]<0 or b[0]>1024:   #controls bullets of both bad3 and hero
            bullets.remove(b)
    for b in bad2bullets:
        b[0]+=b[2]/b[4]*6
        b[1]+=b[3]/b[4]*6
        if b[0]<0 or b[0]>1024 or b[1]<0 or b[1]>700:
            bad2bullets.remove(b)

def explode(x,y):
    for i in range(24):
        screen.blit(explosion[i],(x,y))     #for bad3's green missile explosion
        time.wait(5)
    

def damagehit(): #applies damage for all characters, by bullets or contact
    global smishit, eframe

    for e in enemies2:

        for b in bullets:
            enemy=makeguyrect(e)
            enemy.normalize()
            if enemy.collidepoint((b[0],b[1])):
                bullets.remove(b)
                e.h-=1
                e.hb-=20

        if isinstance (e,Bad3):
            rect=Rect(e.x,e.y,e.w,e.l) #cannot use makguyrect function for bad3 due to different arm positions for diff. angles
            rect.normalize()
            if rect.colliderect(makeguyrect(hero)):
                if counter%80==0:
                    hero.h-=1
                    hero.hb-=12  
        else:
            if makeguyrect(e).colliderect(makeguyrect(hero)):
                if counter%60==0:
                    hero.h-=1
                    hero.hb-=12
                

        if e.h==0:
            dropnum=randint(0,5)
            if dropnum==4:                              #1/6 chance to drop health potion
                drops.append([int(e.x),int(e.y)+e.l])
            deadenemies.append(e)
            enemies2.remove(e)
            spawnenemy()
            if len(enemies[0]+enemies[1]+enemies[2]+enemies[3])-len(deadenemies)==0: #level up if all enemies are dead
                levelup()

    for b in bad2bullets:
        herorect=makeguyrect(hero)
        herorect.normalize()
        
        if herorect.collidepoint(b[0],b[1])and b[6]>=0 and b[6]<=8:
            bad2bullets.remove(b)
            hero.h-=1
            hero.hb-=12
            
        elif herorect.collidepoint(b[0],b[1])  and b[6]==9:
            smishit=True   #smishit is a varibale that controls the sprites for the super missile which explodes when it hits the hero
            eframe+=1
            bad2bullets.remove(b)
            hero.h-=5
            hero.hb-=60

        if eframe>0:
            eframe+=1
        if eframe==23:
            eframe=0
            smishit=False
        

def dropcontrol(): #controls health potions
    for d in drops:
        for i in range(5):
            if getPixel(maskPic,d[0],d[1]+1) != GREEN:
                d[1]+=1

        if makeguyrect(hero).colliderect(Rect(d[0],d[1]-25,25,25)): #drop disappears and heals hero
            if hero.hb>587:
                hero.h=54
                hero.hb=648
            else:
               hero.h+=5
               hero.hb+=60
            drops.remove(d)


def spawnenemy():
    while len(enemies2)<5 and len(enemies[0]+enemies[1]+enemies[2]+enemies[3])-len(deadenemies)>4: #max 5 enemies at once
        try:
            newenemy=enemies[randint(0,3)][randint(0,7)]
            if newenemy not in enemies2 and newenemy not in deadenemies:
                enemies2.append(newenemy)
        except IndexError:
            pass

def levelup(): 
    global backnum, backPic, maskPic, bad1, bad2, bad3, bad4, enemies, enemies2, deadenemies
    if backnum==3: #if game is over
        menu()
    else:
        backnum+=1
        screen.blit(leveluppics[backnum],(0,0))  #shows transition screen
        display.flip()
        myClock.tick(0.33)
        myClock.tick(60)
        backPic=backgrounds[backnum]
        maskPic=masks[backnum]
        bad1=totbad1[backnum]
        bad2=totbad2[backnum] #changes background, mask, and enemies
        bad3=totbad3[backnum]
        bad4=totbad4[backnum]
        enemies=[bad1,bad2,bad3,bad4]
        enemies2=[]
        deadenemies=[]
        bullets=[]
        bad2bullets=[]
        spawnenemy()
    

def drawScene(screen):  #displays the game
    screen.blit(backPic,(0,0))
    screen.blit(showbar,(0,700))

    if move!=-1:
        pic = pics[move][int(frame)]
        screen.blit(pic,(hero.x-pic.get_width()//2,hero.y-pic.get_height()))
    if move==-1 and direction=="right" and actionshoot=="none":
        pic = image.load("standingstill\standingstill0.png")
        screen.blit(pic,(hero.x-pic.get_width()//2,hero.y-pic.get_height()))
    if move==-1 and direction=="left" and actionshoot=="none":
        pic = image.load("standingstill\standingstill1.png")
        screen.blit(pic,(hero.x-pic.get_width()//2,hero.y-pic.get_height()))            #sprites for when hero not running
    if move==-1 and direction=="right" and actionshoot=="shooting":
        pic = image.load("stillshoot\shootingright0.png")
        screen.blit(pic,(hero.x-pic.get_width()//2,hero.y-pic.get_height()))
    if move==-1 and direction=="left" and actionshoot=="shooting":
        pic = image.load("stillshoot\shootingleft0.png")
        screen.blit(pic,(hero.x-pic.get_width()//2,hero.y-pic.get_height()))
    drawhealthbar(hero,700,875,648,40)

    for i in enemies2:                 #draw healthbar for enemies currently on screen
        drawhealthbar(i,i.x,i.y,100,20)

    for b in bad1:
        if b in enemies2:
            pic=zpics[b.m][int(b.f)]
            screen.blit(pic,(b.x-pic.get_width()//2,b.y-pic.get_height()))

    for b in bad2:
        if b in enemies2:
            pic=gpics[b.m][int(b.f)]
            pic=transform.scale(pic,(pic.get_width()//2,pic.get_height()//2))       #sprites for bad guys
            screen.blit(pic,(b.x-pic.get_width()//2,b.y-pic.get_height()))

    for b in bad3:
        if b in enemies2:
            pic=bad3pics[b.m][int(b.f)]
            if b.a<191 and b.a>79:
                screen.blit(pic,(b.x-pic.get_width(),b.y-pic.get_height()))
            elif b.a<90:
                screen.blit(pic,(b.x-65,b.y-pic.get_height()))
            elif b.a>190 and b.a<270:
                screen.blit(pic,(b.x-pic.get_width(),b.y-61))
            else:
                screen.blit(pic,(b.x-65,b.y-61))

    for b in bad4:
        if b in enemies2:
            pic=bad4pics[b.m][b.f]
            screen.blit(pic,(b.x-pic.get_width()//2,b.y-pic.get_height()))

    for d in drops:
        screen.blit(droppic,(d[0],d[1]-25))
    for b in bullets:
        draw.circle(screen,(100,0,0),(int(b[0]),int(b[1])),2)                   #blits bullets and health drops
    for b in bad2bullets:
        screen.blit(b[5],(b[0]-b[5].get_width()//2,b[1]-b[5].get_height()//2))
    if smishit:  #blits the sprites for explosion after the hero is hit with a super missile (green missile)
        screen.blit(explos[int(eframe)],(hero.x+hero.w//2,hero.y+hero.l))
    for k in keyactions:
        lightuprect(keyrects[k]) 
    levtxt=ffont.render(levels[backnum],False,(0,0,0))                  #info bar
    entxt=ffont.render(str(len(enemies[0])+len(enemies[1])+len(enemies[2])+len(enemies[3])-len(deadenemies)),False,(0,0,0))
    screen.blit(levtxt,(130,755))
    screen.blit(entxt,(250,750))
    
    display.flip()





def game():                 #main running loop
    global running,counter,screen,countdown
    screen.blit(leveluppics[backnum],(0,0))
    display.flip()
    myClock.tick(0.33)
    myClock.tick(60)
    while running:

        for evnt in event.get():    
            if evnt.type == QUIT:
                running = False

            if evnt.type == KEYDOWN: #used for double jumping
                if evnt.key==K_UP and hero.og==False and hero.dj==True:
                    hero.vy=-10
                    hero.dj=False


        keys = key.get_pressed()


        if counter==1000:
            counter=0
        mx,my=mouse.get_pos()
        hero.move()
        for e in enemies2:               
            e.move()
        bulletmove()
        damagehit()
        dropcontrol()
        drawScene(screen)
        if hero.hb<=0:
            screen.blit(gameoverpic,(0,0))
            display.flip()
            myClock.tick(0.25)
            myClock.tick(60)
            quit()
        myClock.tick(60)
        counter+=1
            
    
    return "menu"


def instructions():  #function used to show the instructions on the screen
    running = True
    inst = image.load("instructions.png")
    inst = transform.smoothscale(inst, screen.get_size())
    screen.blit(inst,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        if key.get_pressed()[27]: running = False

        display.flip()
    return "menu"
        

def menu():      #shows menu screen
    hero.hb=648
    hero.h=54
    healthdrops=[]
    backPic=backgrounds[backnum]
    maskPic=masks[backnum]
    bad1=totbad1[backnum]
    bad2=totbad2[backnum]
    bad3=totbad3[backnum]
    bad4=totbad4[backnum]
    enemies=[bad1,bad2,bad3,bad4]
    enemies2=[]
    deadenemies=[]
    bullets=[]
    bad2bullets=[]
    
    running = True
    myClock = time.Clock()
    buttons = [Rect(400,y*95+638,263,72) for y in range(2)]
    vals = ["game","instructions"]
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "exit"

        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        screen.blit(mm,(0,0))
        for r,v in zip(buttons,vals):
            if r.collidepoint(mpos):
                draw.rect(screen,(0,255,0),r,2)
                if mb[0]==1:
                    return v
            else:
                draw.rect(screen,(255,255,0),r,2)
                
        display.flip()

#--------------------------------------Sprites and other data (pictures)--------------------------------------
pics=[] #hero sprites
bad3pics=[makeMove('bad300'),makeMove('bad322.5'),makeMove('bad345'),makeMove('bad367.5'),makeMove('bad378.75'),makeMove('bad390'), makeMove('bad3112.5'),
          makeMove('bad3135'), makeMove('bad3157.5'),makeMove('bad3180'), makeMove('bad3202.5'), makeMove('bad3225'), makeMove('bad3247.5'),
          makeMove('bad3270'),makeMove('bad3281.25'),makeMove('bad3292.5'),makeMove('bad3315'),makeMove('bad3337.5')] #bad3 sprites
bad4pics=[makeMove('bad40'),makeMove('bad42'),makeMove('bad41'),makeMove('bad43')] #bad4 sprites
pics.append(makeMove("runningright"))
pics.append(makeMove("jumpingleft"))
pics.append(makeMove("jumpingright"))
pics.append(makeMove("runningleft"))
pics.append(makeMove("runshootright"))
pics.append(makeMove("runshootleft"))
pics.append(makeMove("jumpshootright"))
pics.append(makeMove("jumpshootleft"))
gpics=[]
gpics.append(makeMove("goombaright")) #bad2 sprites
gpics.append(makeMove("goombaleft"))
zpics=[]
zpics.append(makeMove("zeroright")) #bad1 sprites
zpics.append(makeMove("zeroleft"))
zpics.append(makeMove("zerojumpright"))
zpics.append(makeMove("zerojumpright"))
missile=transform.scale(image.load('missile.png'),(40,16)) #bad3 missile
supermissile=transform.scale(image.load('supermissile.png'),(40,16)) #green missile
ms=[]
ms.append(missile)  #appends missiles so that there is only a 1/10 of a chance for the super missile to show up
ms.append(missile)
ms.append(missile)
ms.append(missile)
ms.append(missile)
ms.append(missile)
ms.append(missile)
ms.append(missile)
ms.append(missile)
ms.append(supermissile)
smishit=False
explos=makeMove("explosion") #green missile explosion
eframe=0
droppic=transform.scale(image.load('healthdrop.png'),(20,26)) #health potion pic

leveluppics=[image.load('level1.jpg'),image.load('level2.jpg'),image.load('level3.jpg'),image.load('level4.jpg')]
gameoverpic=image.load('gameover.jpg')
backgrounds=[image.load('background.png'),image.load('background2.jpg'),image.load('background3.png'),image.load('background4.jpg'),
             transform.scale(image.load('background5.png'),(1024,700))]
masks=[image.load('mask.png'),image.load('mask2.png'),image.load('mask3.png'),image.load('mask4.png')]
backPic=backgrounds[backnum] #background
maskPic=masks[backnum] #mask
keyrects=[[50,730,30,35,(255,255,0)],[20,765,30,35,(255,255,0)],
          [50,765,30,35,(255,255,0)],[80,765,30,35,(255,255,0)],
          [20,805,90,35,(255,255,0)]]
#enemies for level 1:
bad1_1=Bad1(0,400,-50,-50,0,0,True,5,100)
bad1_2=Bad1(500,100,-50,-50,0,0,True,5,100)
bad1_3=Bad1(700,100,-50,-50,0,0,True,5,100)
bad2_1=Bad2(500,100,-30,-30,5,'right',100)
bad2_2=Bad2(400,215,-30,-30,5,'right',100)
bad2_3=Bad2(700,215,-30,-30,5,'right',100)
bad2_4=Bad2(800,330,-30,-30,5,'right',100)
bad2_5=Bad2(900,440,-30,-30,5,'right',100)
bad2_6=Bad2(200,440,-30,-30,5,'right',100)
bad2_7=Bad2(500,330,-30,-30,5,'right',100)
bad3_1=Bad3(450,215,-50,-50,5,100)
bad4_1=Bad4(50,560,-30,-30,5,100)
bad4_2=Bad4(100,300,-30,-30,5,100)
bad4_3=Bad4(700,600,-30,-30,5,100)
bad4_4=Bad4(50,300,-30,-30,5,100)
bad4_5=Bad4(700,600,-30,-30,5,100)
bad4_6=Bad4(200,600,-30,-30,5,100)

bad1_lvl1=[bad1_1,bad1_2,bad1_3]
bad2_lvl1=[bad2_1,bad2_2,bad2_3,bad2_4,bad2_5,bad2_6,bad2_7]
bad3_lvl1=[bad3_1]
bad4_lvl1=[bad4_1,bad4_2,bad4_3,bad4_4,bad4_5,bad4_6]

#enemies for level 2:
bad1_1_2=Bad1(0,401,-50,-50,0,0,True,5,100)
bad1_2_2=Bad1(100,402,-50,-50,0,0,True,5,100)
bad1_3_2=Bad1(200,403,-50,-50,0,0,True,5,100)
bad1_4_2=Bad1(300,404,-50,-50,0,0,True,5,100)
bad1_5_2=Bad1(400,405,-50,-50,0,0,True,5,100)
bad1_6_2=Bad1(500,406,-50,-50,0,0,True,5,100)
bad2_1_2=Bad2(450,335,-30,-30,5,'right',100)
bad2_2_2=Bad2(200,230,-30,-30,5,'right',100)
bad2_3_2=Bad2(600,335,-30,-30,5,'right',100)
bad3_1_2=Bad3(800,230,-50,-50,5,100)
bad3_2_2=Bad3(200,435,-50,-50,5,100)
bad3_3_2=Bad3(600,335,-50,-50,5,100)
bad4_1_2=Bad4(50,560,-30,-30,5,100)
bad4_2_2=Bad4(500,50,-30,-30,5,100)
bad4_3_2=Bad4(300,560,-30,-30,5,100)

bad1_lvl2=[bad1_1_2,bad1_2_2,bad1_3_2,bad1_4_2,bad1_5_2,bad1_6_2]
bad2_lvl2=[bad2_1_2,bad2_2_2,bad2_3_2]
bad3_lvl2=[bad3_1_2,bad3_2_2,bad3_3_2]
bad4_lvl2=[bad4_1_2,bad4_2_2,bad4_3_2]

#enemies for level 3:
bad1_1_3=Bad1(0,401,-50,-50,0,0,True,5,100)
bad1_2_3=Bad1(100,401,-50,-50,0,0,True,5,100)
bad1_3_3=Bad1(200,401,-50,-50,0,0,True,5,100)
bad1_4_3=Bad1(300,401,-50,-50,0,0,True,5,100)
bad1_5_3=Bad1(400,401,-50,-50,0,0,True,5,100)
bad1_6_3=Bad1(500,401,-50,-50,0,0,True,5,100)
bad1_7_3=Bad1(0,401,-50,-50,0,0,True,5,100)
bad3_1_3=Bad3(150,250,-50,-50,5,100)
bad3_2_3=Bad3(350,390,-50,-50,5,100)
bad3_3_3=Bad3(520,293,-50,-50,5,100)
bad3_4_3=Bad3(750,391,-50,-50,5,100)
bad3_5_3=Bad3(900,236,-50,-50,5,100)

bad1_lvl3=[bad1_1_3,bad1_2_3,bad1_3_3,bad1_4_3,bad1_5_3,bad1_6_3,bad1_7_3]
bad2_lvl3=[]
bad3_lvl3=[bad3_1_3,bad3_2_3,bad3_3_3,bad3_4_3,bad3_5_3]
bad4_lvl3=[]

#enemies for level 4:
bad1_1_4=Bad1(0,401,-50,-50,0,0,True,5,100)
bad1_2_4=Bad1(100,401,-50,-50,0,0,True,5,100)
bad1_3_4=Bad1(200,401,-50,-50,0,0,True,5,100)
bad1_4_4=Bad1(300,401,-50,-50,0,0,True,5,100)
bad1_5_4=Bad1(400,401,-50,-50,0,0,True,5,100)
bad1_6_4=Bad1(500,401,-50,-50,0,0,True,5,100)
bad1_7_4=Bad1(0,401,-50,-50,0,0,True,5,100)
bad3_1_4=Bad3(205,210,-50,-50,5,100)
bad3_2_4=Bad3(360,355,-50,-50,5,100)
bad3_3_4=Bad3(530,197,-50,-50,5,100)
bad3_4_4=Bad3(730,344,-50,-50,5,100)
bad3_5_4=Bad3(900,198,-50,-50,5,100)
bad3_6_4=Bad3(215,485,-50,-50,5,100)
bad3_7_4=Bad3(530,470,-50,-50,5,100)
bad3_8_4=Bad3(900,490,-50,-50,5,100)

bad1_lvl4=[bad1_1_4,bad1_2_4,bad1_3_4,bad1_4_4,bad1_5_4,bad1_6_4,bad1_7_4]
bad3_lvl4=[bad3_1_4,bad3_2_4,bad3_3_4,bad3_4_4,bad3_5_4,bad3_6_4,bad3_7_4,bad3_8_4]

#lists of all enemies
totbad1=[bad1_lvl1,bad1_lvl2,bad1_lvl3,bad1_lvl4]
totbad2=[bad2_lvl1,bad2_lvl2,bad2_lvl3,[]]
totbad3=[bad3_lvl1,bad3_lvl2,bad3_lvl3,bad3_lvl4]
totbad4=[bad4_lvl1,bad4_lvl2,bad4_lvl3,[]]

bad1=totbad1[backnum]
bad2=totbad2[backnum]
bad3=totbad3[backnum]
bad4=totbad4[backnum]

enemies=[bad1,bad2,bad3,bad4] #enemies for current level
enemies2=[]# enemies currently on screen
deadenemies=[]#enemies killed in current level
spawnenemy()


running = True          
myClock = time.Clock()  
hero= Guy(512,350,-37,-47,0,0,True,True,54,648) #main character
health=5
page = "menu"

while page != "exit":
    if page == "menu":
        page = menu()
    if page == "game":
        page = game()
    if page=="game" and running == False:
        page="exit"
    if page == "instructions":
        page = instructions()    
    
    
quit()
