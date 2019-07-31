from PIL import Image
import numpy as np
import sys
from SSIM_PIL import compare_ssim


filter = [1/9, 1/9, 1/9,
          1/9, 1/9, 1/9,
          1/9, 1/9, 1/9]

def post_filtering(rec_pel, a, b):
    #without padding
    #patch processing
    filter_yx = [[-1,-1], [-1, 0], [-1, 1],
                 [ 0,-1], [ 0, 0], [ 0, 1], 
                 [ 1,-1], [ 1, 0], [ 1, 1]]
    sum_pel = np.zeros(1)
    for num in range(len(filter)):
        x = a + filter_yx[num][1]
        if(x > width - 1):
            x = width - 1
        elif(x < 0):
            x = 0
        y = b + filter_yx[num][0]
        if(y > height - 1):
            y = height - 1
        elif(y < 0):
            y = 0

        sum_pel += rec_pel[x][y] * filter[num]

    return sum_pel

def calc_ssim(rec_img, mod_img):
    return compare_ssim(rec_img, mod_img)

if __name__ == '__main__':
    param = sys.argv
    if(len(param) != 2):
        print("Usage: $ python " + param[0] + " input.pgm")
        quit()

    #open image file
    try:
        rec_img = Image.open(param[1])
    except:
        print('failed to load %s' % param[1])
        quit()

    if rec_img is None:
        print('failed to load %s' % param[1])
        quit()

    #execute PostFilter to reconstructed image and get modified image
    width, height = rec_img.size
    mod_img = Image.new('L', (width, height))

    rec_pel = np.array([[rec_img.getpixel((x,y)) for y in range(height)] for x in range(width)])
    tmp_pel = np.zeros(len(filter))
    print(rec_pel.ndim, rec_pel.shape, rec_pel.size)
    
    for y in range(height):
        for x in range(width):
                sum_pel = post_filtering(rec_pel, x, y)
                mod_img.putpixel((x,y), (sum_pel,))

    #calcurate SSIM using module SSIM-PIL
    ssim = calc_ssim(rec_img, mod_img)

    #test
    #mod_img.show()
    mod_img.save("output_PF_y.pgm")

    print(ssim)
