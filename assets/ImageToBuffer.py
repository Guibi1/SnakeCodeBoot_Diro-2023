from PIL import Image
from numpy import asarray

bgFileName = "assets/Grass.png"
fileName = "assets/SnakeTail.png"


def colorToStr(color):
    return "#"+hex(round(color[0] / 255 * 15))[2] + hex(
        round(color[1] / 255 * 15))[2] + hex(round(color[2] / 255 * 15))[2]


def convert(angle: int):
    # Load image
    bg = background.rotate(angle)
    image = Image.open(fileName)
    imageArray = asarray(image)
    buffer = ""

    # Process image
    for y, row in enumerate(imageArray):
        for x, color in enumerate(row):
            if color[3] == 0:
                buffer += colorToStr(bg.getpixel((x, y)))
            else:
                buffer += colorToStr(color)

        if y + 1 != len(imageArray):
            buffer += "\n"

    # Write output
    print(str(angle) + " = " + "\"\"\"", file=output, end="")
    print(buffer, file=output, end="")
    print("\"\"\"", file=output)


output = open("assets/imageBuffer.txt", "w")
background = Image.open(bgFileName)

convert(0)
convert(90)
convert(180)
convert(270)

output.close()
