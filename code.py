# python3 file name
from main import *
import random

Dog= True # to check if the dog is alive
Total_Survivors= 1 # if this hits 0 then you lose
Round= 0 # if this hits 100 the game finishes and you win
Count= 0 # used to give a name to survivors in the list
Survivors= [] # list for survivors
ammo= 3 # total ammo
food= 5 # total food

def pause(): #(temporary so that you have to press enter to go the next day for unfinished code)
    Continue="123"
    while Continue!= "":
        Continue= input("Press enter to continue to the next day")

def setup():
    global Count
    global Survivors
    global Total_Survivors
    Add_Survivors= random.randint(1,4)      # sets up the game intro
    Total_Survivors+= Add_Survivors
    print(f"A zombie apocalypse has started, survive 100 days, in total: {Total_Survivors} of the mystery gang have survived. You have one dog, good luck")
    for i in range (Total_Survivors):
        Survivors.append("Chr"+str(Count))  # adds all survivors to the list and works out how many survive
        Count+= 1
    print(Survivors)
    next_day()        

def Character_Setup():          # will create objects per survivor
    for i in range(Count):
        pass
        
        


def Dice1():                            
    dice1= random.randint(1,6)
    return dice1                # Sets up both die for the days
def Dice2():
    dice2= random.randint(1,6)
    return dice2

class Alive():                                  # sets up the health and hunger for all survivors and the healing method
    def __init__(self):
        self.max_health= random.randint(4,8)
        self.health= self.max_health
        self.hunger= 5
    def heal(self):
        if (self.health+3)>self.max_health:
            pass
        else:
            self.health+= 3

