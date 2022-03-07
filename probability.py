import wordle


def get_letter_probs():
    words = wordle.five_letter_words();

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
    
     
    
