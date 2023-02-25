import playerSnake


class classement():
    highscore = []

    def __init__(self):

        file = open("score")
        highscore = file.read().split(";")
        pass

    def addHighScore(self):
        arr = self.highscore
        n = len(arr)
        for i in range(n):
            # Last i elements are already sorted
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    # Swap adjacent elements if they are in the wrong order
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                if len(arr) > 5:
                    arr.pop(5)

        file = open("score", "w")
        for score in self.highscore:
            file.write(score)
            file.write(";")
            