def Events(Dog,Count):    # all the events
    global ammo
    global food
    Die1= Dice1()
    Die2= Dice2()
                # Chooses the events that occur based on dice roll

                
    if Die1== 1 or Die1==3:   #zombie apocalypse                                                            # Zombie
        if Die1== 1 and Die2== 3 or Die1== 3 or Die2== 1:
            print(f"A zombie apocalypse has started, you are surrounded by {random.randint(1,4)}zombies"
                  "You will need to fight them off and survive.")
            pause()
        elif Die2== 2:   # ammo + zombie
            if Dog== True:
                pass
            print("You find an abandoned building, it seems like someone has taken as much as they can, but"
                    " but perhaps you can find something they left behind?")
            pause()
        elif Die2== 4:     # food + zombie
            if Dog== True:
                pass
            print("You find an abandoned building, it seems like someone has taken as much as they can, but"
                    " but perhaps you can find something they left behind?")
            pause()
        elif Die2== 5: # Mini zombie apocalypse
           print("You enter an opening, it seems like it'd be an perfect opportunity to rest."
                 "\n As you turn the corner, you notice that you were wrong, as a couple of "
                 "Zombies emerge from behind the corner")
           pause()
        elif Die2== 6:       # Survivor and zombies
           print("You have found a survivor, they have been ambushed by 2 zombies and are currently"
                 " unprepared for this fight. You must defeat these 2 zombies before the survivor"
                 "gets bit and becomes one too.")
           pause()

           
    elif Die1== 2:                                                                                          # ammo
        if Die2== 1 or Die2== 3: # ammo + zombie
            if Dog== True:
                pass
            print("You find an abandoned building, it seems like someone has taken as much as they can, but"
                    " but perhaps you can find something they left behind?")
            pause()
        elif Die2== 2:   # Ammo
            print("You search the area, it doesnt seem like theres any zombies here. On the side you"
                  "find a fallen survivor. Theres nothing you can do for them now."
                  "You notice some ammo they carried")
            ammo+= 4
            pause()
        elif Die2== 4: # Ammo + food
            print("You search the area, it doesnt seem like theres any zombies here. On the side you"
                  "find a fallen survivor. Theres nothing you can do for them now."
                  "You notice some ammo and food they carried")
            ammo+=2
            food+=2
            pause()
        elif Die2== 5:  # Ammo/zombie
            print("You find an area covered in bushes. It seems like its been abandoned for quite a while"
                  "You find 2 ammo at the door, you can try to find more ammo inside, but you dont know if something"
                  "is lurking inside or not, do you take the risk?")
            ammo+= 2
            pause()

        elif Die2== 6: # food for ammo trade
            Trade= ""
            print ("You hear a noise and snap around, come face to face with another survivor. They show no interest in joining you.\nThey show no signs of hostility. In fact, they beg for food, in exchange for ammo they have\nPerhaps theyre not a fighter and just wish to survive, making the ammo useless to them, do you accept? Y/N")
            while Trade!= "N" and Trade !="Y":
                Trade= input(f"Type Y/N only. You have {ammo} ammo and {food} food" ).upper()
                if Trade== "N":
                    pass
                elif Trade== "Y":
                    if food== 0:
                        print("You have run out of food")
                    else:
                        ammo+= 1
                        food-= 1
                        Trade= ""


                        
    elif Die1==4:                                                                                               # food
        if Die2== 1 or Die2==3:     # food + zombie
            if Dog== True:
                pass
            print("You find an abandoned building, it seems like someone has taken as much as they can, but"
                    " but perhaps you can find something they left behind?")
            pause()
        elif Die2== 2: # Ammo + food
            print("You search the area, it doesnt seem like theres any zombies here. On the side you"
                  "find a fallen survivor. Theres nothing you can do for them now."
                  "You notice some ammo and food they carried")
            ammo+=2
            food+=2
            pause()
        elif Die2== 4:   # food
            print("You search the area, it doesnt seem like theres any zombies here. On the side you"
                  "find a fallen survivor. Theres nothing you can do for them now."
                  "You notice some food they carried")
            food+= 4
            pause()
        elif Die2== 5:  # food/zombie
            print("You find an area covered in bushes. It seems like its been abandoned for quite a while"
                  "You find 2 food at the door, you can try to find more food inside, but you dont know if something"
                  "is lurking inside or not, do you take the risk?")
            food+= 2
            pause()
        elif Die2== 6: # ammo for food trade
            Trade= "N"
            print ("You hear a noise and snap around, come face to face with another survivor. They show no interest"
                  " in joining you. They show no signs of hostility. In fact, they ask for some ammo, in exchange for food they have"
                  "Perhaps they have enough food and wish to fend off any zombies attacking them, do you accept? Y/N")
            while Trade== "N":
                Trade= input(f"Type Y/N only. You have {ammo} ammo and {food} food")
                if Trade== "N":
                    break
                elif Trade== "Y":
                    if ammo== 0:
                        print("You have run out of ammo")
                        break
                    else:
                        food+= 1
                        ammo-= 1
                        Trade== "N"


                        
    elif Die1== 5:                                                                                                  # nothing
        if Die2== 1 or Die2==3:
           print("You enter an opening, it seems like it'd be an perfect opportunity to rest."
                 "\n As you turn the corner, you notice that you were wrong, as a couple of "
                 "zombies emerge from behind the corner")
           pause()
        elif Die2==2:
            print("You find an area covered in bushes. It seems like its been abandoned for quite a while"
                  "You find 2 ammo at the door, you can try to find more ammo inside, but you dont know if something"
                  "is lurking inside or not, do you take the risk?")
            ammo+= 2
            pause()
        elif Die2== 4:  # food/zombie
            print("You find an area covered in bushes. It seems like its been abandoned for quite a while"
                  "You find 2 food at the door, you can try to find more food inside, but you dont know if something"
                  "is lurking inside or not, do you take the risk?")
            food+= 2
            pause()
        elif Die2== 5:
            print("You find a spot to shelter for the day. It seems you are safe here. You get a bit of rest")
            # health of each survivor increases by an additional 1
            pause()
        elif Die2== 6:
            print("You find a survivor, you're unable to read the stoic expression on their face. You attempt to"   # Recruit survivor
                  " talk to them...")
            Die1= Dice1()
            Die2= Dice2()
            if Die1%2==0 and Die2%2==0:
                print("They agree to join your team!")  # recruited
            elif Die1%2!=0 and Die2%2 !=0:                # fight
                print ("The survivor refuses to join you. Even worse, they decide to fight you for any supplies you may have!")
            else:
                print("The survivor apologies and states that they have other places to be and other people to protect. They wish you well and leave") #fail
            pause()
                
    elif Die1== 6:
        if Die2== 1 or Die2== 3:
            print("You have found a survivor, they have been ambushed by 2 zombies and are currently unprepared for this fight."
                "You must defeat these 2 zombies before the survivor becomes a zombie too")         
            Trade= ""
            print ("You hear a noise and snap around, come face to face with another survivor. They show no interest in joining you.\nThey show no signs of hostility. In fact, they beg for food, in exchange for ammo they have\nPerhaps theyre not a fighter and just wish to survive, making the ammo useless to them, do you accept? Y/N")
            while Trade!= "N" and Trade !="Y":
                Trade= input(f"Type Y/N only. You have {ammo} ammo and {food} food" ).upper()
                if Trade== "N":
                    pass
                elif Trade== "Y":
                    if food== 0:
                        print("You have run out of food")
                    else:
                        ammo+= 1
                        food-= 1
                        Trade= ""
        elif Die2== 4: # ammo for food trade
            Trade= ""
            print ("You hear a noise and snap around, come face to face with another survivor. They show no interest in joining you.\nThey show no signs of hostility. In fact, they beg for food, in exchange for ammo they have\nPerhaps theyre not a fighter and just wish to survive, making the ammo useless to them, do you accept? Y/N")
            while Trade!= "N" and Trade !="Y":
                Trade= input(f"Type Y/N only. You have {ammo} ammo and {food} food" ).upper()
                if Trade== "N":
                    pass
                elif Trade== "Y":
                    if food== 0:
                        print("You have run out of food")
                    else:
                        ammo+= 1
                        food-= 1
                        Trade= ""
        elif Die2== 5:           
            print("You find a survivor, you're unable to read the stoic expression on their face. You attempt to")   # Recruit survivor
            die1=Dice1()
            die2=Dice2()
            if die1%2==0 and die2 %2!=0:
                print("They agree to join your team!")
                Survivors.append("Chr"+str(Count))
                Count+= 1        
                                       
            elif Die1%2!=0 and Die2%2 !=0:              
                print ("The survivor refuses to join you. Even worse, they decide to fight you for any supplies you may have!")
            else:
                print("The survivor apologies and states that they have other places to be and other people to protect. They wish you well and leave") #fail
            pause()
        elif Die2== 6:
            Trader_Dog= True
            print("You find a survivor, you can either leave, trade them, or recruit them. Choose wisely:")
            Choice= 0
            while Choice>3 or Choice<1:
                try:
                    Choice= int(input("Type 1 for leave, 2 for trade, and 3 for recruit"))
                except ValueError:
                    try:
                        Choice= int(input("You did not enter a number, please enter a number otherwise nothing will happen this day: "))
                    except ValueError:
                        break
                if Choice== 1:
                    break
                elif Choice== 2:
                    Choice_Trade= 0
                    while Choice_Trade>3 or Choice_Trade<1:
                        Choice_Trade= int(input("What would you like to trade for? Enter 1 for ammo, 2 for food, 3 for dog: "))
                            
                        if Choice_Trade== 1:
                            Trade= "Y"
                            while Trade=="Y":
                                Trade= input(f"You have {ammo} ammo and {food} food. Would you like to trade? (Type only Y/N)")
                                if Trade== "N":
                                    break
                                if food== 0:
                                    print("You have run out of food")
                                    Choice= 0                                    
                                else:
                                    ammo+= 1
                                    food-= 1
                                    Choice= 0                                    
                        if Choice_Trade== 2:
                            Trade= "Y"
                            while Trade=="Y":
                                Trade= input(f"You have {ammo} ammo and {food} food. Would you like to trade? (Type only Y/N)")
                                if Trade== "N":
                                    break
                                if ammo== 0:
                                    print("You have run out of ammo")
                                    Choice= 0                    
                                else:
                                    food+= 1
                                    ammo-= 1
                                    Choice= 0
                        if Choice_Trade== 3:
                           if Trader_Dog== False or Dog== True:
                               print ("You already have a dog.")
                               Choice= 0                               
                           elif ammo<2 or food<1:
                               print("You have run out of food or ammo")
                               Choice= 0
                           else:
                               Choice_Dog=(input("The survivor offers his dog for 2 ammo and 1 food, type Y to accept, N to decline."))
                               if Choice_Dog== "Y":
                                   ammo-=2
                                   food-= 1
                                   Dog= True
                                   Trader_Dog= False
                                   Choice= 0
                               else:
                                   Choice= 0
                elif Choice== 3: # recruit
                    Survivors.append("Chr"+str(Count))  # so far adds another survivor to the list
                    Count+= 1  
    next_day()

def day():          # Chooses the event for the day / main game mechanics
    Events(Dog,Count)
    
def next_day():
    global Round
    if Round== 100:
        print("You win! Backup arrived and you managed to escape the infected town safely.")
    else:
        Round+= 1                   # proceeds to the next day
        print(f"Day {Round}")
        day()
setup()

def Fight():
    pass