# -*- coding: utf-8 -*-

from PIL import Image
import pytesseract 

im = Image.open("/cygdrive/e/workspace/py-warehouse/downloads/captchas/1.jpeg")
im = im.convert("L")
im2 = Image.new("L", im.size, 255)

for x in range(im.size[1]):
    for y in range(im.size[0]):
        pix = im.getpixel((y, x))
        if pix < 100:  # these are the numbers to get
            im2.putpixel((y, x), 0)

im2.save("save.png")
print(pytesseract.image_to_string(im2))
