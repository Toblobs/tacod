# led.py // @toblobs

from __init__ import *
from dbio import get_confidence_threshold

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
    
    def get_on_coords(self):

        return [(ix, iy) for ix, iy in np.ndindex(self.shape) if self.matrix[ix, iy] == 1]
    
    def get_off_coords(self):

        return [(ix, iy) for ix, iy in np.ndindex(self.shape) if self.matrix[ix, iy] == 0]
                
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

def generate_using_weights(weights_array, dim = LED_DIMENSIONS, threshold = get_confidence_threshold()):

    d = Display(dim)

    for iy, ix in np.ndindex(weights_array.shape):

        if float(weights_array[iy, ix]) > threshold and random.random() < weights_array[iy, ix]:
            d.matrix[iy, ix] = 1

    return d

def generate_lines(weights_array, num, dim = LED_DIMENSIONS, amount = LINE_GENERATION_AMOUNT):
    
    result = weights_array.copy()
    lines = []

    for x in range(num):

        line_start_pos = random.choice(random.choice([get_row(x) for x in range(dim[0])]))

        x = line_start_pos[0]
        y = line_start_pos[1]

        length = random.randint(3, 5)

        directions = [get_row(x, fro = y, to = y + (length + 1)), # east 
                    get_row(x, to = y, fro = y - (length + 1)), # west
                    get_col(y, fro = x, to = x + (length + 1)), # south
                    get_col(y, to = x, fro = x - (length + 1)), # north
                    ]

        culled = []
        
        for d in directions:
            if len(d) != length:
                pass
            else:
                culled.append(d)
    
        if culled: # aka we have a valid line to gen
            
            chosen = random.choice(culled)
            lines.append(chosen)

            for c in chosen:
                result[c] += amount

                if result[c] > 1:
                    result[c] = 1

    return [result, lines]




    
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

def get_row(row, dim = LED_DIMENSIONS[1], fro = 0, to = LED_DIMENSIONS[0]):
     
    return [(row, c) for c in range(dim) if fro <= c <= to]

def get_col(col, dim = LED_DIMENSIONS[0], fro = 0, to = LED_DIMENSIONS[1]):
    
    return [(x, y) for y in range(dim) for x in range(dim) if (y == col) and (fro <= x <= to)]