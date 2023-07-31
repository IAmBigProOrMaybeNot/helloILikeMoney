import os
from PIL import Image
from PIL import Image, ImageDraw, ImageFont, ImageColor
imagesList = []


def concat2Imgs(img1, img2):

    finalImg = Image.new(
        "RGBA", (img1.width+img2.width, img1.height+img2.height))
    finalImg.paste(img1, (0, 0))
    finalImg.paste(img2, (img1.width, 0))
    return finalImg


def addName(img, name):
    newImage = Image.new("RGBA", (img.width+70, img.height+20))
    newImage.paste(img, (0, 0))
    draw = ImageDraw.Draw(newImage)
    draw.text((0, img.height), name, fill="black")
    return newImage


directory = input()
for image in os.listdir(directory):
    if image.endswith(".png"):
        imagesList.append(directory+"\\"+image)
result = Image.new("RGBA", (0, 0))
for image in imagesList:
    print(image)
    PILImage = Image.open(image)
    PILImage = addName(PILImage, os.path.split(image)[-1])
    result = concat2Imgs(PILImage, result)
result.show("result")
result.save(f"{os.path.split(directory)[-1]}.png")
