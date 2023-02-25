from PIL import Image
from numpy import asarray

fileName = "test.png"

# Load image
image = Image.open(fileName)
imageArray = asarray(image)
buffer = ""

# Process image
for row in imageArray:
    for color in row:
        if color[3] == 0:
            buffer.append("#000")
        else:
            buffer.append("#"+hex(round(color[0] / 255 * 15))[2] + hex(
                round(color[1] / 255 * 15))[2] + hex(round(color[2] / 255 * 15))[2])
    buffer += "\n"

# Write output
output = open("imageBuffer.txt", "w")
print("\"", file=output)
print(buffer, file=output, end="")
print("\"", file=output)
output.close()
