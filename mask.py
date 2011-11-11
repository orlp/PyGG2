import c._mask
import Image

import zipfile
import cStringIO

Mask = c._mask.Mask

# def save_mask(mask, name):
    # img = Image.new("RGBA", mask.get_size())
    # for x in range(mask.get_size()[0]):
        # for y in range(mask.get_size()[1]):
            # if mask.get_at((x, y)):
                # img.putpixel((x, y), (50, 50, 50, 255))
    # img.save(name)

def from_image(image, threshold = 127):
    try: img = image.convert("RGBA")
    except: img = Image.open(image, "r").convert("RGBA")

    return c._mask.load_mask_from_image_PIL(img.im.id, threshold)

def from_image_colorthreshold(image, color, threshold = (0, 0, 0, 255)):
    try: img = image.convert("RGBA")
    except: img = Image.open(image, "r").convert("RGBA")

    return c._mask.load_mask_from_image_threshold_PIL(img.im.id, color, threshold)