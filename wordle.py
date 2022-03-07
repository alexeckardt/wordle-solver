#!/usr/bin/env python

import os

def solve_wordle():

    wordleWords = five_letter_words();

    badGoodLetterPoses = [{""}, {""}, {""}, {""}, {""}]
    blacklist = {""}

    for turn in range(6):

        print("-------------------------------\nTurn {}".format(turn + 1))
        guess = input("Enter Word Guess: ").upper();
    
        knownOrder = input("Known Order (use ; for unknown order): ");

        if ';' not in knownOrder:
            print("Congradulations!");
            break

        unknownPosition = input("Known Letters (not order): ");

        knownLetters = set(unknownPosition.upper() + knownOrder.replace(";", "").upper());
        #print(knownLetters);


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


        #print("no letters in this pos: ", badGoodLetterPoses);
        #print("letters cannot use: ", blacklist);

        #
        printList = []

        wordid = -1
        for word in wordleWords:

            wordid += 1

            if (word == ""):
                continue;

            
            #print("{}:{}".format(word, wordid))


            #Check if All Letters Are Good For This Word
            badCase = False;


            #Check If Words Fail Previous Guess Checks
            for i in range(5):
                wordLetter = word[i].upper()

                #print(word)
                #print("\tChecking {} for pos {}".format(wordLetter, i))
                
                if (wordLetter in blacklist) or (wordLetter in badGoodLetterPoses[i]):
                        badCase = True
                        #print("{} fails previous check".format(word))
                        break


            if (badCase):
                continue

            #Check
            for confirmedLetter in knownLetters:
                if confirmedLetter not in word:
                    #print("{} not in {}".format(confirmedLetter, word))
                    badCase = True
                    break

            if (badCase):
                wordleWords[wordid] = "";
                continue

            for i in range(5):
                if not( word[i] == knownOrder.upper()[i] or knownOrder[i] == ';'):
                    badCase = True;
                    break

            if (badCase):
                wordleWords[wordid] = "";
                continue;    
            printList.append(word)

        #Print The Print List
        print_return_result(printList);

import os
def five_letter_words():

    path = os.path.join(os.path.dirname(__file__), "words.txt");
    listt = []
    
    with open(path, 'r') as f:
        listt = [line.strip() for line in f]

    return listt



def print_return_result(listOfValidWords):

    org = {}

    #Get Vals
    for word in listOfValidWords:
        org[word] = assign_goodness_value(word)

    #Org
    sortorg = sorted(org.items(), key=lambda x: x[1], reverse=True)

    print("Most Likley Words:\n")
    for i in range(min(len(sortorg), 10)):
        print(sortorg[i][0])
    

def get_letter_probs():

    return {'A': 10.18, 'B': 2.44, 'C': 3.77, 'K': 1.71, 'F': 1.69,
            'T': 5.59, 'S': 7.14, 'E': 10.28, 'H': 2.91, 'Y': 2.65,
            'O': 6.73, 'D': 3.55, 'L': 5.65, 'M': 3.34, 'R': 6.95,
            'I': 6.46, 'U': 4.4, 'V': 1.37, 'N': 4.98, 'Z': 0.43,
            'G': 2.49, 'P': 2.94, 'X': 0.46, 'J': 0.41, 'W': 1.23, 'Q': 0.24}
    

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

def assign_goodness_value(word):

    #Bad
    if len(word) != 5:
        return 0

    #Grab
    letterProb = get_letter_probs();
    letterCount = {}

    #Get Sum
    totalSum = 0
    highestLetterCount = 1
    for letter in word:
        totalSum += letterProb[letter];
        letterCount[letter] = letterCount.get(letter, 0) + 1

        if letterCount[letter] > highestLetterCount:
            highestLetterCount = letterCount[letter]

    #Compile
    value = (totalSum * 1.4) / (highestLetterCount**1.5)
    #print("{}: {}".format(word, value))
    return value

#Run
if (__name__ == "__main__"):
    solve_wordle();    

        
