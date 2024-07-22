# led.py // @toblobs

from __init__ import *

class Display:

    def __init__(self, dimensions = LED_DIMENSIONS):

        self.dimensions = dimensions
        self.matrix = np.full(shape = dimensions, fill_value = 0, dtype = int)
        self.shape = self.matrix.shape

        self.emoji_converter = ['⬛', '⬜']

    def __str__(self):

        outstr = """"""
    
        for iy, ix in np.ndindex(self.shape):
            outstr += self.emoji_converter[self.matrix[iy, ix]]
            
            if ix == (self.dimensions[1] - 1):
                outstr += '\n'
            
        return outstr
