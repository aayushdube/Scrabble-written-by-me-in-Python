# Scrabble-written-by-me-in-Python
#Function for scoring individual words
def getWordScore(word, n):
    """
    Returns the score for a word. Assumes the word is a valid word.

    The score for a word is the sum of the points for letters in the
    word, multiplied by the length of the word, PLUS 50 points if all n
    letters are used on the first turn.

    Letters are scored as in Scrabble; A is worth 1, B is worth 3, C is
    worth 3, D is worth 2, E is worth 1, and so on (see SCRABBLE_LETTER_VALUES)

    word: string (lowercase letters)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    returns: int >= 0
    """
    wordScore=0
    actualScore=0
    if word=='':
        return 0
    elif len(word)==n:
        for i in word:
            wordScore=wordScore+SCRABBLE_LETTER_VALUES[i]
        actualScore=(wordScore*len(word))+50
        return actualScore
    else:
        for i in word:
            wordScore=wordScore+SCRABBLE_LETTER_VALUES[i]
        actualScore=wordScore*len(word)
        return actualScore
    
    #Function for dealing with individual hands
    def updateHand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    newHand=hand.copy()
    for i in word:
        if hand.get(i,0)!=0:
            newHand[i]-=1
    return newHand
    
    #Function for checking valid words
    def isValidWord(word, hand, wordList):
    """
    Returns True if word is in the wordList and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or wordList.
   
    word: string
    hand: dictionary (string -> int)
    wordList: list of lowercase strings
    """
    newHand=hand.copy()
    if word in wordList:
        for letter in word:
            if letter in newHand.keys():
                newHand[letter]-=1
                if -1 in newHand.values():
                    return False
            else:
                return False
        if 0 in newHand.keys():
            return False
        else:
            return True
    else:
        return False

#Function for calculating hand length

def calculateHandlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    count=0
    for i in hand.keys():
        for j in range(0,hand[i]):
            count+=1
    return count

