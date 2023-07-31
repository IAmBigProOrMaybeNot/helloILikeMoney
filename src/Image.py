import numpy
import PIL
import cv2


class Image:
    imageBehaviour = None

    def __init__(self, behaviour, path) -> None:
        self.imageBehaviour = behaviour

    def resize(self, x, y):
        self.imageBehaviour.resize(x, y)

    def paste(self, image, x, y, mask=None):
        self.imageBehaviour.paste(image, x, y, mask)

    def composite(self, image2, mask):
        self.imageBehaviour.composite(image2, mask)


class ImageBehaviour(Image):
    def resize(self, x, y) -> Image:
        pass

    def paste(self, image, x, y, mask=None):
        pass

    def composite(self, image2, mask):
        pass


class PillowImageBehaviour(ImageBehaviour):
    def __init__(self, path) -> None:
        self.internal = PIL.Image.open(path)

    def resize(self, x, y):
        self.internal = self.internal.resize((x, y))

    def paste(self, image, x, y, mask=None):
        self.internal.paste(image, (x, y), mask)

    def composite(self, image2, mask):
        pass
class OpenCVImageBehaviour(ImageBehaviour):
    def __init__(self, path) -> None:
        self.internal = cv2.imread(path,cv2.IMREAD_COLOR)

    def resize(self, x, y):
        self.internal = cv2.resize(self.internal,(x,y))

    def paste(self, image, x, y, mask=None):
        self.internal.paste(image, (x, y), mask)

    def composite(self,image2, mask):
        inv_mask = cv2.bitwise_not(mask).astype(np.float64)
        maskAsFloat = mask.astype(np.float64)
        img1 = cv2.multiply(maskAsFloat, image2) / 255.0
        img2 = cv2.multiply(inv_mask, self.internal) / 255.0
        self.internal = (cv2.add(img1, img2)).astype(np.uint8)