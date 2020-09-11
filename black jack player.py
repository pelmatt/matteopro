import numpy as np
import random





def cardvalue():    #This function will allow me to randomly 'pull' cards out of a 'deck'
    x = random.randint(1,52)
    if x >= 1 and x <= 4:
        value = 1
    elif x >=5 and x <= 8:
        value = 2
    elif x >=9 and x <= 12:
        value = 3
    elif x >=13 and x <= 16:
        value = 4
    elif x >=17 and x <= 20:
        value = 5
    elif x >=21 and x <= 24:
        value = 6
    elif x >=25 and x <= 28:
        value = 7
    elif x >=29 and x <= 32:
        value = 8
    elif x >=33 and x <= 36:
        value = 9
    elif x >=37 and x <= 52:
        value = 10
    return value

def playerTurn(dataMatrix, playerTotal, dealerTotal):    #This function will process the 'player turn' the only time the player has to make a choice
    choice = random.randint(1,2)
    repeat = False     #if hit is chosen, this will become true such that he gets to choose wether to hit or stick again
    if playerTotal > 21: #initial check if player is bust, if he is game ends
        dataMatrix[0].append(-1)
        dataMatrix[1].append(playerTotal)
        dataMatrix[2].append(dealerTotal)
    else:  
        if choice == 1:
            playerTotal += cardvalue()
            dataMatrix[0].append(1)
            dataMatrix[1].append(playerTotal)
            dataMatrix[2].append(dealerTotal)
            repeat = True
        elif choice == 2:
            dataMatrix[0].append(2)
            dataMatrix[1].append(playerTotal)
            dataMatrix[2].append(dealerTotal)
        
    if repeat == True:
        dataMatrix, playerTotal, dealerTotal = playerTurn(dataMatrix, playerTotal, dealerTotal)
        
    return dataMatrix, playerTotal, dealerTotal

def dealerTurn(dataMatrix, playerTotal, dealerTotal): #this function deals with the 'dealers turn' the player has no choice in what happens here.
    
    dealerPlay = True
    dealerTotal += cardvalue()
    
    
    while dealerPlay:
        if dealerTotal < 17: #the dealer will stop picking up cards once his total is over 17
            dealerTotal += cardvalue()
        else:
            dealerPlay = False
    if dealerTotal > 21: #check if dealer bust
        dataMatrix[0].append(1)
        dataMatrix[1].append(playerTotal)
        dataMatrix[2].append(dealerTotal)
    elif dealerTotal == playerTotal:  #apply win conditions
        dataMatrix[0].append(0)
        dataMatrix[1].append(playerTotal)
        dataMatrix[2].append(dealerTotal)
    elif dealerTotal > playerTotal:
        dataMatrix[0].append(-1)
        dataMatrix[1].append(playerTotal)
        dataMatrix[2].append(dealerTotal)
    elif dealerTotal < playerTotal:
        dataMatrix[0].append(1)
        dataMatrix[1].append(playerTotal)
        dataMatrix[2].append(dealerTotal)        
        
    return dataMatrix, playerTotal, dealerTotal

def playTheGame():   #this function will take all the above functions and 'play the game' processing first the players turn then the dealers turn
    dealerTotal = 0
    playerTotal = 0
    
    dataMatrix = (([],[],[]))  #each game is documented in a list of list which will later be converted to an array
    
    dealerTotal = cardvalue()
    playerTotal = cardvalue() + cardvalue()
    
    dataMatrix[0].append(0)
    dataMatrix[1].append(playerTotal)
    dataMatrix[2].append(dealerTotal)
    
    dataMatrix, playerTotal, dealerTotal = playerTurn(dataMatrix, playerTotal, dealerTotal)
    
    if playerTotal <= 21:
        dataMatrix, playerTotal, dealerTotal = dealerTurn(dataMatrix, playerTotal, dealerTotal)
    return dataMatrix

