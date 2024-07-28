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


def create_display_from_ids(id_array, dim = LED_DIMENSIONS):
    
    if id_array.shape == dim:
        
        d = Display(dim)
        d.matrix = id_array
        
        return d

    else:
        return False

    
# ---- # to be moved to a different file

class Question:

    def __init__(self, question, id, leds, correct_index):

        self.question = question
        self.id = id
        self.leds = leds
        self.correct = correct_index

        assert correct_index < len(leds) - 1, "The correct index must be an index of a display in the LEDs list."