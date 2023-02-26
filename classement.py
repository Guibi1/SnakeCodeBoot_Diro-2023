highscore = []


def loadHighScores():
    global highscore

    file = open("score")
    for score in file.read().split(";"):
        if (len(score) > 0):
            highscore.append(int(score))


def addHighScore(score):
    global highscore
    if score == 0:
        return

    highscore.append(score)

    n = len(highscore)
    for i in range(n):
        # Last i elements are already sorted
        for j in range(0, n-i-1):
            if highscore[j] > highscore[j+1]:
                # Swap adjacent elements if they are in the wrong order
                highscore[j], highscore[j+1] = highscore[j+1], highscore[j]
    if len(highscore) > 5:
        highscore.pop(5)

    file = open("score", "w")
    for score in highscore:
        file.write(str(score))
        file.write(";")

    file.close()


loadHighScores()
