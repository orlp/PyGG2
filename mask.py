import mask_extension._mask
import Image

import zipfile
import cStringIO

Mask = mask_extension._mask.Mask

def from_image(image, threshold = 127):
    try: img = image.convert("RGBA")
    except: img = Image.open(image, "r").convert("RGBA")

    return mask_extension._mask.load_mask_from_image_PIL(img.im.id, threshold)

def from_image_colorthreshold(image, color, threshold = (0, 0, 0, 255)):
    try: img = image.convert("RGBA")
    except: img = Image.open(image, "r").convert("RGBA")

    return mask_extension._mask.load_mask_from_image_threshold_PIL(img.im.id, color, threshold)