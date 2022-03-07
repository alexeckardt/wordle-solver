
import os
import probability

def solve_wordle():

    wordleWords = five_letter_words();

    badGoodLetterPoses = [{""}, {""}, {""}, {""}, {""}]
    blacklist = {""}

    for turn in range(6):

        print("-------------------------------\nTurn {} Guess:".format(turn))
        guess = input().upper();
    
        print("Known Order (use ; for unknown order): ")
        knownOrder = input();

        if ';' not in knownOrder:
            print("Congradulations!");
            break

        print("Known Letters (not order): ")
        unknownPosition = input();

        knownLetters = set(unknownPosition.upper() + knownOrder.replace(";", "").upper());
        print(knownLetters);


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


        print("no letters in this pos: ", badGoodLetterPoses);
        print("letters cannot use: ", blacklist);

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

    path = os.path.dirname(__file__) + "\\words.txt";
    listt = []
    
    with open(path, 'r') as f:
        listt = [line.strip() for line in f]

    return listt



def print_return_result(listOfValidWords):

    org = {}

    #Get Vals
    for word in listOfValidWords:
        org[word] = probability.assign_goodness_value(word)

    #Org
    sortorg = sorted(org.items(), key=lambda x: x[1], reverse=True)

    print("Most Likley Words:\n")
    for i in range(min(len(sortorg), 10)):
        print(sortorg[i][0])
    


    
        
