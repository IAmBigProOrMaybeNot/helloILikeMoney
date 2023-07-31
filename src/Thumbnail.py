import os
from PIL import Image
from Config import Config
from PIL import Image, ImageEnhance
class Thumbnail:

    def _loadArrowForThumbnail(self,imageAspectRatio):
        self.arrow = Image.open(os.path.abspath("arrow.png"))
    def _finishThumbnail(self,imageAspectRatio):
        self._makeScrapedUnscrapedTransition()

        self._addArrowAndLogoToThumbnail(imageAspectRatio)

    def calculatePositionOnImage(self,image,posXRatio,posYRatio):
        return int(posXRatio * image.width) , int(posYRatio * image.height)

    def _addArrowAndLogoToThumbnail(self, imageAspectRatio):
        self._addArrowToThumbnail()
        self._addLogoToThumbnail()

    def _addArrowToThumbnail(self):
        arrowRatioX,arrowRatioY = float(Config.getConfig("THUMBNAIL","arrowRatioX",0.5)),float(Config.getConfig("THUMBNAIL","arrowRatioY",0.5))
        self.thumbnail.paste(self.arrow,self.calculatePositionOnImage(self.scraped,arrowRatioX,arrowRatioY) , self.arrow)

    def _addLogoToThumbnail(self):
        logoRatioX,logoRatioY = float(Config.getConfig("THUMBNAIL","logoRatioX",0.5)),float(Config.getConfig("THUMBNAIL","logoRatioY",0.5))
        self.thumbnail.paste(
            self.logo, self.calculatePositionOnImage(self.scraped,logoRatioX,logoRatioY), self.logo)

    def _makeScrapedUnscrapedTransition(self):
        self.thumbnail = Image.new(
            "RGBA", (self.scraped.width, self.scraped.height), (0, 0, 0, 0))
        self.thumbnail = Image.composite(
            self.scraped, self.unscraped, self.maskGradient).convert("RGBA")
    def _prepareLogoForThumbnail(self):
        w = self.scraped.width
        self.logo = Image.open(os.path.join(self.type, "logo.png")).convert("RGBA")
        aspectRatio = self._calculateImageAspectRatio(self.logo)
        self.logo = self.logo.resize((int(w // 5), int((w // 5) * aspectRatio)))


    def __init__(self,scraped, unscraped, type, name):
        self.scraped = scraped
        self.unscraped = unscraped
        self.type = type
        self.name = name

    def makeThumbnail(self):
        
        imageAspectRatio = self._calculateImageAspectRatio(self.scraped)

        self.unscraped = self.unscraped.resize((self.scraped.width, self.scraped.height))

        self._prepareLogoForThumbnail()

        self._loadMaskGradient()

        self._loadArrowForThumbnail(imageAspectRatio)

        self._finishThumbnail(imageAspectRatio)
        return self.thumbnail
    def _calculateImageAspectRatio(self, image):
        return image.width/image.height
    def saveThumbnail(self):
        path = "thumbnails\\{0}thumbnail.png".format(self.name)
        print(path)
        self.thumbnail.save(path)
    def _calculateAspectRatioToDefaultSIze(self,scraped):
        defaultSize = [1280, 720]
        imageAspectRatio = [scraped.width /
                            defaultSize[0], scraped.height/defaultSize[1]]

        return imageAspectRatio
    def _loadMaskGradient(self):
        maskGradient = maskGradient = Image.open(
            self.getMaskGradientPath()).convert("L")
        self.maskGradient = maskGradient.resize((self.scraped.width, self.scraped.height))

    def getMaskGradientPath(self):
        return Config.getConfig("VIDEO","maskGradient","ERROR")
    def applyFinishingEffects(self):
        pass
