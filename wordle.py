#!/usr/bin/env python

import os

def solve_wordle():

    wordleWords = five_letter_words();
    letterGroups = generate_letter_group_occurances();

    badGoodLetterPoses = [{""}, {""}, {""}, {""}, {""}]
    blacklist = {""}

    for turn in range(6):

        print("-------------------------------\nGuess {}".format(turn + 1))

        #
        #Get Input
        #
        while (True):
            guess = input("Enter Word Guess: ").strip().upper();
            if (validate_guess(guess)):
                break;
            print("\nEnter a 5 Letter guess; only Use Letters.\n")
            
        while (True):
            unknownPosition = input("Enter all Yellow Letters, Any Order (Leave empty if none): ");
            if (len(unknownPosition) < 5):
                break;

        while (True):
            knownOrder = input("Enter Guess Result (Use Letter if Green and ';' if Not): ");
            if (validate_order(knownOrder)):
                break;

            #Win / Exit Case
            if ';' not in knownOrder:
                print("Congradulations!");
                return 0

            #Error
            print("\nEnter a String 5 charachters long.\n\tExample: If the guess GHOST resulted\n\tno no correct positions, type ';;;;;'")




        #
        #
        #


        #Keep Track of Information
        #Save Set
        knownLetters = set(unknownPosition.upper() + knownOrder.replace(";", "").upper());
        
        #Add To Black List or List of places it cannot be
        for letter in guess:
            if letter not in knownLetters:
                blacklist.add(letter)

            else:

                #If good letter, but bad position (yellow letter)
                #don't include words with letters in these positions
                
                for pos in range(5):
                    if knownOrder[pos] == ';':
                        if guess[pos] == letter:
                            badGoodLetterPoses[pos].add(letter)



        #
        #
        #
        printList = []

        #Find Possible Words
        wordid = -1
        for word in wordleWords:

            #Increment
            wordid += 1
            if (word == ""):
                continue;

            #Check if All Letters Are Good For This Word
            badCase = False;

            #Check If Words Fail Previous Guess Checks
            for i in range(5):
                wordLetter = word[i].upper()
                
                if (wordLetter in blacklist) or (wordLetter in badGoodLetterPoses[i]):
                        badCase = True
                        #print("{} fails previous check".format(word))
                        break
            if (badCase):
                continue

            #Check If Confirmed Letters Exist
            for confirmedLetter in knownLetters:
                if confirmedLetter not in word:
                    #print("{} not in {}".format(confirmedLetter, word))
                    badCase = True
                    break
            if (badCase):
                wordleWords[wordid] = "";
                continue

            #Check if Confirmed Order Works With Letter
            for i in range(5):
                if not( word[i] == knownOrder.upper()[i] or knownOrder[i] == ';'):
                    badCase = True;
                    break
            if (badCase):
                wordleWords[wordid] = "";
                continue;

            #Pass All Checks? Add to List
            printList.append(word)


        #Print The Pretty List
        print_return_result(printList, letterGroups);


def five_letter_words():

    listt = [];
    
    #Open File; List Lines
    path = os.path.join(os.path.dirname(__file__), "words.txt");
    with open(path, 'r') as f:
        listt = [line.strip().upper() for line in f]

    return listt


def print_return_result(listOfValidWords, letterGroups):

    org = {}

    #Get Vals
    for word in listOfValidWords:
        org[word] = assign_goodness_value(word, letterGroups)

    #Sort List
    sortorg = sorted(org.items(), key=lambda x: x[1], reverse=True)

    #Print
    print("Suggested Next Guesses:\n")
    for i in range(min(len(sortorg), 10)):
        print("{}: {}".format(sortorg[i][0], round(100*sortorg[i][1])/100))
    
#Constant
def get_letter_probs():

    return {'A': 10.18, 'B': 2.44, 'C': 3.77, 'K': 1.71, 'F': 1.69,
            'T': 5.59, 'S': 7.14, 'E': 10.28, 'H': 2.91, 'Y': 2.65,
            'O': 6.73, 'D': 3.55, 'L': 5.65, 'M': 3.34, 'R': 6.95,
            'I': 6.46, 'U': 4.4, 'V': 1.37, 'N': 4.98, 'Z': 0.43,
            'G': 2.49, 'P': 2.94, 'X': 0.46, 'J': 0.41, 'W': 1.23, 'Q': 0.24}
    


#Probability
def assign_goodness_value(word, letterGroups):

    #Bad Word, Don't Reccoment
    if len(word) != 5:
        return 0

    #Grab
    letterProb = get_letter_probs();
    letterCount = {}

    #Get Sum Of Points
    totalSum = 0
    bonuses = 0
    highestLetterCount = 1

    vowelsUsed = []
    vowels = ['A', 'E', 'I', 'O', 'U', 'Y']

    #Check Each Letter
    for letter in word:
        totalSum += letterProb[letter];
        letterCount[letter] = letterCount.get(letter, 0) + 1

        if letterCount[letter] > highestLetterCount:
            highestLetterCount = letterCount[letter]

        #Add Vowel Letter, Dereward Multiple Different Vowels
        if letter in vowels and letter not in vowelsUsed:
            bonuses -= 1/8
            vowelsUsed.append(letter)

          
    #Check If Groups Of Letters Exist
    for i in range(5):
            for j in range(i, 6):
                sequence = word[i:j]

                if sequence in letterGroups:
                    bonuses += letterGroups[sequence]/20


    #Compile
    value = (totalSum * 5) / (highestLetterCount**0.5) + bonuses
    return value


def validate_guess(guess):

    for letter in guess:
        if not letter.isalpha():
            return False;

    if (len(guess) != 5):
        return False;

    return True;


def validate_order(order):

    for letter in order:
        if not (letter.isalpha() or letter == ';'):
            return False;

    if (len(order) != 5):
        return False;

    return True;

#Generates the above table from all chars in the file
def generate_letter_probs():

    words = five_letter_words();

    count = {}
    totalLetters = 0
    for word in words:
        for letter in word:
            count[letter] = count.get(letter, 0) + 1
            totalLetters += 1

    for letter in count:
        count[letter] = round(count[letter] / totalLetters * 10000) / 100

    return count


#Generates Above
def generate_letter_group_occurances():

    words = five_letter_words();

    count = {}
    
    for word in words:
        for i in range(5):
            for j in range(i, 6):
                sequence = word[i:j]

                if (len(sequence) >= 2 and len(sequence) <= 3):
                    count[sequence] = count.get(sequence, 0) + 1

    l = sorted(count.items(), key=lambda x: x[0], reverse=True)
    
    return commonish(l, 5)

def commonish(l, cutoff):

    l2 = {}

    for item in l:
        if item[1] >= cutoff:
            l2[item[0]] = item[1];

    return l2


#
#
#
#Run
if (__name__ == "__main__"):
    solve_wordle();    


