import requests
from PIL import Image
from io import BytesIO

class AsciiArtGenerator:

    def __init__(self):
        self.pixel_values = []
        self.blocks = []
        self.characters = []

        self.image_width = 0
        self.block_width = 4
        self.block_height = 6

    # Loads an image and gets pixel values
    # Sets image dimensions and block dimensions
    # The image will be trimmed (rows/cols removed) in order to fit the block size
    def load_image(self, output_filename, local_url=None, url=None):     
        # Get the image   
        if(local_url != None):
            file = open(local_url, 'rb')
            image = Image.open(file)
        else:
            res = requests.get(url)
            image = Image.open(BytesIO(res.content))

        # Get image dimensions
        img_w = image.size[0]
        img_h = image.size[1]
        self.image_width = img_w

        # Set block size
        block_w = self.block_width
        block_h = self.block_height

        # Transform pixel values (1d array) into a 2d array
        pixels = list(image.getdata())
        for i in range(0, int(len(pixels) / img_w)):
            start = i * img_w
            self.pixel_values.append(pixels[start:start + img_w])

        # Remove rows / cols if necessary
        mod_w = int(img_w % block_w)
        mod_h = int(img_h % block_h)
        if(mod_w != 0):
            self.remove_cols(mod_w)
        if(mod_h != 0):
            self.remove_rows(mod_h)
        
        # Compute the blocks and get the characters
        self.compute_blocks(block_w, block_h)
        self.characters = [ self.get_character(i) for i in self.blocks ]
        
        # Write the characters to output file
        self.output_characters(output_filename)
   
    # Separates pixels in each block into a 2d list
    def compute_blocks(self, block_w, block_h):
        blocks = []
        # Go through every block segment in the image
        for y in range(0, len(self.pixel_values), block_h): 
            for x in range(0, len(self.pixel_values[0]), block_w):
                # Add each pixel in the block
                block = []
                for row in self.pixel_values[y:y + block_h]:
                    for pixel in row[x:x + block_w]:
                        block.append(pixel)
                blocks.append(block)
        
        # Now that we have all the blocks
        # Get the average grayscale value of each block in rgb
        self.compute_block_values(blocks)

    # Removes n rows of pixels from the bottom of the image
    def remove_rows(self, n_rows):
        self.pixel_values = self.pixel_values[:-n_rows]

    # Removes n columns of pixels from the right of the image
    def remove_cols(self, n_cols):
        for i in range(0, len(self.pixel_values)):
            self.pixel_values[i] = self.pixel_values[i][:-n_cols]

    # Computes the average grayscale value for each pixel (0-255.99)
    # Then computes the average grayscale value for each block
    # And converts that value to float (0-1.0)
    def compute_block_values(self, blocks):
        # First convert each pixel tuple (r, g, b, a) into grayscale value (0-255.99)
        for i in range(0, len(blocks)):
            for j in range(0, len(blocks[i])):
                blocks[i][j] = sum(blocks[i][j][:3]) / 3

        # Get the grayscale value (0-255.99) for each block
        # And convert the value to float (0.0 - 1.0)
        for i in range(0, len(blocks)):
            blocks[i] = sum(blocks[i]) / len(blocks[i])
            blocks[i] = blocks[i] / 255.99

        # Finally, assign to blocks so characters can be computed
        self.blocks = blocks

    # Returns an ascii character based on grayscale float value
    def get_character(self, grayscale_float):
        if(grayscale_float < 0.1):
            return ' '
        elif(grayscale_float >= 0.1 and grayscale_float < 0.2):
            return '.'
        elif(grayscale_float >= 0.2 and grayscale_float < 0.3):
            return ':'
        elif(grayscale_float >= 0.3 and grayscale_float < 0.4):
            return '-'
        elif(grayscale_float >= 0.4 and grayscale_float < 0.5):
            return '='
        elif(grayscale_float >= 0.5 and grayscale_float < 0.6):
            return '+'
        elif(grayscale_float >= 0.6 and grayscale_float < 0.7):
            return '*'
        elif(grayscale_float >= 0.7 and grayscale_float < 0.8):
            return '#'
        elif(grayscale_float >= 0.8 and grayscale_float < 0.9):
            return '%'
        elif(grayscale_float >= 0.9):
            return '@'

    # Outputs the characters to a file
    def output_characters(self, filename):
        width = self.image_width / self.block_width
        with open(filename, 'w') as file:
            for i in range(0, len(self.characters)):
                file.write(self.characters[i])
                if((i + 1) % int(width) == 0):
                    file.write('\n')

                    
            
