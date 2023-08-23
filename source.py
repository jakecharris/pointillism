import numpy as np
from PIL import Image

# Goal: convert an image file from normal pixels to ANSI art made of dots "."
# of same color with canvas-like color background

# ANSI foreground color (n, 0-255) based on 256-bit -> \033[38;5;nm
# ANSI background color (n, 0-255) based on 256-bit -> \033[48;5;nm
# end with \033[m
# colors: https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
# example: print("\033[48;5;19m\033[38;5;214mHello world!\033[m")

# Open the image
def open_image_array(img_dir="razorback.png"):
    
    # img_dir = input("Name your picture's filename: ") # input image path
    img_rgb = Image.open(img_dir).convert('RGB') # convert from RGBA to RGB
    # img_rgb.show()
    
    # convert image into 3D array of 3 8-bit RGB values for each pixel
    rgb_array = np.array(img_rgb, dtype=np.uint8)
    size_d = list(rgb_array.shape) # pic dims [y, x, 3]
    size_d[2] = -1 # change 3 -> -1
    
    # convert 3D 8-bit color array to 2D int32 color array (each pixel has 1 ANSI color value)
    colorint32 = np.dstack((rgb_array, np.zeros(rgb_array.shape[:2], 'uint8'))).view('uint32').squeeze(-1)
    ansi_array = np.floor(colorint32**(1/3)) # cube root & round down to get 256 ANSI color codes
    
    # convert 2d int32 array back to 3D 8-bit array, if needed
    rgb_convert = colorint32.view('uint8').reshape(size_d)[:,:,:3]
    
    # ANSI array of colored dots based on ansi_colors array
    # BG = 230 # off-white background canvas color ANSI code
    ansi_list = ansi_array.astype('uint8').tolist() # convert array to list of lists
    for lst in ansi_list:
        dot_list = ['\033[48;5;230m'] # BG color
        for val in lst:
            dot = '\033[38;5;' + str(val) + 'm.' # add FG color values
            dot_list.append(dot)
        dot_list.append('\033[m')
        row = ''.join(dot_list)
        print(row)
    
    # Image.fromarray(canvas_array).show()
    # print("\033[48;5;230m\033[38;5;45m.\033[38;5;7m.\033[m")
    # print(len(canvas_list))
    # print(rgb_array)
    # print(size_d)
    # print(colorint32)
    # print(canvas_array)
    # print(canvas_list)
    
    

if __name__ == "__main__":
    open_image_array()