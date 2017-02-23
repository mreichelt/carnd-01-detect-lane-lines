# coding=utf-8

#importing some useful packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
#plt.switch_backend('MacOSX')
#plt.ion()


#reading in an image
#image = mpimg.imread('test_images/solidWhiteRight.jpg')
#print('This image is:', type(image), 'with dimensions:', image.shape)
#plt.imshow(image)  # if you wanted to show a single color channel image called 'gray', for example, call as plt.imshow(gray, cmap='gray')
#plt.show()




import math

def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    """
    Applies an image mask.

    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)

    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    #filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    """
    NOTE: this is the function you might want to use as a starting point once you want to
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).

    Think about things like separating line segments by their
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of
    the lines and extrapolate to the top and bottom of the lane.

    This function draws `lines` with `color` and `thickness`.
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """

    # for line in lines:
    #     for x1,y1,x2,y2 in line:
    #         cv2.line(img, (x1, y1), (x2, y2), color, thickness)
    # return

    width = img.shape[1]

    left_p1 = []
    left_p2 = []
    right_p1 = []
    right_p2 = []

    for line in lines:
        for x1,y1,x2,y2 in line:
            centerX = (x1 + x2) / 2
            if (centerX < width / 2):
                left_p1.append((x1, y1))
                left_p2.append((x2, y2))
            else:
                right_p1.append((x1, y1))
                right_p2.append((x2, y2))

    if (len(left_p1) > 0 and len(left_p2) > 0):
        cv2.line(img, min(left_p1), max(left_p2), color, thickness)

    if (len(right_p1) > 0 and len(right_p2) > 0):
        cv2.line(img, min(right_p1), max(right_p2), color, thickness)


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.

    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines, thickness=5)
    return line_img

# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1, λ=0):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.

    `initial_img` should be the image before any processing.

    The result image is computed as follows:

    initial_img * α + img * β + λ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, λ)





def find_lane_lines(original_image):
    img = np.copy(original_image)

    # step 1: convert to gray scale and blur
    img = grayscale(img)
    img = gaussian_blur(img, 5)

    # step 2: find edges with canny
    img = canny(img, 50, 150)

    # step 3: now only use the region of the image that we're interested in
    #  -> the region where the lanes are
    height, width = img.shape
    vertices = np.array([[(width * 0.06, height), (width / 2.10, height / 1.68), (width / 1.90, height / 1.68), (width * 0.94, height)]], dtype=np.int32)
    img = region_of_interest(img, vertices)

    # step 4: find the hough lines
    rho = 2              # distance resolution in pixels of the Hough grid
    theta = np.pi/180    # angular resolution in radians of the Hough grid
    threshold = 15       # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 10 # minimum number of pixels making up a line
    max_line_gap = 80    # maximum gap in pixels between connectable line segments
    img = hough_lines(img, rho, theta, threshold, min_line_length, max_line_gap)

    # step 5: draw weighted image
    return weighted_img(img, original_image)



import os

for test_image in os.listdir("test_images/"):
    print('reading ' + test_image)
    img = mpimg.imread('test_images/' + test_image)
    img = find_lane_lines(img)
    #plt.imshow(img)
    mpimg.imsave("test_images_processed/" + test_image, img)

from moviepy.editor import VideoFileClip

def process_image(image):
    return find_lane_lines(image)

white_output = 'white.mp4'
clip1 = VideoFileClip("solidWhiteRight.mp4")
white_clip = clip1.fl_image(process_image)
white_clip.write_videofile(white_output, audio=False)

yellow_output = 'yellow.mp4'
clip2 = VideoFileClip('solidYellowLeft.mp4')
yellow_clip = clip2.fl_image(process_image)
yellow_clip.write_videofile(yellow_output, audio=False)

challenge_output = 'extra.mp4'
clip2 = VideoFileClip('challenge.mp4')
challenge_clip = clip2.fl_image(process_image)
challenge_clip.write_videofile(challenge_output, audio=False)
