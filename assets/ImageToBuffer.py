from PIL import Image
from numpy import asarray

fileName = "assets/apple.png"

# Load image
image = Image.open(fileName)
imageArray = asarray(image)
buffer = ""

# Process image
for i, row in enumerate(imageArray):
    for color in row:
        if color[3] == 0:
            buffer += "#000"
        else:
            buffer += "#"+hex(round(color[0] / 255 * 15))[2] + hex(
                round(color[1] / 255 * 15))[2] + hex(round(color[2] / 255 * 15))[2]

    if i + 1 != len(imageArray):
        buffer += "\n"

# Write output
output = open("assets/imageBuffer.txt", "w")
print("\"\"\"", file=output, end="")
print(buffer, file=output, end="")
print("\"\"\"", file=output, end="")
output.close()
