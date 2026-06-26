from appJar import gui
import random
### DUE FRIDAY 1ST APRIL ###

'''The puzzle game is “4 pics 1 word”,  which contains four pictures that have
something in common. Your task is to re-create this game using Python and
appJar.'''

### GAME REQUIREMENTS ###

'''
- max 10 levels, which gets harder to guess
- points allocated for each correct guess and appropriate level of difficulty 
- points deducted for each incorrect guess, it cannot have a negative score
- max five guess per set of images
- hint provided on 3rd attempt
- no skip level until correct input
- images must be .gif format
'''

### WORK ###
level = 0
points = 0
attempts = 5
wrongs = 0

pics = ["worry", "security", "coffee", "piano", "hold", "drop", "pack",
        "misty", "two", "factory", "article", "defeat", "storage", "hall",
        "solution", "chilly", "tasty", "ready", "afraid", "adoption"]
gifs = ["concern.gif", "security.gif", "coffee.gif", "piano.gif", "hold.gif",
        "drop.gif", "pack.gif", "misty.gif", "two.gif", "factory.gif",
        "article.gif", "defeat.gif", "storage.gif", "hall.gif", "solution.gif",
        "chilly.gif", "tasty.gif", "ready.gif", "afraid.gif", "adoption.gif",
        "titlepage.gif", "goodending.gif", "badending.gif"]
used = []

def chooser(level):
    if level <= 5:
        num = random.randint(0, 9)    # level easy
    else:
        num = random.randint(10, 19)    # level hard

    while num in used:
        if level <= 5:
            num = random.randint(0, 9)
        else:
            num = random.randint(10, 19)

    used.append(num)        
        
    return num

def pointer(level, guess, tempts, tally):
    if guess == 1:    # correct answers
        if level <= 5:
            if tempts == 5:
                tally += 5
            elif tempts == 4:
                tally += 4
            elif tempts == 3:
                tally += 3
            elif tempts == 2:
                tally += 2
            elif tempts == 1:
                tally += 1
        else:
            if tempts == 5:
                tally += 9
            elif tempts == 4:
                tally += 7
            elif tempts == 3:
                tally += 5
            elif tempts == 2:
                tally += 3
            elif tempts == 1:
                tally += 1

    else:             # incorrect answers
        if tally == 0:
            tally = 0
        else:
            tally -= 1
    
    return tally

def hinter():
    space = []
    space2 = []
    space3 = []
    
    clue = ""

    for i in range(len(pics)):
        clue = pics[i][0] + " _" * (len(pics[i]) - 1)
        space.append(clue)
        
        clue2 = pics[i][0]
        
        letter = random.randint(1, (len(pics[i]) - 1))
        
        for x in range(len(pics[i])):
            if len(pics[i]) < 4:
                clue2 = space[i]
            elif x == 0:
                pass
            elif x == letter:
                clue2 += " " + pics[i][letter]
            else:
                clue2 += " _"

        space2.append(clue2)

        clue3 = pics[i][0]

        letter2 = random.randint(1, (len(pics[i]) - 1))
        while letter2 == letter:
            letter2 = random.randint(1, (len(pics[i]) - 1))

        letter3 = random.randint(1, (len(pics[i]) - 1))
        breaker = 0    # prevent repeat of len(two)
        while letter3 == letter or letter3 == letter2:
            letter3 = random.randint(1, (len(pics[i]) - 1))
            breaker += 1

            if breaker == 5:
                break
        breaker = 0

        for x in range(len(pics[i])):
            if len(pics[i]) < 5:
                clue3 = space2[i]
            elif x == 0:
                pass
            elif x == letter:
                clue3 += " " + pics[i][letter]
            elif x == letter2:
                clue3 += " " + pics[i][letter2]
            elif x == letter3 and len(pics[i]) > 5:
                clue3 += " " + pics[i][letter3]
            else:
                clue3 += " _"
                    
        space3.append(clue3)
    
    return space, space2, space3

