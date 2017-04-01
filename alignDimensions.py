# TODO: look at https://pillow.readthedocs.io/en/4.0.x/reference/Image.html

def alignDimensions(image, dimX, dimY):
    """given an image (2d array of RGB pixel values), aligns the dimensions
    of the image to be dimX x dimY"""
    # TODO: other methods
    return crop(image, dimX, dimY)

def crop(image, dimX, dimY):
    """ crops image to be of dimX x dimY. If image is too small, adds black
    pixels. By default, takes pixels from top-left corner."""
    # TODO
    return image
    
