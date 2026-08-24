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
current_level = 0 #current level of the game
current_points = 0 #current number of points made during gameplay
current_attempts = 5 #current number of available attempts to have
incorrect_count = 0 #counts the number of incorrect guesses during gameplay
pic_index = -1 #index used to make the picture in the gameplay

#pictures that will be used in the gameplay
word_list = [
        #easy levels
        "worry", "security", "coffee", "piano", "hold", "drop", "pack", "misty",
        "two", "factory",

        #hard levels
        "article", "defeat", "storage", "hall", "solution", "chilly", "tasty",
        "ready", "afraid", "adoption"
]

#name of the actual pictures that will be imported in the gameplay
gif_list = [
        #easy levels
        "concern.gif", "security.gif", "coffee.gif", "piano.gif", "hold.gif",
        "drop.gif", "pack.gif", "misty.gif", "two.gif", "factory.gif",

        #hard levels
        "article.gif", "defeat.gif", "storage.gif", "hall.gif", "solution.gif",
        "chilly.gif", "tasty.gif", "ready.gif", "afraid.gif", "adoption.gif",

        #other
        "titlepage.gif", "goodending.gif", "badending.gif"
]

used_pics = [] #stores the index of the gif and word items to create the picture in the gameplay

#returns a random index from the word_list array based on the game level
def get_index_for_picture(level: int):
    if level <= 5:
        index = random.randint(0, 9)    #gets an easy level
    else:
        index = random.randint(10, 19)    #gets a hard level

    return index

#gets a random word_list array index based on the game level
def get_pic_index(level: int):
    #picks an index
    index = get_index_for_picture(level)

    #gets another index if the index is already used
    while index in used_pics:
        index = get_index_for_picture(level)

    #adds an new index to the used_pics array
    used_pics.append(index)        
        
    return index

#manipulate the current points
def manipulate_points(correct_guess: bool,
                      level: int,
                      num_of_attempts: int,
                      points: int = 0
                      ):
    #calculate the additional points when on the hard levels
    additional_points = 0
    if level > 5:
        additional_points = num_of_attempts - 1

    #manipulates the points
    if correct_guess:    #if the guess is correct answer (or 1)
        match num_of_attempts:
            case 5:
                points += 5 + additional_points
            case 4:
                points += 4 + additional_points
            case 3:
                points += 3 + additional_points
            case 2:
                points += 2 + additional_points
            case 1:
                points += 1 + additional_points

    else:             #if the guess is incorrect answer (or otherwise)
        if points > 0:
            points -= 1
    
    return points

#creates the first hint
def create_first_hint(word: str):
    hint = word[0] + " _" * (len(word) - 1)

    return hint

#checks if the next hint could be made
def valid_next_hint(hint):
    num_of_blank = hint.count("_")

    return num_of_blank > 1
    
#creates the next hints after the first hint
def create_next_hint(word: str, old_hint: str):
    #returns old hint if making the next hint is invalid
    if not valid_next_hint(old_hint):
        return old_hint

    #gets the index that will replace the blank space
    hint_length = len(old_hint)

    replace_index = random.randint(2, hint_length - 1)
    while old_hint[replace_index] != '_':
        replace_index = random.randint(2, hint_length - 1)

    #get the letter of the word belonging to the hint
    letter_index = int(replace_index / 2)
    letter = word[letter_index]

    #creates the next hint
    next_hint = old_hint[:replace_index] + letter + old_hint[replace_index + 1:]

    return next_hint

#shows the constant components of the game round gui
def show_constant_game_round_gui():
    app.setLabel("message", "Guess a word from the pictures")

    app.showEntry("word")
    app.setFocus("word")

    app.hideButton("Play")
    app.hideButton("Exit")
    app.showButton("Guess")
    app.showButton("Skip")
    app.disableButton("Skip")

    app.showLabel("pointsattempts")

#sets the pointsattempts label
def set_pointattempts_label(points: int,
                            num_of_attempts: int
                            ):
    app.setLabel("pointsattempts", "Points: " + str(points) + "        " + "Attempts: " + str(num_of_attempts))
    
#sets the pointsattempts label
def set_hint_label(hint_txt: str):
    app.setLabel("hint", "Hint: " + hint_txt)
    
#sets the constant components of the game round gui
def set_inconstant_game_round_gui(level: int,
                       picture_index: int,
                       points: int,
                       num_of_attempts: int
                       ):
    app.setLabel("heading", "Level " + str(level))

    app.setImage("pic", gif_list[picture_index])

    app.hideLabel("hint")

    app.clearEntry("word")

    set_pointattempts_label(points, num_of_attempts)

