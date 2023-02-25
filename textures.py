# Snake
snakeHead = """#000#463#463#6b3#6b3#6b3#6b3#6b3#463#463#000
#000#463#6b3#9d5#9d5#9d5#9d5#9d5#6b3#463#000
#000#6b3#9d5#9d5#9d5#9d5#9d5#9d5#9d5#6b3#000
#000#9d5#9d5#9d5#9d5#9d5#9d5#9d5#9d5#9d5#000
#000#9d5#fff#000#9d5#9d5#9d5#fff#000#9d5#000
#000#9d5#9d5#9d5#9d5#9d5#9d5#9d5#9d5#9d5#000
#000#000#fe3#9d5#6b3#9d5#6b3#9d5#fe3#000#000
#000#000#000#fe3#fe3#fe3#fe3#fe3#000#000#000
#000#000#000#000#000#e00#000#000#000#000#000
#000#000#000#000#e00#e00#e00#000#000#000#000
#000#000#000#000#e00#000#e00#000#000#000#000"""

snakeLine = """#000#000#000#9d5#9d5#9d5#9d5#9d5#000#000#000
#000#000#000#9d5#9d5#9d5#9d5#9d5#000#000#000
#000#000#000#9d5#9d5#9d5#9d5#9d5#000#000#000
#000#000#000#9d5#463#463#463#9d5#000#000#000
#000#000#000#463#223#223#223#463#000#000#000
#000#000#000#223#223#223#223#223#000#000#000
#000#000#000#223#6b3#6b3#6b3#223#000#000#000
#000#000#000#6b3#9d5#9d5#9d5#6b3#000#000#000
#000#000#000#9d5#9d5#9d5#9d5#9d5#000#000#000
#000#000#000#9d5#9d5#9d5#9d5#9d5#000#000#000
#000#000#000#9d5#9d5#9d5#9d5#9d5#000#000#000"""

snakeCorner = """#000#000#000#9d5#9d5#9d5#9d5#9d5#000#000#000
#000#000#000#9d5#9d5#9d5#9d5#463#000#000#000
#000#000#000#9d5#9d5#463#463#223#223#000#000
#000#000#000#9d5#463#223#223#223#6b3#9d5#9d5
#000#000#000#463#223#223#223#6b3#9d5#9d5#9d5
#000#000#000#223#223#223#6b3#9d5#9d5#9d5#9d5
#000#000#000#000#223#6b3#9d5#9d5#9d5#9d5#9d5
#000#000#000#000#000#9d5#9d5#9d5#9d5#9d5#9d5
#000#000#000#000#000#000#000#000#000#000#000
#000#000#000#000#000#000#000#000#000#000#000
#000#000#000#000#000#000#000#000#000#000#000"""

snakeTail = """#000#000#000#9d5#9d5#9d5#9d5#9d5#000#000#000
#000#000#000#6b3#9d5#9d5#9d5#6b3#000#000#000
#000#000#000#6b3#9d5#9d5#9d5#6b3#000#000#000
#000#000#000#000#6b3#9d5#6b3#000#000#000#000
#000#000#000#000#6b3#9d5#6b3#000#000#000#000
#000#000#000#000#000#6b3#000#000#000#000#000
#000#000#000#000#000#6b3#000#000#000#000#000
#000#000#000#000#000#000#000#000#000#000#000
#000#000#000#000#000#000#000#000#000#000#000
#000#000#000#000#000#000#000#000#000#000#000
#000#000#000#000#000#000#000#000#000#000#000"""

# Apple
apple = """#000#000#000#000#000#000#472#8d4#000#000#000
#000#000#c22#b22#000#6a3#6a3#8d4#c22#000#000
#000#d33#e55#e66#c22#6b3#7c4#d33#c22#d33#000
#000#d55#f77#e44#b22#b22#b22#d33#b22#b22#d33
#b22#e55#d33#b22#c22#b22#b22#b22#b22#b22#b22
#b22#b22#c22#c22#b22#b22#b22#b22#b22#b11#b22
#c22#b22#b22#b22#c22#b11#b22#b22#b22#b11#b22
#000#c22#c22#b11#b22#b11#b11#b11#b11#b11#b11
#000#b11#b22#c22#b11#b11#b11#b11#b11#b11#000
#000#000#b22#b11#b11#b11#b11#b11#b11#000#000
#000#000#000#b22#b11#000#b11#b11#000#000#000"""

gapple = """#000#000#000#fe3#000#000#472#8d4#000#000#000
#000#000#fe3#ff7#fe3#6a3#6a3#8d4#fd2#000#000
#000#fe7#fea#fe3#ffe#6b3#7c4#fd6#fd7#fe3#000
#000#fea#ffd#ffd#ffe#ffe#fec#fe9#fe3#ff7#fe3
#fd4#fe9#fea#ffd#ffd#ffd#fec#fe8#fd5#fe3#fd5
#fd6#fea#ffe#ffe#ffd#feb#feb#fd5#fd7#fd2#fd4
#fe8#fe9#ffd#fec#fe8#fe8#fd4#fd5#fd5#fd4#fd3
#000#fe8#fd2#fd7#fd7#fea#fe8#fd2#fd3#fd3#ec3
#000#fe3#fd6#fd4#fd5#fd7#fd3#fc3#fc2#fd2#000
#fe3#ff7#fe3#fd5#fd3#fd3#fc2#ec3#fc2#000#000
#000#fe3#000#fd4#fd2#000#fc1#fd3#000#000#000"""

toxicApple = """#000#000#000#000#000#000#323#343#000#000#000
#000#000#000#000#000#453#453#683#a7b#000#000
#000#000#000#000#546#343#a8b#656#97a#a7b#000
#000#000#000#000#333#546#222#656#545#869#747
#000#000#000#213#111#435#222#111#435#869#425
#000#000#213#111#111#545#222#222#324#647#424
#313#213#a8b#667#556#435#424#324#424#647#869
#000#a7b#a8b#a7b#435#859#859#424#758#758#536
#212#869#869#868#647#424#425#637#868#536#000
#000#000#748#868#868#868#868#868#868#000#000
#000#212#000#536#536#000#536#757#000#000#000"""
