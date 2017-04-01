import ocr
import alignDimensions

# Default image dimensions to use for neural network
dimX = 28
dimY = 28

"""represents an input image along with a caption"""
class Meme:

    def __init__(self, image, caption=None):
        self.image = image
        self.caption = caption
        # Photo OCR if we don't have an input caption
        if not self.caption:
            self.caption = ocr.ocr(self.image)
        # Make image dimensions uniform
        if len(self.image) != dimX or len(self.image[0]) != dimY:
            self.image = alignDimensions.alignDimensions(self.image)