def press(button):
    global level
    global points
    global attempts
    global wrongs
    global pics
    global hint
    global num
    
    if button == "Play":     # start/restart
        hint = hinter()
        level = 1
        points = 0
        attempts = 5
        wrongs = 0
        num = chooser(level)
        
        app.setLabel("heading", "Level " + str(level))
        app.setLabel("message", "Guess a word from the pictures")

        app.setImage("pic", gifs[num])

        app.hideLabel("hint")
        
        app.showEntry("word")
        app.setFocus("word")
        
        app.hideButton("Play")
        app.hideButton("Exit")
        app.showButton("Guess")
        app.showButton("Skip")
        app.disableButton("Skip")

        app.showLabel("pointsattempts")
        app.setLabel("pointsattempts", "Points: " + str(points) + "           " + "Attempts: " + str(attempts))
        
    elif button == "Guess":     # user arena
        user = app.getEntry("word")
        
        if user == "":
            app.setFocus("word")
        else:
            if user.lower() == pics[num]:
                points = pointer(level, 1, attempts, points)
                attempts = 5
                
                app.infoBox("answer", "CORRECT!")
                
                level += 1

                num = chooser(level)
                
                app.setLabel("heading", "Level " + str(level))
                
                app.setImage("pic", gifs[num])

                app.hideLabel("hint")

                app.clearEntry("word")
                
                app.setLabel("pointsattempts", "Points: " + str(points) + "        " + "Attempts: " + str(attempts))
                
            else:
                app.infoBox("answer", "INCORRECT.")

                points = pointer(level, 0, attempts, points)
                attempts -= 1
                wrongs += 1

                app.clearEntry("word")
                
                app.setLabel("pointsattempts", "Points: " + str(points) + "        " + "Attempts: " + str(attempts))

            if attempts == 3:                
                app.showLabel("hint")
                app.setLabel("hint", "Hint: " + hint[0][num])
            elif attempts == 2:
                app.setLabel("hint", "Hint: " + hint[1][num])
            else:
                app.setLabel("hint", "Hint: " + hint[2][num])
                
            if level == 11 or attempts == 0:    # end game 
                used.clear()

                app.setLabel("message", "You got " + str(points) + "/70 points with " + str(wrongs) + "/40 mistakes.")

                app.showLabel("hint")
                if wrongs > 30:
                    app.setLabel("hint", "(Pretty bad with so much incorrects.)")
                elif wrongs in range(11,30):
                    app.setLabel("hint", "(Good job.)")
                elif wrongs in range(6,10):
                    app.setLabel("hint", "(Closer to perfect.)")
                elif wrongs in range(1,5):
                    app.setLabel("hint", "(Nearly aced it!)")
                else:
                    app.setLabel("hint", "(WOW! That's a perfect score!)")

                app.hideEntry("word")

                app.hideLabel("pointsattempts")
                
                app.hideButton("Guess")
                app.hideButton("Skip")                
                app.showButton("Play")
                app.showButton("Exit")
                app.setButton("Play", "Play again?")

                if level == 11:
                    app.setLabel("heading", "You made it to the finish line!")
                    app.setImage("pic", "goodending.gif")
                    app.infoBox("ending", "!!! YOU GOT VICTORY !!!")
                else:
                    app.setLabel("heading", "Too bad. You ran out of attempts.")
                    app.setImage("pic", "badending.gif")
                    app.infoBox("ending", "YOU FAIL")
                
    elif button == "Exit":
        app.stop()
        
app = gui("4 pics 1 word", "615x615")
app.setFont(12)
app.setImageLocation("gif")

app.addLabel("heading", "Welcome to the 4 pics 1 word game!")
app.addLabel("message", """This game has 10 levels where you cannot skip.
You will be given 5 attempts if you made a mistake.""")

app.addImage("pic", "titlepage.gif")

app.addLabel("hint", "BY: ABBY C 11")

app.addEntry("word")
app.hideEntry("word")

app.addButtons(["Play", "Exit"], press)
app.addButtons(["Guess", "Skip"], press)
app.hideButton("Guess")
app.hideButton("Skip")

app.addLabel("pointsattempts", "Points: " + str(points) + "           " + "Attempts: " + str(attempts))
app.hideLabel("pointsattempts")

app.go()