frame = []
#%%
counter = 0 
for x in range(0,5000000):    #repeat the game 5 million times and store each array in a list called frame
    frame.append(np.array(playTheGame()))
    counter += 1
    if counter/100000 == float(counter//100000):
        print(counter)

#%%
win = 0
lose = 0
passed = 0

for x in range(0,len(frame)):  #how many times did we win, lose or draw
    if frame[x][0][-1] == 1:
        win += 1
    elif frame[x][0][-1] == 0:
        passed += 1
    elif frame[x][0][-1] == -1:
        lose += 1

#%%

probwin = win/len(frame)     #what are my chances
problose = lose/len(frame)
probpassed = passed/len(frame)

#%%

def playHelper(iteration): #this function is designed such that if you wanted to use the above to help you, it will tell you what the best move to take is
    
    
    frame1 = []
    frame2 = []
    playerTotal = int(input('The total value of your cards:'))
    dealerTotal = int(input('The total value of dealer cards:'))
    
    
    for x in range(len(frame)):
        if frame[x][1][iteration] == playerTotal and frame[x][2][iteration] == dealerTotal:
            frame1.append(frame[x])
    
    for x in range(len(frame1)):
        if frame1[x][0][-1] == 1:
            frame2.append(frame1[x])
    
    hits = 0
    sticks = 0  
    for x in range(len(frame2)):
            if frame2[x][0][iteration + 1] == 1:
                hits += 1
            elif frame2[x][0][iteration + 1] == 2:
                sticks += 1
    print('Probability Hit win: ', hits/len(frame2))
    print('Probability Stick win: ', sticks/len(frame2))
    choice = int(input('did you stick or hit? 1 for stick 2 for hit: '))
    if choice == 2:
        iteration += 1  
        playHelper(iteration)
    
#playHelper(0)
    
#%%
winhitcounter = 0
for x in range(0,len(frame)): #I was curious as to how many times hitting led to a winning outcome: 460,000/1,400,000
    if frame[x][0][1] == 1 and frame[x][0][-1] == 1:
        winhitcounter += 1
    
#%%
def helptester(iteration, playerTotal, dealerTotal):   #This function would act as the above but is designed to talk to the computer and not humans, you can
    frame1 = []                                         #tell this by the lack of inputs
    frame2 = []
    
   
    
    for x in range(len(frame)):
        if frame[x][1][iteration] == playerTotal and frame[x][2][iteration] == dealerTotal:
            frame1.append(frame[x])
    
    for x in range(len(frame1)):
        if frame1[x][0][-1] == 1:
            frame2.append(frame1[x])
    
    hits = 0
    sticks = 0  
    for x in range(len(frame2)):
            if frame2[x][0][iteration + 1] == 1:
                hits += 1
            elif frame2[x][0][iteration + 1] == 2:
                sticks += 1
    choice = 0
    if hits/len(frame2) > sticks/len(frame2):
        choice = 1
    elif hits/len(frame2) < sticks/len(frame2):
        choice = 2

    return choice

def playtester():    #The equivalent of the 'playthegame' function however, instead of random choices being made, choices are made depending on the adivce of the helper
    dealerTotal = cardvalue()
    playerTotal = cardvalue() + cardvalue()
    choice = 0
    iteration = 0
    dataMatrix = (([],[],[]))
    dataMatrix[0].append(0)
    dataMatrix[1].append(playerTotal)
    dataMatrix[2].append(dealerTotal)
    
    repeat = True
    while repeat:
        
        choice = helptester(iteration, playerTotal, dealerTotal)
    
        if playerTotal > 21:
            dataMatrix[0].append(-1)
            dataMatrix[1].append(playerTotal)
            dataMatrix[2].append(dealerTotal)
            repeat = False
        else:  
            if choice == 1:
                iteration += 1
                playerTotal += cardvalue()
                dataMatrix[0].append(1)
                dataMatrix[1].append(playerTotal)
                dataMatrix[2].append(dealerTotal)
                repeat = True
            elif choice == 2:
                dataMatrix[0].append(2)
                dataMatrix[1].append(playerTotal)
                dataMatrix[2].append(dealerTotal)
                repeat = False
        
    if playerTotal <= 21:
      dataMatrix, playerTotal, dealerTotal = dealerTurn(dataMatrix, playerTotal, dealerTotal)
    return dataMatrix  

#%%
testframe = []
testcounter = 0

for x in range(0,1000):     #test the helper 1000 times
    try:
        testframe.append(np.array(playtester()))
        testcounter += 1
        print(testcounter)   
    except:
        pass
    
testwin = 0
testlose = 0
testpassed = 0

for x in range(0,len(testframe)):   #how many times did the ciomputer win or lose now?
    if testframe[x][0][-1] == 1:
        testwin += 1
    elif testframe[x][0][-1] == 0:
        testpassed += 1
    elif testframe[x][0][-1] == -1:
        testlose += 1   
    
#%%
testprobwin = testwin/len(testframe)   #what is are my new probabilities?
testproblose = testlose/len(testframe)
testprobpassed = testpassed/len(testframe)
    
    
    
    



