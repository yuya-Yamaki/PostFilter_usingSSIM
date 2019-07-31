
from PIL import Image
import numpy as np
import sys
from SSIM_PIL import compare_ssim

filter = [1/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9]

def post_filtering(rec_img):
    width, height = rec_img.size
    mod_img = Image.new('L', (width, height))

    rec_pel = np.array([[rec_img.getpixel((x,y)) for y in range(height)] for x in range(width)])
    tmp_pel = np.zeros(len(filter))

    print(rec_pel.ndim, rec_pel.shape, rec_pel.size)
#without padding
    for y in range(1, height-1):
        for x in range(1, width-1):
            tmp_pel[0] = rec_pel[x-1][y-1]
            tmp_pel[1] = rec_pel[x-1][y]
            tmp_pel[2] = rec_pel[x-1][y+1]
            tmp_pel[3] = rec_pel[x][y-1]
            tmp_pel[4] = rec_pel[x][y]
            tmp_pel[5] = rec_pel[x][y+1]
            tmp_pel[6] = rec_pel[x+1][y-1]
            tmp_pel[7] = rec_pel[x+1][y]
            tmp_pel[8] = rec_pel[x+1][y+1]

            sum_pel = np.zeros(1)
            for num in range(len(filter)):
                sum_pel += tmp_pel[num] * filter[num]

            mod_img.putpixel((x,y), (sum_pel,))

    return mod_img

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

    mod_img = post_filtering(rec_img)
    mod_img.show()
    mod_img.save("output_PF.pgm")

    ssim = calc_ssim(rec_img, mod_img)
    print(ssim)
