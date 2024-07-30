# led.py // @toblobs

from __init__ import *

emoji_converter = ['⬛', '⬜']

class Display:

    def __init__(self, dimensions = LED_DIMENSIONS):

        self.dimensions = dimensions
        self.matrix = np.full(shape = dimensions, fill_value = 0, dtype = int)
        self.shape = self.matrix.shape

    def __str__(self):

        outstr = """"""
    
        for iy, ix in np.ndindex(self.shape):
            outstr += emoji_converter[self.matrix[iy, ix]]
            
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

def create_display_from_emojis(emoji_str, dim = LED_DIMENSIONS):

    d = Display(dim)

    emoji_str = ''.join(emoji_str.split())

    for y in range(dim[1]):
        for x in range(dim[0]):

            index = emoji_converter.index(emoji_str[(x * dim[1]) + y])

            d.matrix[x, y] = index

    return d

global one
one = create_display_from_ids(np.matrix([[0, 0, 0, 0, 0],
                                       [0, 0, 0, 1, 0],
                                       [0, 0, 0, 1, 0],
                                       [0, 0, 0, 1, 0],
                                       [0, 0, 0, 1, 0],
                                       [0, 0, 0, 1, 0],
                                       [0, 0, 0, 0, 0]]))

global two
two = create_display_from_ids(np.matrix([[0, 0, 0, 0, 0],
                                [0, 1, 1, 1, 0],
                                [0, 0, 0, 1, 0],
                                [0, 1, 1, 1, 0],
                                [0, 1, 0, 0, 0],
                                [0, 1, 1, 1, 0],
                                [0, 0, 0, 0, 0]]))

global three
three = create_display_from_ids(np.matrix([[0, 0, 0, 0, 0],
                                [0, 1, 1, 1, 0],
                                [0, 0, 0, 1, 0],
                                [0, 1, 1, 1, 0],
                                [0, 0, 0, 1, 0],
                                [0, 1, 1, 1, 0],
                                [0, 0, 0, 0, 0]]))

global four
four = create_display_from_ids(np.matrix([[0, 0, 0, 0, 0],
                                [0, 1, 0, 1, 0],
                                [0, 1, 0, 1, 0],
                                [0, 1, 1, 1, 0],
                                [0, 0, 0, 1, 0],
                                [0, 0, 0, 1, 0],
                                [0, 0, 0, 0, 0]]))

global five
five = create_display_from_ids(np.matrix([[0, 0, 0, 0, 0],
                                [0, 1, 1, 1, 0],
                                [0, 1, 0, 0, 0],
                                [0, 1, 1, 1, 0],
                                [0, 0, 0, 1, 0],
                                [0, 1, 1, 1, 0],
                                [0, 0, 0, 0, 0]]))

global six
six = create_display_from_ids(np.matrix([[0, 0, 0, 0, 0],
                                [0, 1, 1, 1, 0],
                                [0, 1, 0, 0, 0],
                                [0, 1, 1, 1, 0],
                                [0, 1, 0, 1, 0],
                                [0, 1, 1, 1, 0],
                                [0, 0, 0, 0, 0]]))

global seven
seven = create_display_from_ids(np.matrix([[0, 0, 0, 0, 0],
                                [0, 1, 1, 1, 0],
                                [0, 0, 0, 1, 0],
                                [0, 0, 0, 1, 0],
                                [0, 0, 0, 1, 0],
                                [0, 0, 0, 1, 0],
                                [0, 0, 0, 0, 0]]))

global eight
eight = create_display_from_ids(np.matrix([[0, 0, 0, 0, 0],
                                [0, 1, 1, 1, 0],
                                [0, 1, 0, 1, 0],
                                [0, 1, 1, 1, 0],
                                [0, 1, 0, 1, 0],
                                [0, 1, 1, 1, 0],
                                [0, 0, 0, 0, 0]]))
