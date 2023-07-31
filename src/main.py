import scipy
import gc
from PIL import ImageFilter
import random
from googleapiclient.http import MediaFileUpload
import googleapiclient.errors
import googleapiclient.discovery
import google_auth_oauthlib.flow
import math
import os
import cv2
import numpy as np
import moviepy
from PIL import Image
import moviepy.editor as mp
import logging
import Music
from Config import Config
from Thumbnail import Thumbnail

logging.basicConfig()

FPS = int(Config.getConfig("VIDEO","FPS",60))

musicFolder = """C:\\Users\\Luki\\PycharmProjects\\HelloILikeMoney\\music"""


def generateUnscrapedFromScraped(scraped):
    scrapedGrayscale = scraped.convert("L")
    image = scrapedGrayscale.filter(ImageFilter.FIND_EDGES).convert("RGBA")
    return image


def addSongsToVideo(dir, to, music):
    clip = mp.VideoFileClip(dir)
    clip.audio = music
    clip.write_videofile(to)
    logging.log(1,"Removing video without music cos no longer needed")
    os.remove(dir)
    


def saveImagesIntoGifFormat(imgs):
    savedPlace = "temp.gif"
    imgs[0].save(savedPlace, save_all=True, optimize=False,
                 append_images=imgs[1:], loop=0,)
    return savedPlace


def generateImagesForVideo(brush, scraped, unscraped):
    step = int(Config.getConfig("VIDEO","STEP",20))

    print(step)
    largeMask = Image.new("L", (scraped.width, scraped.height), (0))

    frameSize = (scraped.width, scraped.height)

    filepath = 'videos\\{0}.mp4'.format(os.path.split(scraped.filename)[-1])

    out = cv2.VideoWriter(filepath, -1, FPS, frameSize)

    for x in range(0, scraped.width - 20, math.ceil(step)):
        for y in range(0, scraped.height - 20, math.ceil(step)):
            open_cv_image = makeCV2Image(
                brush, scraped, unscraped, largeMask, x, y)

            out.write(open_cv_image)
    out.release()

    return filepath


def makeCV2Image(brush, scraped, unscraped, largeMask, x, y):
    largeMask.paste(brush, (x, y))
    unscraped = Image.composite(scraped, unscraped, largeMask)
    cv2Img = convert_from_image_to_cv2(unscraped)
    # print(cv2Img)
    return cv2Img


def calculateStepWithMusic(duration, w, h):

    logging.warning(str(duration))
    frames = 10*duration
    step = math.sqrt(w*h/frames)
    return step


def makeVideoWrapper(scrapedPath,  brushPath):
    scraped = Image.open(scrapedPath).resize((1920,1200))
    unscraped = generateUnscrapedFromScraped(scraped).convert("RGBA")
    brush = Image.open(brushPath)

    generateAddictingVideosForChildren(scraped, unscraped, brush)

    tierdownAfterVideo(scrapedPath)
    thumbnail = Thumbnail(scraped, unscraped, "mylittlepony",
                     os.path.split(scrapedPath)[-1])
    thumbnail.makeThumbnail()
    thumbnail.saveThumbnail()

def generateAddictingVideosForChildren(scraped, unscraped, brush):
    musicObj = Music.Music(musicFolder=musicFolder)
    music = musicObj.bestFit(calculateLengthOfVideo(20, scraped))

    logging.warning("Starting to create addicting video for children")
    filepath = generateImagesForVideo(brush, scraped, unscraped)
    addSongsToVideo(filepath, os.path.abspath("videos\\{0}final.mp4".format(
        os.path.split(scraped.filename)[-1])), music)
    # uploadToYoutube()


def calculateLengthOfVideo(step, scraped):
    w, h = scraped.width, scraped.height
    return w/step*h/step


def tierdownAfterVideo(scrapedPath):
    logging.warning("Putting unscraped and scraped image from {0} to folder processed".format(
        scrapedPath))

    scrapedName = os.path.basename(scrapedPath)



    os.rename(scrapedPath, os.path.abspath("processedImages\\"+scrapedName))

def getComponentsFromPathAndRename(scrapedPath):
    components = list(os.path.split(scrapedPath))
    components[components.index("images")] = "processedImages"

    return components

def convert_from_image_to_cv2(img: Image) -> np.ndarray:
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


for i in os.listdir("images"):
    logging.warning("PROCESSING IMAGE {0}".format(i))
    makeVideoWrapper(os.path.join("images", i), "bruch.png")
    gc.collect()