#Function for playing individual hands
def playHand(hand, wordList, n):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    * The user may input a word or a single period (the string ".") 
      to indicate they're done playing
    * Invalid words are rejected, and a message is displayed asking
      the user to choose another word until they enter a valid word or "."
    * When a valid word is entered, it uses up letters from the hand.
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when there are no more unused letters or the user
      inputs a "."

      hand: dictionary (string -> int)
      wordList: list of lowercase strings
      n: integer (HAND_SIZE; i.e., hand size required for additional points)
      
    """
    points=0
    input1=''
    while calculateHandlen(hand)!=0:
        s=''
        for letter in hand.keys():
            for j in range(hand[letter]):
                s+=letter
        print 'Current Hand: ' + s
        input1=raw_input('Enter word, or a "." to indicate that you are finished: ')
        if input1=='.':
            break
        if isValidWord(input1, hand, wordList)==True:
            wordScore=getWordScore(input1, n)
            hand=updateHand(hand, input1)
            points+=wordScore
            print '"'+input1+'"'+' earned ' + str(wordScore)+' points.'+'Total: '+str(points)
        else:
            print 'Invalid word, please try again.'
    print 'Goodbye!'+' Total score: '+str(points)+' points.'
    
    #Function for playing a game
    def playGame(wordList):
    """
    Allow the user to play an arbitrary number of hands.
 
    1) Asks the user to input 'n' or 'r' or 'e'.
      * If the user inputs 'n', let the user play a new (random) hand.
      * If the user inputs 'r', let the user play the last hand again.
      * If the user inputs 'e', exit the game.
      * If the user inputs anything else, tell them their input was invalid.
 
    2) When done playing the hand, repeat from step 1
    """
    input1=''
    hand={}
    while input1!='e':
        input1=raw_input('Enter n to deal a new hand, r to replay the last hand, or e to end game: ')
        if input1=='r' and hand=={}:
            print 'You have not played a hand yet. Please play a new hand first!'
        elif input1=='r':
            playHand(hand,wordList,HAND_SIZE)
        elif input1=='n':
            hand=dealHand(HAND_SIZE)
            playHand(hand,wordList,HAND_SIZE)
        elif input1=='e':
            break
        else:
            print 'Invalidcommand'

#Randomization by making computer pick the word
def compChooseWord(hand, wordList, n):
    """
    Given a hand and a wordList, find the word that gives 
    the maximum value score, and return it.

    This word should be calculated by considering all the words
    in the wordList.

    If no words in the wordList can be made from the hand, return None.

    hand: dictionary (string -> int)
    wordList: list (string)
    returns: string or None
    """
    def wordPossible(word, hand):
    
        newHand=hand.copy()
        for letter in word:
            if letter in newHand.keys():
                newHand[letter]-=1
                if -1 in newHand.values():
                    return False
            else:
                return False
        if 0 in newHand.keys():
            return False
        else:
            return True
    maxScore=0
    bestWord=''
    for i in wordList:
        if wordPossible(i, hand)==True and getWordScore(i,n)>maxScore:
            maxScore=getWordScore(i,n)
            bestWord=i
    if bestWord=='':
        return None
    else:
        return bestWord

#Computer playing the game against itself
def compChooseWord(hand, wordList, n):
    """
    Given a hand and a wordList, find the word that gives 
    the maximum value score, and return it.

    This word should be calculated by considering all the words
    in the wordList.

    If no words in the wordList can be made from the hand, return None.

    hand: dictionary (string -> int)
    wordList: list (string)
    returns: string or None
    """
    def wordPossible(word, hand):
    
        newHand=hand.copy()
        for letter in word:
            if letter in newHand.keys():
                newHand[letter]-=1
                if -1 in newHand.values():
                    return False
            else:
                return False
        if 0 in newHand.keys():
            return False
        else:
            return True
    maxScore=0
    bestWord=''
    for i in wordList:
        if wordPossible(i, hand)==True and getWordScore(i,n)>maxScore:
            maxScore=getWordScore(i,n)
            bestWord=i
    if bestWord=='':
        return None
    else:
        return bestWord

def compPlayHand(hand, wordList, n):
    """
    Allows the computer to play the given hand, following the same procedure
    as playHand, except instead of the user choosing a word, the computer 
    chooses it.

    1) The hand is displayed.
    2) The computer chooses a word.
    3) After every valid word: the word and the score for that word is 
    displayed, the remaining letters in the hand are displayed, and the 
    computer chooses another word.
    4)  The sum of the word scores is displayed when the hand finishes.
    5)  The hand finishes when the computer has exhausted its possible
    choices (i.e. compChooseWord returns None).
 
    hand: dictionary (string -> int)
    wordList: list (string)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    """
    points=0
    input1=''
    while calculateHandlen(hand)!=0:
        s=''
        for letter in hand.keys():
            for j in range(hand[letter]):
                s+=letter
        print 'Current Hand: ' + s
        input1=compChooseWord(hand, wordList, n)
        if input1==None:
            break
        if isValidWord(input1, hand, wordList)==True:
            wordScore=getWordScore(input1, n)
            hand=updateHand(hand, input1)
            points+=wordScore
            print '"'+input1+'"'+' earned ' + str(wordScore)+' points.'+'Total: '+str(points)
        else:
            print 'Invalid word, please try again.'
    print 'Goodbye!'+' Total score: '+str(points)+' points.'
    
    #Final Game Function
    
    def playGame(wordList):
    """
    Allow the user to play an arbitrary number of hands.
 
    1) Asks the user to input 'n' or 'r' or 'e'.
        * If the user inputs 'e', immediately exit the game.
        * If the user inputs anything that's not 'n', 'r', or 'e', keep asking them again.

    2) Asks the user to input a 'u' or a 'c'.
        * If the user inputs anything that's not 'c' or 'u', keep asking them again.

    3) Switch functionality based on the above choices:
        * If the user inputted 'n', play a new (random) hand.
        * Else, if the user inputted 'r', play the last hand again.
          But if no hand was played, output "You have not played a hand yet. 
          Please play a new hand first!"
        
        * If the user inputted 'u', let the user play the game
          with the selected hand, using playHand.
        * If the user inputted 'c', let the computer play the 
          game with the selected hand, using compPlayHand.

    4) After the computer or user has played the hand, repeat from step 1

    wordList: list (string)
    """  
    input1=''
    input2=''
    hand={}
    while input1!='e':
        input1=raw_input('Enter n to deal a new hand, r to replay the last hand, or e to end game: ')
        if input1=='r' and hand=={}:
            print 'You have not played a hand yet. Please play a new hand first!'
        elif input1=='r':
            while True:
                input2=raw_input('Enter u to have yourself play, c to have the computer play: ')
                if input2=='u':
                    playHand(hand,wordList,HAND_SIZE)
                    break
                elif input2=='c':
                    compPlayHand(hand,wordList,HAND_SIZE)
                    break
                else:
                    print 'Invalid command'
        elif input1=='n':
            while True:
                input2=raw_input('Enter u to have yourself play, c to have the computer play: ')
                if input2=='u':
                    hand=dealHand(HAND_SIZE)
                    playHand(hand,wordList,HAND_SIZE)
                    break
                elif input2=='c':
                    hand=dealHand(HAND_SIZE)
                    compPlayHand(hand,wordList,HAND_SIZE)
                    break
                else:
                    print' Invalid command'
        elif input1=='e':
            break
        else:
            print 'Invalidcommand'
        