#shows the end of the game
def show_end_of_game_gui(level: int,
                         points: int,
                         num_of_incorrects: int,
                         ):
    app.setLabel("message", "You got " + str(points) + "/70 points with " + str(num_of_incorrects) + "/40 mistakes.")

    app.hideEntry("word")

    app.hideLabel("pointsattempts")

    app.hideButton("Guess")
    app.hideButton("Skip")                
    app.showButton("Play")
    app.showButton("Exit")
    app.setButton("Play", "Play again?")

    if level >= 11:
        app.setLabel("heading", "You made it to the finish line!")

        app.showLabel("hint")
        if num_of_incorrects > 30:
            app.setLabel("hint", "(Pretty bad with so much incorrects.)")
        elif num_of_incorrects in range(11,30):
            app.setLabel("hint", "(Good job.)")
        elif num_of_incorrects in range(6,10):
            app.setLabel("hint", "(Closer to perfect.)")
        elif num_of_incorrects in range(1,5):
            app.setLabel("hint", "(Nearly aced it!)")
        else:
            app.setLabel("hint", "(WOW! That's a perfect score!)")

        app.setImage("pic", "goodending.gif")

        app.infoBox("ending", "!!! YOU GOT VICTORY !!!")
    else:
        app.setLabel("heading", "Too bad. You ran out of attempts.")
        app.hideLabel("hint")
        app.setImage("pic", "badending.gif")

        app.infoBox("ending", "YOU FAIL")

#behaviour of the buttons
def press(button):
    global current_level
    global current_points
    global current_attempts
    global incorrect_count
    global word_list
    global hint
    global pic_index

    #when player start or restart game
    if button == "Play":
        #sets game variables
        current_level = 1
        current_points = 0
        current_attempts = 5
        incorrect_count = 0
        pic_index = get_pic_index(current_level)

        #sets game gui
        show_constant_game_round_gui()
        set_inconstant_game_round_gui(current_level,
                                    pic_index,
                                    current_points,
                                    current_attempts
                                    )

    #when players guess a word
    elif button == "Guess":
        user = app.getEntry("word")
        
        if user == "": 
            app.setFocus("word") #refocuses on the entry when the word entered is empty
        else:
            #when the player guesses correctly
            if user.lower() == word_list[pic_index]:
                current_points = manipulate_points(True,
                                                   current_level,
                                                   current_attempts,
                                                   current_points
                                                   )
                current_attempts = 5 #resets the current available attempts

                #display an info box for correct guesses
                app.infoBox("answer", "CORRECT!")

                #increases the level
                current_level += 1

                pic_index = get_pic_index(current_level)

                #next level of the game gui
                set_inconstant_game_round_gui(current_level,
                                            pic_index,
                                            current_points,
                                            current_attempts
                                            )

            #when the player guesses incorrectly
            else:
                #display an info box for incorrect guesses
                app.infoBox("answer", "INCORRECT.")

                #perform consequences of incorrect guesses
                current_points = manipulate_points(False,
                                                   current_level,
                                                   current_attempts,
                                                   current_points
                                                   )
                current_attempts -= 1
                incorrect_count += 1

                #updates the game gui after incorrect guesses
                app.clearEntry("word")
                set_pointattempts_label(current_points, current_attempts)
                
            #displays the hint when the current available attempts are 3 and below
            if current_attempts <= 3:
                if current_attempts == 3:
                    hint = create_first_hint(word_list[pic_index])
                    
                    app.showLabel("hint")
                elif current_attempts == 2:
                    hint = create_next_hint(word_list[pic_index], hint)
                elif current_attempts == 1:
                    for i in range(2):
                        hint = create_next_hint(word_list[pic_index], hint)
                        
                set_hint_label(hint)

            #when the player reaches the end of the game 
            if current_level == 11 or current_attempts == 0:
                used_pics.clear() #clears the used_pics array

                #displays the end game gui
                show_end_of_game_gui(current_level,
                                     current_points,
                                     incorrect_count
                                     )

    #when player wants to exit the game
    elif button == "Exit":
        app.stop()

#sets up the gui app for the game
app = gui("4 pics 1 word", "615x615") #size and title of the app
app.setFont(12) #font size
app.setImageLocation("gif") #locates the image folder

#adds the content of the gui
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

app.addLabel("pointsattempts", "Points and attempts unavailable")
app.hideLabel("pointsattempts")

#executes the games
app.go()
