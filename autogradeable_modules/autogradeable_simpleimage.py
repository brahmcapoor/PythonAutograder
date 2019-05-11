#!/usr/bin/env python3

"""
Stanford CS106AP AutogradeableSimpleImage module
Brahm Capoor
 -5/2019 Autogradeable version (changed implementation of SimpleImage.show)
Nick Parlante
 -4/2019 stripped down version
 does not have files or foreach
Supports creating a blank image,
and setting red/green/blue per pixel on it.
Features:
1. image = SimpleImage.blank(400, 200)   # create new image of size
2. image.width, image.height      # access size
3. pixel = image.get_pixel(x, y)  # access pixel at x,y
4. pixel.red = 100   # set red/green/blue of pixel
5. image.show()      # display image on screen

Example use - makes big yellow image
(this same code is in main() in this file).

from simpleimage import SimpleImage
...

    image = SimpleImage.blank(400, 200)
    for y in range(image.height):
        for x in range(image.width):
            pixel = image.get_pixel(x, y)
            pixel.red = 255
            pixel.green = 255
            pixel.blue = 0
    image.show()
"""

# If this line fails, "Pillow" needs to be installed
from PIL import Image


def clamp(num):
    """
    Return a "clamped" version of the given num,
    converted to be an int limited to the range 0..255 for 1 byte.
    """
    num = int(num)
    if num < 0:
        return 0
    if num >= 256:
        return 255
    return num


class Pixel(object):
    """
    A pixel at an x,y in a SimpleImage.
    Supports set/set .red .green .blue
    and get .x .y
    """

    def __init__(self, image, x, y):
        self.image = image
        self._x = x
        self._y = y

    def __str__(self):
        return 'r:' + str(self.red) + ' g:' + str(self.green) + ' b:' + str(self.blue)

    # Pillow image stores each pixel color as a (red, green, blue) tuple.
    # So the functions below have to unpack/repack the tuple to change anything.

    @property
    def red(self):
        return self.image.px[self._x, self._y][0]

    @red.setter
    def red(self, value):
        rgb = self.image.px[self._x, self._y]
        self.image.px[self._x, self._y] = (clamp(value), rgb[1], rgb[2])

    @property
    def green(self):
        return self.image.px[self._x, self._y][1]

    @green.setter
    def green(self, value):
        rgb = self.image.px[self._x, self._y]
        self.image.px[self._x, self._y] = (rgb[0], clamp(value), rgb[2])

    @property
    def blue(self):
        return self.image.px[self._x, self._y][2]

    @blue.setter
    def blue(self, value):
        rgb = self.image.px[self._x, self._y]
        self.image.px[self._x, self._y] = (rgb[0], rgb[1], clamp(value))

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


# color tuples for background color names 'red' 'white' etc.
BACK_COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
}


class SimpleImage(object):
    def __init__(self, width, height, back_color):
        if not back_color:
            back_color = 'white'
        color_tuple = BACK_COLORS[back_color]
        self.pil_image = Image.new('RGB', (width, height), color_tuple)
        self.px = self.pil_image.load()
        size = self.pil_image.size
        self._width = size[0]
        self._height = size[1]

    @classmethod
    def blank(cls, width, height, back_color=None):
        """Create a new blank image of the given width and height."""
        return SimpleImage(width, height, back_color=back_color)

    @property
    def width(self):
        """Width of image in pixels."""
        return self._width

    @property
    def height(self):
        """Height of image in pixels."""
        return self._height

    def get_pixel(self, x, y):
        """
        Returns a Pixel at the given x,y, suitable for getting/setting
        .red .green .blue values.
        """
        if x < 0 or x >= self._width or y < 0 or y >= self.height:
            e = Exception('get_pixel bad coordinate x %d y %d (vs. image width %d height %d)' %
                          (x, y, self._width, self.height))
            raise e
        return Pixel(self, x, y)

    def set_rgb(self, x, y, red, green, blue):
        """
        Set the pixel at the given x,y to have
        the given red/green/blue values without
        requiring a separate pixel object.
        """
        self.px[x, y] = (red, green, blue)

    def show(self):
        """
        Prints each pixel individually
        """
        for y in range(self._height):
            for x in range(self._width):
                print(self.px[x, y])


def main():
    """
    main() runs an example - makes a big yellow image.
    """
    image = SimpleImage.blank(400, 200)
    for y in range(image.height):
        for x in range(image.width):
            pixel = image.get_pixel(x, y)
            pixel.red = 255
            pixel.green = 255
            pixel.blue = 0
    image.show()


if __name__ == '__main__':
    main()
