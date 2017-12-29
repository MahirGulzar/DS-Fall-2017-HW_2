import os, pygame       # Must install pygame for this module to work (see Manual)

def load_image(name):
    """Load images."""
    fullname = os.path.join("images", name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() == None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
        print "Oops! Could not load image:", fullname
    return image, image.get_rect()
