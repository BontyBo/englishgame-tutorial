# hangman/views.py
from django.shortcuts import render
from .models import wordBank

def index(request):
    word = None
    message = ''
    attemp = 3
    Guessed = ""
    if request.method == "POST":
        word = request.POST.get("word")
        guessCharacter = request.POST.get("guess").lower()
        Guessed = request.POST.get("Guessed")
        # print('ppppppppppp',Guessed)
        attemp = int(request.POST.get("attemp"))
        wordDisplay = request.POST.get("word-display")
        message = request.POST.get("message")

    
        if guessCharacter in Guessed:
            message = "you already guess this character"
        elif guessCharacter in word:
            Guessed += guessCharacter
            message = ''
        else:
            attemp -= 1
            Guessed += guessCharacter
            message = "Incorrect guess!"
        
        if attemp <= 0:
            message = f"Game Over! The word was: {word}"

        # print("QQQQQQQQQQQQQQQQQq",' '.join(list(Guessed)))
    if not word:
        word = getRandomWord()
    wordDisplay = processWordDisplay(word, Guessed)
    
    if wordDisplay.split(' ') == list(word):
        message = "Congratulations! You won!"
    return render(request,"hangman/game.html", {"word":word,
                                                "wordDisplay":wordDisplay,
                                                "Guessed": Guessed,
                                                "attemp": attemp,
                                                "message": message})


def getRandomWord(setWordForTest=None):
    if setWordForTest:
        word = wordBank.objects.filter(word=setWordForTest).first() 
    else:
        word = wordBank.objects.order_by("?").first() 

    return word.word

def processWordDisplay(word, guessedChar):
    if type(word) != str:
        print("word type is not string")
        raise TypeError("word type is not string")
    if type(guessedChar) != str:
        print("guessed character type is not string")
        raise TypeError("guessed character type is not string")
    temp = []
    word = word.lower()
    guessedChar  = guessedChar.lower()
    for char in word:
        if char in guessedChar:
            temp.append(char)
        else:
            temp.append("_")
    # print(">>>>>>",temp,word,guessedChar)
    return ' '.join(temp)